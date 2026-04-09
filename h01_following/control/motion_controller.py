"""
control/motion_controller.py
运动控制模块：将目标位姿转化为差速底盘速度指令。
使用 PID 控制，角度优先策略：先对准再前进。
"""

from __future__ import annotations
import math
import time
import asyncio
from dataclasses import dataclass

try:
    from rclpy.node import Node
    from geometry_msgs.msg import Twist
    ROS_AVAILABLE = True
except ImportError:
    ROS_AVAILABLE = False
    Node = object
    Twist = None

from config.settings import MotionConfig
from utils.event_bus import EventBus
from utils.logger import get_logger


class PIDController:
    def __init__(self, kp: float, ki: float = 0.0, kd: float = 0.0,
                 limit: float = float("inf")):
        self.kp, self.ki, self.kd = kp, ki, kd
        self.limit = limit
        self._integral = 0.0
        self._prev_error = 0.0
        self._prev_time = time.time()

    def compute(self, error: float) -> float:
        now = time.time()
        dt = max(now - self._prev_time, 1e-4)
        self._integral += error * dt
        derivative = (error - self._prev_error) / dt
        output = self.kp * error + self.ki * self._integral + self.kd * derivative
        self._prev_error = error
        self._prev_time = now
        return max(-self.limit, min(self.limit, output))

    def reset(self) -> None:
        self._integral = 0.0
        self._prev_error = 0.0


@dataclass
class Twist:
    """简化版 Twist 消息"""
    linear_x: float = 0.0
    angular_z: float = 0.0


class MotionController:
    """
    运动控制器（非 ROS 版本）
    输入事件: target_pose, obstacle_command, follow_command
    输出:     control/cmd_vel (EventBus 事件)
    """

    def __init__(self, config: MotionConfig, bus: EventBus):
        self._config = config
        self._bus = bus
        self._logger = get_logger("MotionController")

        self._following_active = False
        self._obstacle_override = False

        self._pid_angular = PIDController(
            kp=config.kp_angular, limit=config.max_angular_vel
        )
        self._pid_linear = PIDController(
            kp=config.kp_linear, limit=config.max_linear_vel
        )

        bus.subscribe("follow_command", self._on_follow_command)

        self._latest_pose = None
        self._running = False

    async def start(self):
        """启动控制器"""
        self._running = True
        self._logger.info("运动控制器已启动")
        # 启动控制循环
        while self._running:
            self._control_loop()
            await asyncio.sleep(0.05)  # 20Hz

    async def stop(self):
        """停止控制器"""
        self._running = False
        self._publish_zero()
        self._logger.info("运动控制器已停止")

    async def execute(self, data):
        """执行速度指令（兼容接口）"""
        pass

    # ── 公开回调 ───────────────────────────────────────────────
    def on_target_pose(self, payload) -> None:
        self._latest_pose = payload

    def on_obstacle_command(self, payload: dict) -> None:
        """避障模块发出的紧急指令。"""
        self._obstacle_override = payload.get("stop", False)
        if self._obstacle_override:
            self._publish_zero()

    def _on_follow_command(self, payload: dict) -> None:
        self._following_active = payload.get("active", False)
        if not self._following_active:
            self._publish_zero()
            self._pid_angular.reset()
            self._pid_linear.reset()

    # ── 控制循环 ────────────────────────────────────────────────
    def _control_loop(self) -> None:
        if not self._following_active or self._obstacle_override:
            return
        if self._latest_pose is None:
            return

        pose = self._latest_pose
        dist = pose.distance if hasattr(pose, 'distance') else pose.get('distance', 0)
        angle = pose.angle if hasattr(pose, 'angle') else pose.get('angle', 0)
        target_dist = self._config.follow_distance
        dist_tol = self._config.distance_tol
        angle_tol = self._config.angle_tol

        twist = Twist()

        # 角度偏差优先：先转向对准目标
        if abs(angle) > angle_tol:
            twist.angular_z = self._pid_angular.compute(angle)
            # 转向时线速度减小
            if abs(angle) > 0.4:
                self._publish(twist)
                return

        # 距离控制
        dist_error = dist - target_dist
        if abs(dist_error) > dist_tol:
            twist.linear_x = self._pid_linear.compute(dist_error)

        self._publish(twist)

    # ── 底层发布 ────────────────────────────────────────────────
    def _publish(self, twist: Twist) -> None:
        # 安全限幅
        linear_x = max(
            -self._config.max_linear_vel,
            min(self._config.max_linear_vel, twist.linear_x)
        )
        angular_z = max(
            -self._config.max_angular_vel,
            min(self._config.max_angular_vel, twist.angular_z)
        )
        # 通过 EventBus 发布速度指令
        self._bus.publish("control/cmd_vel", {
            "linear_x": linear_x,
            "angular_z": angular_z
        })

    def _publish_zero(self) -> None:
        self._bus.publish("control/cmd_vel", {"linear_x": 0.0, "angular_z": 0.0})


