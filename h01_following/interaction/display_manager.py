"""
interaction/display_manager.py
屏幕显示模块：渲染当前状态和目标信息到 13.3 寸触摸屏。
"""

from __future__ import annotations
import time
import numpy as np
from config.settings import DisplayConfig
from utils.event_bus import EventBus
from utils.logger import get_logger
from control.state_machine import State


_STATE_LABELS = {
    State.IDLE:          ("待机中", (120, 120, 120)),
    State.SEARCHING:     ("搜索目标...", (255, 180, 0)),
    State.FOLLOWING:     ("正在跟随", (0, 200, 80)),
    State.OBSTACLE_STOP: ("障碍物停止", (220, 60, 60)),
    State.LOST:          ("目标丢失", (255, 100, 0)),
    State.CHARGING:      ("返回充电", (0, 160, 255)),
}


class DisplayManager:
    def __init__(self, config: DisplayConfig, bus: EventBus):
        self._config = config
        self._bus = bus
        self._logger = get_logger("DisplayManager")
        self._current_state = State.IDLE
        self._target_info = {"distance": 0.0, "angle": 0.0}
        self._running = False

    async def start(self):
        """启动显示管理器"""
        self._running = True
        self._bus.subscribe("state_changed", self.on_state_changed)
        self._bus.subscribe("target_pose", self.on_target_pose)

    async def stop(self):
        """停止显示管理器"""
        self._running = False

    async def show_alert(self, data):
        """显示告警（兼容接口）"""
        message = data.get("message", "")
        self._logger.info(f"[屏幕告警] {message}")

    async def update_status(self, data):
        """更新状态显示（兼容接口）"""
        self._render()

    def on_state_changed(self, payload: dict) -> None:
        self._current_state = payload["to"]
        self._render()

    def on_target_pose(self, pose) -> None:
        self._target_info = {
            "distance": pose.distance,
            "angle": math.degrees(pose.angle),
        }
        if self._config.show_debug:
            self._render()

    def _render(self) -> None:
        if not self._config.enabled:
            return
        label, color = _STATE_LABELS.get(
            self._current_state, ("未知状态", (128, 128, 128))
        )
        dist = self._target_info["distance"]
        angle = self._target_info["angle"]
        self._logger.info(
            f"[屏幕] 状态={label}  距离={dist:.2f}m  角度={angle:.1f}°"
        )
        # 实际渲染：通过 ROS topic 发布 OpenCV 图像到屏幕节点
        # self._bus.publish("display_frame", self._draw_frame(label, color, dist, angle))

    def _draw_frame(self, label, color, dist, angle) -> np.ndarray:
        try:
            import cv2
            frame = np.zeros((self._config.height, self._config.width, 3), dtype=np.uint8)
            cv2.putText(frame, label, (100, 200), cv2.FONT_HERSHEY_SIMPLEX,
                        3, color, 4, cv2.LINE_AA)
            cv2.putText(frame, f"距离: {dist:.2f} m", (100, 350),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2)
            cv2.putText(frame, f"角度: {angle:.1f}°", (100, 450),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2)
            return frame
        except ImportError:
            return np.zeros((100, 100, 3), dtype=np.uint8)


import math  # noqa: E402
