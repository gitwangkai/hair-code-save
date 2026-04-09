# H01 机器人人体跟随系统

基于 ROS 2 + RGBD 相机 + 激光雷达的低耦合人体跟随框架。  
适配星炽动力 H01 机器人（QCS8550 · 48TOPs DSP · 双轮差速底盘）。

---

## 文件结构

```
h01_following/
├── main.py                     # 主入口：组装模块、注册事件、启动
├── config/
│   ├── settings.py             # 所有参数 dataclass（集中管理）
│   └── config.yaml             # 现场覆盖配置
├── perception/
│   ├── camera_node.py          # RGBD 相机 ROS 订阅节点
│   ├── lidar_node.py           # 激光雷达 ROS 订阅节点
│   └── detector.py             # YOLOv8-pose ONNX/SNPE 推理
├── tracking/
│   ├── tracker.py              # ByteTrack 多目标关联（含 ReID）
│   ├── localizer.py            # 2D bbox → 3D 坐标（针孔相机模型）
│   └── reid.py                 # 外观重识别（颜色直方图 + 骨骼比例）
├── control/
│   ├── state_machine.py        # 跟随状态机（IDLE/SEARCHING/FOLLOWING…）
│   ├── motion_controller.py    # PID → cmd_vel 差速底盘控制
│   └── obstacle_avoidance.py   # 激光雷达 + 超声波 动态避障
├── interaction/
│   ├── voice_manager.py        # TTS 语音播报
│   └── display_manager.py      # 13.3 寸屏幕 UI 渲染
├── utils/
│   ├── event_bus.py            # 发布-订阅事件总线（模块解耦核心）
│   └── logger.py               # 统一日志工厂
├── tools/
│   └── export_to_snpe.py       # YOLOv8 → SNPE DLC 转换脚本
├── launch/
│   └── h01_following.launch.py # ROS 2 一键启动文件
└── tests/
    └── test_all.py             # 全模块单元测试（不依赖 ROS）
```

---

## 环境依赖

### 系统依赖
```bash
# ROS 2 Humble（Ubuntu 22.04）
sudo apt install ros-humble-desktop
sudo apt install ros-humble-realsense2-camera    # RGBD 相机
sudo apt install ros-humble-cv-bridge
sudo apt install espeak-ng                        # TTS 语音

# YDLIDAR 驱动（根据实际激光雷达型号选择）
# https://github.com/YDLIDAR/ydlidar_ros2_driver
```

### Python 依赖
```bash
pip install -r requirements.txt
# 可选：ByteTrack
pip install bytetracker
# 可选：SNPE 模型转换
pip install ultralytics onnx onnxsim
```

---

## 快速开始

### 1. 导出检测模型（首次运行）
```bash
# 下载并转换 YOLOv8n-pose 为 ONNX
python tools/export_to_snpe.py --model yolov8n-pose --output models/

# 若有 SNPE SDK，进一步转为 DLC（利用 DSP 加速）
python tools/export_to_snpe.py --model yolov8n-pose --output models/ --quantize
```

### 2. 调整配置
编辑 `config/config.yaml`，主要参数：
- `motion.follow_distance`：跟随保持距离（默认 1.0m）
- `detection.model_path`：模型文件路径
- `detection.use_dsp`：是否启用 DSP 加速

### 3. 启动系统
```bash
# 方式一：ROS 2 launch（推荐，含相机/雷达驱动）
source /opt/ros/humble/setup.bash
ros2 launch h01_following launch/h01_following.launch.py

# 方式二：直接运行主节点（相机/雷达驱动已在外部启动）
python main.py
```

### 4. 控制命令
```bash
# 开始跟随（通过 ROS topic 发送命令）
ros2 topic pub /cmd_start std_msgs/msg/Empty "{}" --once

# 停止跟随
ros2 topic pub /cmd_stop std_msgs/msg/Empty "{}" --once
```

---

## 运行单元测试
```bash
# 不需要 ROS 环境
pip install pytest
python -m pytest tests/ -v
```

---

## 核心设计：事件总线解耦

所有模块通过 `EventBus` 通信，**互不持有引用**：

```
CameraNode  →[raw_rgb_frame]→  HumanDetector
                               ↓[human_detections]
                           HumanTracker
                               ↓[tracked_targets]
                           TargetLocalizer
                               ↓[target_pose]
              StateMachine ←───┤
              MotionController ←┘
                               ↓[/cmd_vel]
                           差速底盘
```

新增功能只需：① 创建新模块 ② 在 `main.py` 中订阅/发布事件，其他文件不动。

---

## PID 参数调优

在 `config/config.yaml` 中调整：
```yaml
motion:
  kp_angular: 1.2    # 增大 → 转向更快，过大会震荡
  kp_linear:  0.5    # 增大 → 接近/远离目标更快，过大会超调
  follow_distance: 1.0  # 保持距离（米）
```

建议调优顺序：先固定目标测角速度收敛，再测距离控制。

---

## 硬件对应（H01 规格书）

| 功能模块 | 使用的硬件 | 规格 |
|---|---|---|
| 人体检测 | RGBD 深度相机 ×2 | 15~300cm，74°视场 |
| 避障 | 激光雷达 + 超声波 | 360°，0.1-20m |
| 底盘控制 | 差速电机 | 导航速度 0.25m/s |
| 模型加速 | QCS8550 DSP | 48 TOPs |
| 语音播报 | 4MIC + 功放 | 2×10W 立体声 |
| 状态显示 | 13.3 寸触摸屏 | 1920×1080 |
