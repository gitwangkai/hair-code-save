"""
tracking/localizer.py
目标定位模块：将 2D 追踪框映射到 3D 坐标（相机系 → 机器人系）。
输入: tracked_targets + latest_depth
输出: target_pose -> TargetPose
"""

from __future__ import annotations
import time
import numpy as np
from dataclasses import dataclass
from typing import Optional, Dict

from config.settings import LocalizationConfig
from utils.event_bus import EventBus
from utils.logger import get_logger


@dataclass
class TargetPose:
    track_id: int
    distance: float      # 到目标的距离 (m)
    angle: float         # 相对机器人前向的角度 (rad), 左正右负
    x: float             # 目标在机器人坐标系中的 x (前向)
    y: float             # 目标在机器人坐标系中的 y (左向)
    timestamp: float


class Localizer:
    """Localizer 别名，兼容 main.py 接口"""
    
    def __init__(self, config, event_bus):
        self._localizer = TargetLocalizer(config, event_bus)
        self._config = config
        self._bus = event_bus
        self._running = False
    
    async def start(self):
        """启动定位器"""
        self._running = True
        # 订阅跟踪事件
        self._bus.subscribe("tracking/target", self._on_target)
    
    async def stop(self):
        """停止定位器"""
        self._running = False
    
    def _on_target(self, data):
        """处理跟踪目标"""
        self._localizer.on_tracked_targets(data)
    
    async def update_target(self, data):
        """更新目标（兼容接口）"""
        self._localizer.on_tracked_targets(data)


class TargetLocalizer:
    """
    输入事件: tracked_targets, latest_depth
    输出事件: target_pose -> TargetPose
    """

    def __init__(self, config: LocalizationConfig, bus: EventBus):
        self._config = config
        self._bus = bus
        self._logger = get_logger("TargetLocalizer")
        self._latest_depth: Optional[dict] = None
        self._camera_info: Optional[dict] = None
        # 平滑滤波历史值
        self._smoothed: Dict[int, TargetPose] = {}

        # 订阅深度帧和相机参数更新
        bus.subscribe("latest_depth",      self._cache_depth)
        bus.subscribe("raw_rgb_frame",     self._cache_camera_info)

    # ── 公开回调 ───────────────────────────────────────────────
    def on_tracked_targets(self, payload: dict) -> None:
        if self._latest_depth is None or self._camera_info is None:
            return
        targets = payload["targets"]
        depth_map = self._latest_depth["depth"]

        # 选取主跟随目标（最近的已确认目标）
        best = self._select_primary(targets, depth_map)
        if best is None:
            return

        self._bus.publish("target_pose", best)

    # ── 私有方法 ───────────────────────────────────────────────
    def _select_primary(self, targets, depth_map) -> Optional[TargetPose]:
        candidates = []
        for t in targets:
            pose = self._estimate_pose(t, depth_map)
            if pose is not None:
                candidates.append(pose)
        if not candidates:
            return None
        # 取距离最近的目标
        return min(candidates, key=lambda p: p.distance)

    def _estimate_pose(self, target, depth_map) -> Optional[TargetPose]:
        bbox = target.bbox
        cx = int((bbox[0] + bbox[2]) / 2)
        cy = int((bbox[1] + bbox[3]) / 2)

        # 在 bbox 中心区域采样深度，取中位数增强鲁棒性
        margin = 20
        x1 = max(0, cx - margin); x2 = min(depth_map.shape[1], cx + margin)
        y1 = max(0, cy - margin); y2 = min(depth_map.shape[0], cy + margin)
        patch = depth_map[y1:y2, x1:x2]
        valid = patch[(patch > 0.2) & (patch < 8.0)]
        if valid.size == 0:
            return None
        depth_val = float(np.median(valid))

        # 针孔相机模型：像素 → 3D
        fx = self._camera_info["fx"]
        fy = self._camera_info["fy"]
        cx_cam = self._camera_info["cx"]
        cy_cam = self._camera_info["cy"]
        X = (cx - cx_cam) * depth_val / fx
        Z = depth_val

        distance = float(np.sqrt(X**2 + Z**2))
        angle = float(np.arctan2(-X, Z))   # 右手系，左正

        # 低通滤波平滑
        alpha = self._config.smooth_alpha
        if target.track_id in self._smoothed:
            prev = self._smoothed[target.track_id]
            distance = alpha * distance + (1 - alpha) * prev.distance
            angle    = alpha * angle    + (1 - alpha) * prev.angle

        pose = TargetPose(
            track_id=target.track_id,
            distance=distance,
            angle=angle,
            x=Z, y=-X,
            timestamp=time.time(),
        )
        self._smoothed[target.track_id] = pose
        return pose

    def _cache_depth(self, payload: dict) -> None:
        self._latest_depth = payload

    def _cache_camera_info(self, payload: dict) -> None:
        if payload.get("camera_info"):
            self._camera_info = payload["camera_info"]
