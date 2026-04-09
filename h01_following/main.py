#!/usr/bin/env python3
"""
h01_following - 人体跟随主程序
组装模块 · 注册事件 · 启动执行器
"""

import asyncio
import signal
import sys
from dataclasses import dataclass
from typing import Optional

from config.settings import Settings, load_config
from perception.camera_node import CameraNode
from perception.lidar_node import LidarNode
from perception.detector import YOLODetector
from tracking.tracker import ByteTracker
from tracking.localizer import Localizer
from control.state_machine import StateMachine
from control.motion_controller import MotionController
from control.obstacle_avoidance import ObstacleAvoidance
from interaction.voice_manager import VoiceManager
from interaction.display_manager import DisplayManager
from utils.event_bus import EventBus
from utils.logger import get_logger

logger = get_logger("main")


@dataclass
class FollowingSystem:
    """人体跟随系统主类"""
    
    config: Settings
    event_bus: EventBus
    
    # 感知模块
    camera: Optional[CameraNode] = None
    lidar: Optional[LidarNode] = None
    detector: Optional[YOLODetector] = None
    
    # 跟踪模块
    tracker: Optional[ByteTracker] = None
    localizer: Optional[Localizer] = None
    
    # 控制模块
    state_machine: Optional[StateMachine] = None
    motion_controller: Optional[MotionController] = None
    obstacle_avoidance: Optional[ObstacleAvoidance] = None
    
    # 交互模块
    voice_manager: Optional[VoiceManager] = None
    display_manager: Optional[DisplayManager] = None
    
    _running: bool = False
    
    async def initialize(self):
        """初始化所有模块"""
        logger.info("Initializing following system...")
        
        # 初始化感知模块
        self.camera = CameraNode(self.config.camera, self.event_bus)
        self.lidar = LidarNode(self.config.lidar, self.event_bus)
        self.detector = YOLODetector(self.config.detector, self.event_bus)
        
        # 初始化跟踪模块
        self.tracker = ByteTracker(self.config.tracker, self.event_bus)
        self.localizer = Localizer(self.config.localizer, self.event_bus)
        
        # 初始化控制模块
        self.state_machine = StateMachine(self.config.state_machine, self.event_bus)
        self.motion_controller = MotionController(self.config.motion, self.event_bus)
        self.obstacle_avoidance = ObstacleAvoidance(self.config.obstacle, self.event_bus)
        
        # 初始化交互模块
        self.voice_manager = VoiceManager(self.config.voice, self.event_bus)
        self.display_manager = DisplayManager(self.config.display, self.event_bus)
        
        # 注册事件处理器
        self._register_events()
        
        logger.info("System initialization completed")
    
    def _register_events(self):
        """注册事件总线处理器"""
        # 感知 -> 跟踪
        self.event_bus.subscribe("detection/detected", self._on_detection)
        self.event_bus.subscribe("lidar/scan", self._on_lidar_scan)
        
        # 跟踪 -> 控制
        self.event_bus.subscribe("tracking/target", self._on_tracking_target)
        self.event_bus.subscribe("localization/position", self._on_position_update)
        
        # 控制 -> 执行
        self.event_bus.subscribe("control/cmd_vel", self._on_cmd_vel)
        self.event_bus.subscribe("control/state", self._on_state_change)
        
        # 交互事件
        self.event_bus.subscribe("system/alert", self._on_system_alert)
        self.event_bus.subscribe("system/status", self._on_status_update)
    
    async def _on_detection(self, data):
        """处理检测结果"""
        if self.tracker:
            await self.tracker.update(data)
    
    async def _on_lidar_scan(self, data):
        """处理雷达扫描数据"""
        if self.obstacle_avoidance:
            await self.obstacle_avoidance.update_scan(data)
    
    async def _on_tracking_target(self, data):
        """处理跟踪目标"""
        if self.localizer:
            await self.localizer.update_target(data)
    
    async def _on_position_update(self, data):
        """处理位置更新"""
        if self.state_machine:
            await self.state_machine.update_position(data)
    
    async def _on_cmd_vel(self, data):
        """处理速度指令"""
        if self.motion_controller:
            await self.motion_controller.execute(data)
    
    async def _on_state_change(self, data):
        """处理状态变更"""
        if self.voice_manager:
            await self.voice_manager.announce_state(data)
    
    async def _on_system_alert(self, data):
        """处理系统告警"""
        if self.voice_manager:
            await self.voice_manager.speak_alert(data)
        if self.display_manager:
            await self.display_manager.show_alert(data)
    
    async def _on_status_update(self, data):
        """处理状态更新"""
        if self.display_manager:
            await self.display_manager.update_status(data)
    
    async def start(self):
        """启动系统"""
        self._running = True
        logger.info("Starting following system...")
        
        # 启动所有模块
        tasks = [
            asyncio.create_task(self.camera.start()),
            asyncio.create_task(self.lidar.start()),
            asyncio.create_task(self.detector.start()),
            asyncio.create_task(self.tracker.start()),
            asyncio.create_task(self.localizer.start()),
            asyncio.create_task(self.state_machine.start()),
            asyncio.create_task(self.motion_controller.start()),
            asyncio.create_task(self.obstacle_avoidance.start()),
            asyncio.create_task(self.voice_manager.start()),
            asyncio.create_task(self.display_manager.start()),
        ]
        
        await asyncio.gather(*tasks)
    
    async def stop(self):
        """停止系统"""
        self._running = False
        logger.info("Stopping following system...")
        
        # 停止所有模块
        if self.camera:
            await self.camera.stop()
        if self.lidar:
            await self.lidar.stop()
        if self.detector:
            await self.detector.stop()
        if self.tracker:
            await self.tracker.stop()
        if self.localizer:
            await self.localizer.stop()
        if self.state_machine:
            await self.state_machine.stop()
        if self.motion_controller:
            await self.motion_controller.stop()
        if self.obstacle_avoidance:
            await self.obstacle_avoidance.stop()
        if self.voice_manager:
            await self.voice_manager.stop()
        if self.display_manager:
            await self.display_manager.stop()
        
        logger.info("System stopped")


async def main():
    """主入口"""
    # 加载配置
    config = load_config("config/config.yaml")
    
    # 创建事件总线
    event_bus = EventBus()
    
    # 创建系统
    system = FollowingSystem(config, event_bus)
    
    # 信号处理
    def signal_handler(sig, frame):
        logger.info("Received shutdown signal")
        asyncio.create_task(system.stop())
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        # 初始化并启动
        await system.initialize()
        await system.start()
    except Exception as e:
        logger.error(f"System error: {e}")
        await system.stop()
        raise


if __name__ == "__main__":
    asyncio.run(main())