# ROS 版本（如果 ROS 可用）
if ROS_AVAILABLE:
    class MotionControllerROS(Node):
        """
        运动控制器（ROS 版本）
        输入事件: target_pose, obstacle_command, follow_command
        输出:     /cmd_vel (ROS topic)
        """

        def __init__(self, config: MotionConfig, bus: EventBus):
            super().__init__("motion_controller_node")
            self._config = config
            self._bus = bus
            self._logger = get_logger("MotionControllerROS")

            from geometry_msgs.msg import Twist as RosTwist
            self._pub = self.create_publisher(RosTwist, config.cmd_vel_topic, 10)
            self._following_active = False
            self._obstacle_override = False

            self._pid_angular = PIDController(
                kp=config.kp_angular, limit=config.max_angular_vel
            )
            self._pid_linear = PIDController(
                kp=config.kp_linear, limit=config.max_linear_vel
            )

            bus.subscribe("follow_command", self._on_follow_command)

            # 控制循环定时器（20Hz）
            self.create_timer(0.05, self._control_loop)
            self._latest_pose = None

        # ── 公开回调 ───────────────────────────────────────────────
        def on_target_pose(self, payload) -> None:
            self._latest_pose = payload

        def on_obstacle_command(self, payload: dict) -> None:
            """避障模块发出的紧急指令。"""
            self._obstacle_override = payload.get("stop", False)
            if self._obstacle_override:
                self._publish_zero()

        def _on_follow_command(self, payload: dict) -> None:
            self._following_active = payload.get("active", False)
            if not self._following_active:
                self._publish_zero()
                self._pid_angular.reset()
                self._pid_linear.reset()

        # ── 控制循环 ────────────────────────────────────────────────
        def _control_loop(self) -> None:
            if not self._following_active or self._obstacle_override:
                return
            if self._latest_pose is None:
                return

            from geometry_msgs.msg import Twist as RosTwist
            pose = self._latest_pose
            dist = pose.distance if hasattr(pose, 'distance') else pose.get('distance', 0)
            angle = pose.angle if hasattr(pose, 'angle') else pose.get('angle', 0)
            target_dist = self._config.follow_distance
            dist_tol = self._config.distance_tol
            angle_tol = self._config.angle_tol

            twist = RosTwist()

            # 角度偏差优先：先转向对准目标
            if abs(angle) > angle_tol:
                twist.angular.z = self._pid_angular.compute(angle)
                # 转向时线速度减小
                if abs(angle) > 0.4:
                    self._publish(twist)
                    return

            # 距离控制
            dist_error = dist - target_dist
            if abs(dist_error) > dist_tol:
                twist.linear.x = self._pid_linear.compute(dist_error)

            self._publish(twist)

        # ── 底层发布 ────────────────────────────────────────────────
        def _publish(self, twist) -> None:
            # 安全限幅
            twist.linear.x = max(
                -self._config.max_linear_vel,
                min(self._config.max_linear_vel, twist.linear.x)
            )
            twist.angular.z = max(
                -self._config.max_angular_vel,
                min(self._config.max_angular_vel, twist.angular.z)
            )
            self._pub.publish(twist)

        def _publish_zero(self) -> None:
            from geometry_msgs.msg import Twist as RosTwist
            self._pub.publish(RosTwist())

        def stop(self) -> None:
            self._publish_zero()
            self._logger.info("底盘已停止")
