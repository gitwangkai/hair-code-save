"""
tracking/tracker.py
目标追踪模块：基于 ByteTrack 实现多目标关联，输出稳定 ID 的追踪结果。
输入: human_detections
输出: tracked_targets
"""

from __future__ import annotations
import time
import numpy as np
from dataclasses import dataclass, field
from typing import List, Dict, Optional

from config.settings import TrackingConfig
from utils.event_bus import EventBus
from utils.logger import get_logger


@dataclass
class TrackedTarget:
    track_id: int
    bbox: np.ndarray          # [x1, y1, x2, y2]
    confidence: float
    keypoints: Optional[np.ndarray]
    age: int                  # 连续追踪帧数
    last_seen: float = field(default_factory=time.time)
    is_confirmed: bool = False


class ByteTracker:
    """ByteTracker 别名，兼容 main.py 接口"""
    
    def __init__(self, config, event_bus):
        self._tracker = HumanTracker(config, event_bus)
        self._config = config
        self._bus = event_bus
        self._running = False
    
    async def start(self):
        """启动跟踪器"""
        self._running = True
        # 订阅检测事件
        self._bus.subscribe("detection/detected", self._on_detection)
    
    async def stop(self):
        """停止跟踪器"""
        self._running = False
    
    def _on_detection(self, data):
        """处理检测结果"""
        self._tracker.on_detections(data)
    
    async def update(self, data):
        """更新跟踪（兼容接口）"""
        self._tracker.on_detections(data)


class HumanTracker:
    """
    输入事件: human_detections
    输出事件: tracked_targets -> List[TrackedTarget]
             target_lost     -> track_id (目标丢失时)
    """

    def __init__(self, config: TrackingConfig, bus: EventBus):
        self._config = config
        self._bus = bus
        self._logger = get_logger("HumanTracker")
        self._tracker = self._init_tracker()
        self._next_id = 1
        # 简易 KF 状态存储（若无 bytetrack 库则降级）
        self._tracks: Dict[int, TrackedTarget] = {}

    # ── 公开回调 ───────────────────────────────────────────────
    def on_detections(self, payload: dict) -> None:
        detections = payload["detections"]
        stamp = payload["stamp"]

        if self._tracker is not None:
            targets = self._bytetrack_update(detections)
        else:
            targets = self._simple_iou_update(detections)

        self._cleanup_lost_tracks()

        if targets:
            self._bus.publish("tracked_targets", {
                "targets": targets,
                "stamp": stamp,
            })

    # ── ByteTrack 接口 ─────────────────────────────────────────
    def _init_tracker(self):
        try:
            from bytetracker import BYTETracker
            from types import SimpleNamespace
            args = SimpleNamespace(
                track_thresh=self._config.iou_threshold,
                track_buffer=self._config.max_age,
                match_thresh=self._config.iou_threshold,
                mot20=False,
            )
            self._logger.info("ByteTracker 初始化成功")
            return BYTETracker(args)
        except ImportError:
            self._logger.warning("bytetracker 未安装，降级为简易 IoU 追踪")
            return None

    def _bytetrack_update(self, detections) -> List[TrackedTarget]:
        dets = np.array([
            [*d.bbox, d.confidence] for d in detections
        ], dtype=np.float32) if detections else np.empty((0, 5))

        online_targets = self._tracker.update(dets, [480, 640], [480, 640])
        targets = []
        for t in online_targets:
            tid = int(t.track_id)
            bbox = np.array(t.tlbr, dtype=np.float32)
            track = TrackedTarget(
                track_id=tid,
                bbox=bbox,
                confidence=float(t.score),
                keypoints=None,
                age=int(t.tracklet_len),
                is_confirmed=t.tracklet_len >= self._config.min_hits,
            )
            self._tracks[tid] = track
            targets.append(track)
        return [t for t in targets if t.is_confirmed]

    def _simple_iou_update(self, detections) -> List[TrackedTarget]:
        """无 ByteTrack 时的简易 IoU 关联降级方案。"""
        if not detections:
            for tid in list(self._tracks):
                self._tracks[tid].age -= 1
            return list(self._tracks.values())

        unmatched_det = list(range(len(detections)))
        updated = {}

        for tid, track in self._tracks.items():
            best_iou, best_i = 0.0, -1
            for i in unmatched_det:
                iou = self._iou(track.bbox, detections[i].bbox)
                if iou > best_iou:
                    best_iou, best_i = iou, i
            if best_iou >= self._config.iou_threshold:
                d = detections[best_i]
                track.bbox = d.bbox
                track.confidence = d.confidence
                track.keypoints = d.keypoints
                track.age += 1
                track.last_seen = time.time()
                track.is_confirmed = track.age >= self._config.min_hits
                updated[tid] = track
                unmatched_det.remove(best_i)

        for i in unmatched_det:
            d = detections[i]
            tid = self._next_id
            self._next_id += 1
            updated[tid] = TrackedTarget(
                track_id=tid, bbox=d.bbox,
                confidence=d.confidence, keypoints=d.keypoints, age=1,
            )

        self._tracks = updated
        return [t for t in self._tracks.values() if t.is_confirmed]

    def _cleanup_lost_tracks(self) -> None:
        now = time.time()
        lost = [
            tid for tid, t in self._tracks.items()
            if now - t.last_seen > 1.0
        ]
        for tid in lost:
            self._bus.publish("target_lost", tid)
            del self._tracks[tid]
            self._logger.debug(f"目标 {tid} 已丢失并清除")

    @staticmethod
    def _iou(a: np.ndarray, b: np.ndarray) -> float:
        ix1, iy1 = max(a[0], b[0]), max(a[1], b[1])
        ix2, iy2 = min(a[2], b[2]), min(a[3], b[3])
        inter = max(0, ix2 - ix1) * max(0, iy2 - iy1)
        if inter == 0:
            return 0.0
        area_a = (a[2]-a[0]) * (a[3]-a[1])
        area_b = (b[2]-b[0]) * (b[3]-b[1])
        return inter / (area_a + area_b - inter)
