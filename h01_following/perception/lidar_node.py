"""
perception/lidar_node.py
激光雷达 ROS 订阅节点
"""

import asyncio
import math
from dataclasses import dataclass
from typing import Optional, List
import numpy as np

try:
    import rclpy
    from rclpy.node import Node
    from sensor_msgs.msg import LaserScan
    ROS_AVAILABLE = True
except ImportError:
    ROS_AVAILABLE = False

from utils.event_bus import EventBus
from utils.logger import get_logger

logger = get_logger("lidar_node")


@dataclass
class LidarScan:
    """激光雷达扫描数据"""
    ranges: np.ndarray        # 距离数组 (m)
    angles: np.ndarray        # 角度数组 (rad)
    intensities: Optional[np.ndarray] = None  # 强度
    timestamp: float = 0.0    # 时间戳
    frame_id: str = ""        # 坐标系 ID
    angle_min: float = 0.0    # 起始角度
    angle_max: float = 0.0    # 终止角度
    angle_increment: float = 0.0  # 角度步长
    range_min: float = 0.0    # 最小有效距离
    range_max: float = 0.0    # 最大有效距离
    
    def get_points_in_range(self, angle_start: float, angle_end: float) -> np.ndarray:
        """获取指定角度范围内的点"""
        mask = (self.angles >= angle_start) & (self.angles <= angle_end)
        return self.ranges[mask]
    
    def get_min_distance(self, angle_start: float = -math.pi/4, 
                         angle_end: float = math.pi/4) -> float:
        """获取指定角度范围内的最小距离"""
        points = self.get_points_in_range(angle_start, angle_end)
        valid = points[(points > self.range_min) & (points < self.range_max)]
        return float(np.min(valid)) if len(valid) > 0 else float('inf')
    
    def get_obstacles(self, threshold: float = 0.5) -> List[dict]:
        """检测障碍物（简单聚类）"""
        obstacles = []
        valid_mask = (self.ranges > self.range_min) & (self.ranges < self.range_max)
        
        # 转换为笛卡尔坐标
        x = self.ranges[valid_mask] * np.cos(self.angles[valid_mask])
        y = self.ranges[valid_mask] * np.sin(self.angles[valid_mask])
        
        # 简单障碍物检测（连续点）
        i = 0
        while i < len(x):
            if self.ranges[valid_mask][i] < threshold:
                # 找到障碍物起始
                start_idx = i
                while i < len(x) and self.ranges[valid_mask][i] < threshold:
                    i += 1
                end_idx = i
                
                # 计算障碍物属性
                obs_x = np.mean(x[start_idx:end_idx])
                obs_y = np.mean(y[start_idx:end_idx])
                obs_dist = math.sqrt(obs_x**2 + obs_y**2)
                obs_angle = math.atan2(obs_y, obs_x)
                obs_width = math.sqrt((x[end_idx-1] - x[start_idx])**2 + 
                                      (y[end_idx-1] - y[start_idx])**2)
                
                obstacles.append({
                    "x": obs_x,
                    "y": obs_y,
                    "distance": obs_dist,
                    "angle": obs_angle,
                    "width": obs_width
                })
            else:
                i += 1
        
        return obstacles


class LidarNode:
    """
    激光雷达节点
    - 订阅 LaserScan 消息
    - 发布 lidar/scan 事件
    """
    
    def __init__(self, config, event_bus: EventBus):
        self.config = config
        self.event_bus = event_bus
        self._running = False
        self._node: Optional[Node] = None
        self._sub = None
        
        # 模拟模式
        self._simulation_mode = not ROS_AVAILABLE
        
        if not ROS_AVAILABLE:
            logger.warning("ROS 2 不可用，进入模拟模式")
    
    async def start(self):
        """启动雷达节点"""
        if self._running:
            return
        
        self._running = True
        logger.info("Starting lidar node...")
        
        if self._simulation_mode:
            await self._run_simulation()
        else:
            await self._run_ros()
    
    async def _run_ros(self):
        """ROS 订阅模式"""
        if not ROS_AVAILABLE:
            return
        
        # 创建 ROS 节点（如果 camera_node 已初始化，则使用已有上下文）
        if not rclpy.ok():
            rclpy.init(args=None)
        
        self._node = rclpy.create_node("lidar_node")
        
        self._sub = self._node.create_subscription(
            LaserScan,
            self.config.scan_topic,
            self._on_scan,
            10
        )
        
        logger.info(f"Subscribed to: {self.config.scan_topic}")
        
        while self._running and rclpy.ok():
            rclpy.spin_once(self._node, timeout_sec=0.01)
            await asyncio.sleep(0.001)
        
        self._cleanup_ros()
    
    def _on_scan(self, msg: LaserScan):
        """激光雷达回调"""
        try:
            # 转换为 numpy 数组
            ranges = np.array(msg.ranges, dtype=np.float32)
            
            # 生成角度数组
            num_points = len(ranges)
            angles = np.linspace(msg.angle_min, msg.angle_max, num_points)
            
            # 处理强度（如果有）
            intensities = None
            if len(msg.intensities) == num_points:
                intensities = np.array(msg.intensities, dtype=np.float32)
            
            scan = LidarScan(
                ranges=ranges,
                angles=angles,
                intensities=intensities,
                timestamp=msg.header.stamp.sec + msg.header.stamp.nanosec * 1e-9,
                frame_id=msg.header.frame_id,
                angle_min=msg.angle_min,
                angle_max=msg.angle_max,
                angle_increment=msg.angle_increment,
                range_min=msg.range_min,
                range_max=msg.range_max
            )
            
            # 发布事件
            self.event_bus.publish("lidar/scan", scan)
            logger.debug(f"Published scan: {len(ranges)} points")
            
        except Exception as e:
            logger.error(f"雷达数据处理失败: {e}")
    
    async def _run_simulation(self):
        """模拟模式：生成测试数据"""
        logger.info("Running in simulation mode")
        
        scan_count = 0
        num_points = 360  # 1度一个点
        
        while self._running:
            # 生成模拟扫描数据（前方有障碍物）
            angles = np.linspace(-math.pi, math.pi, num_points)
            ranges = np.full(num_points, 10.0, dtype=np.float32)  # 默认 10m
            
            # 在前方添加障碍物
            front_start = num_points // 2 - 30
            front_end = num_points // 2 + 30
            ranges[front_start:front_end] = 1.5 + np.random.normal(0, 0.05, 60)
            
            # 添加一些随机噪声
            ranges += np.random.normal(0, 0.02, num_points)
            
            # 处理无效值
            ranges[ranges < 0.1] = float('inf')
            
            scan = LidarScan(
                ranges=ranges,
                angles=angles,
                timestamp=scan_count * 0.1,
                frame_id="laser_sim",
                angle_min=-math.pi,
                angle_max=math.pi,
                angle_increment=2 * math.pi / num_points,
                range_min=0.1,
                range_max=20.0
            )
            
            self.event_bus.publish("lidar/scan", scan)
            scan_count += 1
            
            if scan_count % 10 == 0:
                logger.debug(f"Simulated {scan_count} scans")
            
            await asyncio.sleep(0.1)  # 10Hz
    
    async def stop(self):
        """停止雷达节点"""
        self._running = False
        logger.info("Lidar node stopped")
        
        if not self._simulation_mode:
            self._cleanup_ros()
    
    def _cleanup_ros(self):
        """清理 ROS 资源"""
        if self._node:
            self._node.destroy_node()
            self._node = None
