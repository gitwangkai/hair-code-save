"""
control/obstacle_avoidance.py
障碍物检测与避障模块：消费激光雷达数据，发出停止或绕行指令。
与运动控制模块解耦：只发事件，不直接操作底盘。
"""

from __future__ import annotations
import math
import numpy as np

try:
    from rclpy.node import Node
    from sensor_msgs.msg import LaserScan, Range
    from std_msgs.msg import Bool
    ROS_AVAILABLE = True
except ImportError:
    ROS_AVAILABLE = False
    Node = object

from config.settings import AvoidanceConfig
from utils.event_bus import EventBus
from utils.logger import get_logger


class ObstacleAvoidance:
    """ObstacleAvoidance 别名，兼容 main.py 接口"""
    
    def __init__(self, config, event_bus):
        self._avoider = ObstacleAvoider(config, event_bus)
        self._config = config
        self._bus = event_bus
        self._running = False
    
    async def start(self):
        """启动避障模块"""
        self._running = True
        # 订阅雷达扫描
        self._bus.subscribe("lidar/scan", self._on_scan)
    
    async def stop(self):
        """停止避障模块"""
        self._running = False
    
    def _on_scan(self, data):
        """处理雷达扫描"""
        # 转换 LidarScan 为字典格式
        payload = {
            "ranges": data.ranges.tolist(),
            "angle_min": data.angle_min,
            "angle_increment": data.angle_increment
        }
        self._avoider.on_lidar_scan(payload)
    
    async def update_scan(self, data):
        """更新扫描（兼容接口）"""
        self._on_scan(data)


class ObstacleAvoider:
    """
    输入事件: lidar_scan, ultrasonic_range, cliff_detected
    输出事件: obstacle_detected, obstacle_cleared, obstacle_command
    """

    def __init__(self, config: AvoidanceConfig, bus: EventBus):
        self._config = config
        self._bus = bus
        self._logger = get_logger("ObstacleAvoider")
        self._obstacle_active = False

        bus.subscribe("lidar_scan",      self.on_lidar_scan)
        bus.subscribe("ultrasonic_data", self._on_ultrasonic)
        bus.subscribe("cliff_detected",  self._on_cliff)

    # ── 公开回调 ───────────────────────────────────────────────
    def on_lidar_scan(self, payload: dict) -> None:
        """处理激光雷达扫描，检测前方扇区障碍。"""
        ranges = np.array(payload["ranges"], dtype=np.float32)
        angle_min = payload["angle_min"]
        angle_increment = payload["angle_increment"]

        # 只检测前方 ±60° 扇区
        front_angle = math.radians(60)
        n = len(ranges)
        indices = [
            i for i in range(n)
            if abs(angle_min + i * angle_increment) <= front_angle
        ]
        front_ranges = ranges[indices]
        valid = front_ranges[(front_ranges > 0.05) & (front_ranges < 20.0)]

        if valid.size == 0:
            return

        min_dist = float(np.min(valid))
        self._evaluate_obstacle(min_dist, source="lidar")

    def _on_ultrasonic(self, payload: dict) -> None:
        """超声波补充近距离盲区检测（<0.3m）。"""
        distance = payload.get("range", 999)
        if distance < self._config.stop_distance:
            self._trigger_obstacle(distance, source="ultrasonic")

    def _on_cliff(self, payload) -> None:
        """悬崖检测：立即触发紧急停止。"""
        self._logger.warning("悬崖检测触发！紧急停止")
        self._bus.publish("obstacle_command", {"stop": True, "reason": "cliff"})
        self._bus.publish("obstacle_detected", {"distance": 0, "reason": "cliff"})

    # ── 内部逻辑 ────────────────────────────────────────────────
    def _evaluate_obstacle(self, distance: float, source: str) -> None:
        stop_dist = self._config.stop_distance
        slow_dist = self._config.slow_distance

        if distance < stop_dist:
            self._trigger_obstacle(distance, source)
        elif distance < slow_dist:
            # 减速区：发布减速因子
            factor = (distance - stop_dist) / (slow_dist - stop_dist)
            self._bus.publish("obstacle_command", {
                "stop": False,
                "slow_factor": float(factor),
                "reason": source,
            })
            if self._obstacle_active:
                self._obstacle_active = False
                self._bus.publish("obstacle_cleared", {"source": source})
        else:
            if self._obstacle_active:
                self._obstacle_active = False
                self._bus.publish("obstacle_cleared", {"source": source})
                self._bus.publish("obstacle_command", {"stop": False, "slow_factor": 1.0})

    def _trigger_obstacle(self, distance: float, source: str) -> None:
        if not self._obstacle_active:
            self._obstacle_active = True
            self._logger.warning(f"障碍物！距离={distance:.2f}m 来源={source}")
            self._bus.publish("obstacle_detected", {
                "distance": distance, "source": source
            })
            self._bus.publish("obstacle_command", {"stop": True, "reason": source})
