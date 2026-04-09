"""
tracking/reid.py
目标重识别模块：目标消失后重新出现时，判断是否为同一人。
使用轻量级外观特征（颜色直方图 + 骨骼特征）比对，无需深度学习模型。
如有条件可替换为 OSNet / FastReID ONNX 模型。
"""

from __future__ import annotations
import time
import numpy as np
from dataclasses import dataclass, field
from typing import Optional, List
import cv2

from utils.logger import get_logger


@dataclass
class AppearanceFeature:
    track_id: int
    color_hist: np.ndarray        # HSV 颜色直方图 (上半身)
    keypoint_ratio: Optional[float]  # 肩宽/身高比
    bbox_aspect: float            # 宽高比
    last_seen: float = field(default_factory=time.time)


class ReIDManager:
    """
    当追踪器报告 target_lost 后，保存外观特征库。
    新目标出现时，与特征库比对，若相似度超过阈值则复用旧 ID。

    使用方式：
        reid = ReIDManager(threshold=0.6, max_age=10.0)
        # 目标消失时保存
        reid.save(track_id, frame, bbox, keypoints)
        # 新检测到时查询
        matched_id = reid.query(frame, bbox, keypoints)
    """

    def __init__(self, threshold: float = 0.6, max_age: float = 10.0):
        self._threshold = threshold
        self._max_age = max_age          # 特征保留时间(秒)
        self._gallery: dict[int, AppearanceFeature] = {}
        self._logger = get_logger("ReIDManager")

    # ── 公开接口 ───────────────────────────────────────────────
    def save(
        self,
        track_id: int,
        frame: np.ndarray,
        bbox: np.ndarray,
        keypoints: Optional[np.ndarray] = None,
    ) -> None:
        """目标丢失时调用，保存外观特征到图库。"""
        feat = self._extract(frame, bbox, keypoints)
        if feat is not None:
            feat.track_id = track_id
            self._gallery[track_id] = feat
            self._logger.debug(f"ReID 保存特征 ID={track_id}")

    def query(
        self,
        frame: np.ndarray,
        bbox: np.ndarray,
        keypoints: Optional[np.ndarray] = None,
    ) -> Optional[int]:
        """
        新目标出现时调用。
        返回匹配的旧 track_id，或 None（视为全新目标）。
        """
        self._purge_old()
        if not self._gallery:
            return None

        feat = self._extract(frame, bbox, keypoints)
        if feat is None:
            return None

        best_id, best_score = None, 0.0
        for tid, gal_feat in self._gallery.items():
            score = self._similarity(feat, gal_feat)
            if score > best_score:
                best_score, best_id = score, tid

        if best_score >= self._threshold:
            self._logger.info(f"ReID 命中 ID={best_id} score={best_score:.3f}")
            del self._gallery[best_id]   # 匹配后从图库移除
            return best_id

        return None

    def remove(self, track_id: int) -> None:
        self._gallery.pop(track_id, None)

    # ── 特征提取 ───────────────────────────────────────────────
    def _extract(
        self,
        frame: np.ndarray,
        bbox: np.ndarray,
        keypoints: Optional[np.ndarray],
    ) -> Optional[AppearanceFeature]:
        x1, y1, x2, y2 = [int(v) for v in bbox]
        h, w = frame.shape[:2]
        x1, y1 = max(0, x1), max(0, y1)
        x2, y2 = min(w, x2), min(h, y2)
        if x2 <= x1 or y2 <= y1:
            return None

        crop = frame[y1:y2, x1:x2]
        # 只取上半身（更稳定）
        mid_y = crop.shape[0] // 2
        upper = crop[:mid_y]
        if upper.size == 0:
            return None

        # HSV 颜色直方图
        hsv = cv2.cvtColor(upper, cv2.COLOR_BGR2HSV)
        hist = cv2.calcHist([hsv], [0, 1], None, [18, 8], [0, 180, 0, 256])
        hist = cv2.normalize(hist, hist).flatten()

        # 骨骼比例（肩宽/身高）
        kp_ratio = None
        if keypoints is not None and len(keypoints) >= 7:
            l_shoulder = keypoints[5][:2]   # COCO index 5
            r_shoulder = keypoints[6][:2]   # COCO index 6
            hip_y = keypoints[11][1] if len(keypoints) > 11 else y2
            shoulder_w = float(np.linalg.norm(l_shoulder - r_shoulder))
            body_h = float(abs(hip_y - (y1 + y2) / 2)) + 1e-6
            kp_ratio = shoulder_w / body_h

        bbox_w, bbox_h = x2 - x1, y2 - y1
        aspect = bbox_w / max(bbox_h, 1)

        return AppearanceFeature(
            track_id=-1,
            color_hist=hist,
            keypoint_ratio=kp_ratio,
            bbox_aspect=aspect,
        )

    def _similarity(self, a: AppearanceFeature, b: AppearanceFeature) -> float:
        """综合颜色直方图相似度 + 骨骼比例相似度。"""
        # Bhattacharyya 距离 → 相似度
        hist_sim = float(cv2.compareHist(
            a.color_hist.reshape(-1, 1).astype(np.float32),
            b.color_hist.reshape(-1, 1).astype(np.float32),
            cv2.HISTCMP_BHATTACHARYYA,
        ))
        hist_score = 1.0 - hist_sim    # [0,1], 越大越像

        # 骨骼比例相似度
        kp_score = 0.5   # 无骨骼时给中性分
        if a.keypoint_ratio is not None and b.keypoint_ratio is not None:
            diff = abs(a.keypoint_ratio - b.keypoint_ratio)
            kp_score = max(0.0, 1.0 - diff * 2)

        # 宽高比惩罚（差异过大直接降分）
        aspect_penalty = max(0.0, 1.0 - abs(a.bbox_aspect - b.bbox_aspect))

        return 0.6 * hist_score + 0.3 * kp_score + 0.1 * aspect_penalty

    def _purge_old(self) -> None:
        now = time.time()
        expired = [
            tid for tid, f in self._gallery.items()
            if now - f.last_seen > self._max_age
        ]
        for tid in expired:
            del self._gallery[tid]
            self._logger.debug(f"ReID 特征过期清除 ID={tid}")
