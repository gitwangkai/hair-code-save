"""
perception/detector.py
人体检测模块：YOLO 推理，输出检测框 + 骨骼关键点。
只消费 raw_rgb_frame，只发布 human_detections，不关心追踪和控制。
"""

from __future__ import annotations
import time
import numpy as np
from dataclasses import dataclass, field
from typing import List, Optional

from config.settings import DetectionConfig
from utils.event_bus import EventBus
from utils.logger import get_logger


@dataclass
class Detection:
    bbox: np.ndarray          # [x1, y1, x2, y2]
    confidence: float
    keypoints: Optional[np.ndarray] = None   # (17, 3) COCO 格式
    timestamp: float = field(default_factory=time.time)


class YOLODetector:
    """YOLODetector 别名，兼容 main.py 接口"""
    
    def __init__(self, config, event_bus):
        self._detector = HumanDetector(config, event_bus)
        self._config = config
        self._bus = event_bus
        self._running = False
        # 从 localization config 获取 depth_scale
        self._depth_scale = 0.001
    
    async def start(self):
        """启动检测器"""
        self._running = True
        # 订阅相机帧
        self._bus.subscribe("camera/raw_frame", self._on_frame)
    
    async def stop(self):
        """停止检测器"""
        self._running = False
    
    def _on_frame(self, data):
        """处理相机帧"""
        # 转换 FrameData 为字典格式
        payload = {
            "frame": data.rgb,
            "stamp": data.timestamp
        }
        self._detector.on_rgb_frame(payload)
        
        # 同时发布深度帧
        if data.depth is not None:
            depth_payload = {
                "depth": data.depth * self._depth_scale,
                "stamp": data.timestamp
            }
            self._detector.on_depth_frame(depth_payload)


class HumanDetector:
    """
    输入事件: raw_rgb_frame
    输出事件: human_detections -> List[Detection]
    """

    def __init__(self, config: DetectionConfig, bus: EventBus):
        self._config = config
        self._bus = bus
        self._logger = get_logger("HumanDetector")
        self._model = self._load_model()
        self._frame_skip = 0        # 可按需跳帧降低 CPU

    # ── 公开回调（由 EventBus 调用）────────────────────────────
    def on_rgb_frame(self, payload: dict) -> None:
        self._frame_skip += 1
        if self._frame_skip % 2 != 0:   # 每 2 帧检测一次
            return
        frame = payload["frame"]
        stamp = payload["stamp"]
        detections = self._infer(frame)
        if detections:
            self._bus.publish("human_detections", {
                "detections": detections,
                "stamp": stamp,
                "frame_shape": frame.shape,
            })

    def on_depth_frame(self, payload: dict) -> None:
        # 深度帧暂存供定位器使用（通过 bus 中转）
        self._bus.publish("latest_depth", payload)

    # ── 私有方法 ───────────────────────────────────────────────
    def _load_model(self):
        """加载 ONNX 模型，支持 SNPE DSP 后端。"""
        try:
            import onnxruntime as ort
            providers = (
                ["SNPEExecutionProvider"] if self._config.use_dsp
                else ["CPUExecutionProvider"]
            )
            session = ort.InferenceSession(
                self._config.model_path, providers=providers
            )
            self._logger.info(f"模型加载成功: {self._config.model_path}")
            return session
        except Exception as e:
            self._logger.warning(f"模型加载失败，使用 Mock: {e}")
            return None

    def _infer(self, frame: np.ndarray) -> List[Detection]:
        if self._model is None:
            return self._mock_detection(frame)
        try:
            blob = self._preprocess(frame)
            outputs = self._model.run(None, {self._model.get_inputs()[0].name: blob})
            return self._postprocess(outputs, frame.shape)
        except Exception as e:
            self._logger.error(f"推理异常: {e}")
            return []

    def _preprocess(self, frame: np.ndarray) -> np.ndarray:
        import cv2
        size = self._config.input_size
        resized = cv2.resize(frame, (size, size))
        blob = resized.transpose(2, 0, 1)[np.newaxis].astype(np.float32) / 255.0
        return blob

    def _postprocess(self, outputs, frame_shape) -> List[Detection]:
        """解析 YOLOv8-pose 输出，过滤低置信度检测。"""
        detections = []
        h, w = frame_shape[:2]
        raw = outputs[0][0]               # shape: (num_det, 56) for pose
        for row in raw.T:
            conf = float(row[4])
            if conf < self._config.confidence_threshold:
                continue
            cx, cy, bw, bh = row[:4]
            x1 = int((cx - bw / 2) / self._config.input_size * w)
            y1 = int((cy - bh / 2) / self._config.input_size * h)
            x2 = int((cx + bw / 2) / self._config.input_size * w)
            y2 = int((cy + bh / 2) / self._config.input_size * h)
            kps = row[5:].reshape(17, 3) if len(row) > 5 else None
            detections.append(Detection(
                bbox=np.array([x1, y1, x2, y2]),
                confidence=conf,
                keypoints=kps,
            ))
        return detections

    def _mock_detection(self, frame: np.ndarray) -> List[Detection]:
        """单元测试 / 无模型时的 mock 输出。"""
        h, w = frame.shape[:2]
        return [Detection(
            bbox=np.array([w//4, h//4, w*3//4, h*3//4]),
            confidence=0.95,
        )]
