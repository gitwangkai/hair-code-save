"""
perception/camera_node.py
RGBD 相机 ROS 订阅节点
"""

import asyncio
from dataclasses import dataclass
from typing import Optional, Callable
import numpy as np

# cv_bridge 可能因 numpy 版本不兼容而失败，先尝试导入
try:
    from cv_bridge import CvBridge
    CV_BRIDGE_AVAILABLE = True
except Exception:
    CV_BRIDGE_AVAILABLE = False

try:
    import rclpy
    from rclpy.node import Node
    from sensor_msgs.msg import Image, CameraInfo
    ROS_AVAILABLE = True
except ImportError:
    ROS_AVAILABLE = False

from utils.event_bus import EventBus
from utils.logger import get_logger

logger = get_logger("camera_node")


@dataclass
class FrameData:
    """帧数据结构"""
    rgb: np.ndarray           # RGB 图像 (H, W, 3)
    depth: Optional[np.ndarray] = None  # 深度图 (H, W)
    timestamp: float = 0.0    # 时间戳
    frame_id: str = ""        # 坐标系 ID
    
    # 相机内参
    fx: float = 0.0
    fy: float = 0.0
    cx: float = 0.0
    cy: float = 0.0


class CameraNode:
    """
    RGBD 相机节点
    - 订阅 RGB 和深度图像
    - 同步时间戳
    - 发布 raw_rgb_frame 事件
    """
    
    def __init__(self, config, event_bus: EventBus):
        self.config = config
        self.event_bus = event_bus
        self._running = False
        self._bridge: Optional[CvBridge] = None
        self._node: Optional[Node] = None
        self._rgb_sub = None
        self._depth_sub = None
        self._info_sub = None
        
        # 帧缓冲（用于同步）
        self._latest_rgb: Optional[FrameData] = None
        self._latest_depth: Optional[np.ndarray] = None
        self._camera_info: Optional[CameraInfo] = None
        
        # 模拟模式（无 ROS 时使用）
        self._simulation_mode = not ROS_AVAILABLE or not CV_BRIDGE_AVAILABLE
        
        if not ROS_AVAILABLE:
            logger.warning("ROS 2 不可用，进入模拟模式")
        elif not CV_BRIDGE_AVAILABLE:
            logger.warning("cv_bridge 不可用（numpy 版本不兼容），进入模拟模式")
    
    async def start(self):
        """启动相机节点"""
        if self._running:
            return
        
        self._running = True
        logger.info("Starting camera node...")
        
        if self._simulation_mode:
            # 模拟模式：生成测试图像
            await self._run_simulation()
        else:
            # ROS 模式
            await self._run_ros()
    
    async def _run_ros(self):
        """ROS 订阅模式"""
        if not ROS_AVAILABLE:
            return
        
        if CV_BRIDGE_AVAILABLE:
            self._bridge = CvBridge()
        
        # 创建 ROS 节点
        rclpy.init(args=None)
        self._node = rclpy.create_node("camera_node")
        
        # 订阅 RGB 图像
        self._rgb_sub = self._node.create_subscription(
            Image,
            self.config.rgb_topic,
            self._on_rgb,
            10
        )
        
        # 订阅深度图像
        self._depth_sub = self._node.create_subscription(
            Image,
            self.config.depth_topic,
            self._on_depth,
            10
        )
        
        # 订阅相机信息
        self._info_sub = self._node.create_subscription(
            CameraInfo,
            self.config.info_topic,
            self._on_camera_info,
            10
        )
        
        logger.info(f"Subscribed to: {self.config.rgb_topic}")
        logger.info(f"Subscribed to: {self.config.depth_topic}")
        
        # 在后台运行 ROS spin
        while self._running and rclpy.ok():
            rclpy.spin_once(self._node, timeout_sec=0.01)
            await asyncio.sleep(0.001)
        
        self._cleanup_ros()
    
    def _on_rgb(self, msg: Image):
        """RGB 图像回调"""
        try:
            cv_image = self._bridge.imgmsg_to_cv2(msg, "rgb8")
            
            self._latest_rgb = FrameData(
                rgb=cv_image,
                timestamp=msg.header.stamp.sec + msg.header.stamp.nanosec * 1e-9,
                frame_id=msg.header.frame_id
            )
            
            # 尝试同步深度图
            self._try_publish_frame()
            
        except Exception as e:
            logger.error(f"RGB 转换失败: {e}")
    
    def _on_depth(self, msg: Image):
        """深度图像回调"""
        try:
            # 深度图通常是 16UC1 格式 (mm)
            cv_image = self._bridge.imgmsg_to_cv2(msg, "16UC1")
            self._latest_depth = cv_image
            
        except Exception as e:
            logger.error(f"深度图转换失败: {e}")
    
    def _on_camera_info(self, msg: CameraInfo):
        """相机信息回调"""
        self._camera_info = msg
        
        # 更新内参
        if self._latest_rgb:
            self._latest_rgb.fx = msg.k[0]
            self._latest_rgb.fy = msg.k[4]
            self._latest_rgb.cx = msg.k[2]
            self._latest_rgb.cy = msg.k[5]
    
    def _try_publish_frame(self):
        """尝试发布同步后的帧"""
        if self._latest_rgb is None:
            return
        
        # 复制数据
        frame = FrameData(
            rgb=self._latest_rgb.rgb.copy(),
            timestamp=self._latest_rgb.timestamp,
            frame_id=self._latest_rgb.frame_id,
            fx=self._latest_rgb.fx,
            fy=self._latest_rgb.fy,
            cx=self._latest_rgb.cx,
            cy=self._latest_rgb.cy
        )
        
        # 附加深度图（如果有）
        if self._latest_depth is not None:
            frame.depth = self._latest_depth.copy()
        
        # 发布事件
        self.event_bus.publish("camera/raw_frame", frame)
        logger.debug(f"Published frame: {frame.frame_id}")
    
    async def _run_simulation(self):
        """模拟模式：生成测试图像"""
        logger.info("Running in simulation mode")
        
        frame_count = 0
        while self._running:
            # 生成随机测试图像
            rgb = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
            depth = np.random.randint(500, 3000, (480, 640), dtype=np.uint16)
            
            frame = FrameData(
                rgb=rgb,
                depth=depth,
                timestamp=frame_count / 30.0,
                frame_id="camera_sim",
                fx=600.0,
                fy=600.0,
                cx=320.0,
                cy=240.0
            )
            
            self.event_bus.publish("camera/raw_frame", frame)
            frame_count += 1
            
            if frame_count % 30 == 0:
                logger.debug(f"Simulated {frame_count} frames")
            
            await asyncio.sleep(1.0 / self.config.fps)
    
    async def stop(self):
        """停止相机节点"""
        self._running = False
        logger.info("Camera node stopped")
        
        if not self._simulation_mode:
            self._cleanup_ros()
    
    def _cleanup_ros(self):
        """清理 ROS 资源"""
        if self._node:
            self._node.destroy_node()
            self._node = None
        if ROS_AVAILABLE and rclpy.ok():
            rclpy.shutdown()
