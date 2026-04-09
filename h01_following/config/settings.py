"""
config/settings.py
全局配置，所有模块从这里读取参数，避免硬编码。
"""

from dataclasses import dataclass, field
from pathlib import Path
import yaml


@dataclass
class CameraConfig:
    rgb_topic:   str   = "/camera/color/image_raw"
    depth_topic: str   = "/camera/depth/image_rect_raw"
    info_topic:  str   = "/camera/color/camera_info"
    fps:         int   = 30
    width:       int   = 640
    height:      int   = 480


@dataclass
class LidarConfig:
    scan_topic:  str   = "/scan"
    frame_id:    str   = "laser_frame"
    min_range:   float = 0.1
    max_range:   float = 20.0


@dataclass
class DetectionConfig:
    model_path:       str   = "models/yolov8n-pose.onnx"
    confidence_threshold: float = 0.5
    nms_threshold:    float = 0.45
    input_size:       int   = 640
    use_dsp:          bool  = True   # 启用 QCS8550 DSP 加速


@dataclass
class TrackingConfig:
    max_age:          int   = 30     # 目标消失多少帧后丢弃
    min_hits:         int   = 3      # 至少连续确认几帧才算有效目标
    iou_threshold:    float = 0.3
    reid_threshold:   float = 0.6    # 重识别相似度阈值


@dataclass
class LocalizationConfig:
    camera_frame:     str   = "camera_color_optical_frame"
    base_frame:       str   = "base_link"
    depth_scale:      float = 0.001  # mm → m
    smooth_alpha:     float = 0.3    # 低通滤波系数


@dataclass
class AvoidanceConfig:
    safety_radius:    float = 0.3    # 机器人外接圆半径(m)
    slow_distance:    float = 0.6    # 开始减速的障碍距离
    stop_distance:    float = 0.25   # 停止的障碍距离
    cliff_topic:      str   = "/cliff_detected"
    ultrasonic_topic: str   = "/ultrasonic/range"


@dataclass
class MotionConfig:
    cmd_vel_topic:    str   = "/cmd_vel"
    follow_distance:  float = 1.0    # 目标跟随距离(m)
    distance_tol:     float = 0.15   # 距离容差
    angle_tol:        float = 0.1    # 角度容差(rad)
    max_linear_vel:   float = 0.25   # 导航最大速度(m/s)
    max_angular_vel:  float = 0.8    # 最大角速度(rad/s)
    kp_linear:        float = 0.5    # 线速度 P 增益
    kp_angular:       float = 1.2    # 角速度 P 增益


@dataclass
class StateConfig:
    search_timeout:   float = 5.0    # 搜索目标超时(s)
    lost_timeout:     float = 3.0    # 目标丢失超时(s)
    reacquire_radius: float = 2.0    # 重搜索半径(m)


@dataclass
class VoiceConfig:
    enabled:          bool  = True
    language:         str   = "zh-CN"
    tts_engine:       str   = "espeak"   # 或 "edge-tts"
    volume:           float = 0.8


@dataclass
class DisplayConfig:
    enabled:          bool  = True
    screen_topic:     str   = "/display/image"
    width:            int   = 1920
    height:           int   = 1080
    show_debug:       bool  = False


@dataclass
class FollowingConfig:
    camera:       CameraConfig       = field(default_factory=CameraConfig)
    lidar:        LidarConfig        = field(default_factory=LidarConfig)
    detection:    DetectionConfig    = field(default_factory=DetectionConfig)
    tracking:     TrackingConfig     = field(default_factory=TrackingConfig)
    localization: LocalizationConfig = field(default_factory=LocalizationConfig)
    avoidance:    AvoidanceConfig    = field(default_factory=AvoidanceConfig)
    motion:       MotionConfig       = field(default_factory=MotionConfig)
    state:        StateConfig        = field(default_factory=StateConfig)
    voice:        VoiceConfig        = field(default_factory=VoiceConfig)
    display:      DisplayConfig      = field(default_factory=DisplayConfig)

    @classmethod
    def load(cls, path: str = "config/config.yaml") -> "FollowingConfig":
        """从 YAML 文件加载配置，文件不存在则使用默认值。"""
        cfg_path = Path(path)
        if not cfg_path.exists():
            return cls()
        with open(cfg_path) as f:
            data = yaml.safe_load(f) or {}
        # 逐层覆盖默认值
        obj = cls()
        for section, values in data.items():
            if hasattr(obj, section) and isinstance(values, dict):
                section_obj = getattr(obj, section)
                for k, v in values.items():
                    if hasattr(section_obj, k):
                        setattr(section_obj, k, v)
        return obj
