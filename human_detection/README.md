# 🤖 智能迎宾机器人

基于 YOLOv8 + InsightFace 的人体检测与人脸识别系统，适用于机器人迎宾场景。

## ✨ 功能特性

- **人体检测**: 基于 YOLOv8，支持实时人体检测和追踪
- **人脸识别**: 基于 InsightFace，支持人脸注册和识别
- **智能迎宾**: 自动检测访客，区分新老访客，生成个性化问候语
- **距离估计**: 基于人体高度估计距离，支持 2 米范围内的精准检测
- **云台追踪**: 支持云台控制，保持目标在画面中央
- **机械臂互动**: 迎宾时自动控制机械臂挥手/欢迎动作
- **挥手联动**: 检测到人时自动执行挥手动作并播放音频
- **触发间隔**: 支持配置最短触发间隔(默认60秒)，防止重复触发
- **访客统计**: 记录访客信息，支持统计分析

## 📁 项目结构

```
human_detection/
├── main.py                 # 主程序入口
├── web_gui.py             # Web GUI 服务器
├── requirements.txt        # Python 依赖
├── README.md              # 项目说明
├── src/
│   ├── camera.py          # 摄像头驱动
│   ├── detector.py        # 人体检测 (YOLOv8)
│   ├── face_recognizer.py # 人脸识别 (InsightFace)
│   ├── greeter.py         # 迎宾业务逻辑
│   ├── arm_controller.py  # 机械臂控制器 (PallasSDK)
│   └── ...
├── utils/
│   └── visualization.py   # 可视化工具
├── models/                # 模型文件目录
│   ├── yolov8n.pt        # YOLOv8 模型 (自动下载)
│   └── insightface/      # InsightFace 模型
└── data/
    └── face_database.pkl # 人脸数据库
```

## 🚀 快速开始

### 1. 安装依赖

```bash
cd human_detection
pip install -r requirements.txt
```

### 2. 运行程序

```bash
# 使用默认摄像头
python main.py

# 指定摄像头
python main.py --camera 0

# 列出可用摄像头
python main.py --list-cameras

# 调整迎宾距离
python main.py --distance 2.5
```

### 3. 使用说明

运行后，按以下按键操作:

| 按键 | 功能 |
|------|------|
| `q` | 退出程序 |
| `s` | 保存截图 |
| `r` | 注册当前人脸 |
| `c` | 标定距离参数 |

## 📋 工作流程

```
待机状态 ──→ 检测到人体 ──→ 人脸识别 ──→ 迎宾问候 ──→ 追踪目标 ──→ 返回待机
              (2米内)       (识别身份)   (语音+屏幕)   (云台控制)
```

## 🔧 高级配置

### 注册人脸

1. 让人面对摄像头
2. 按 `r` 键
3. 输入姓名

### 标定距离

1. 让人站在 2 米处
2. 按 `c` 键
3. 系统自动计算焦距参数

### 调整迎宾参数

编辑 `main.py` 中的 `config` 字典:

```python
config = {
    "welcome_distance": 2.0,      # 迎宾触发距离 (米)
    "min_greet_interval": 10,      # 最短迎宾间隔 (秒)
    "confidence_threshold": 0.5,   # 检测置信度阈值
    "recognition_threshold": 0.6,  # 人脸识别阈值
    ...
}
```

## 🎯 性能优化

在 ARM 平台 (如 AidLux) 上，建议:

1. **使用轻量级模型**:
   - YOLOv8n (Nano) - 推荐，速度最快
   - YOLOv8s (Small) - 平衡精度和速度

2. **降低分辨率**:
   ```bash
   python main.py --width 480 --height 360
   ```

3. **调整检测频率**:
   - 修改 `detector.py` 中的处理间隔

## 📊 性能指标

在典型 ARM64 平台上的测试数据:

| 模型 | 分辨率 | FPS | CPU 占用 |
|------|--------|-----|----------|
| YOLOv8n | 640x480 | 15-20 | 60-70% |
| YOLOv8s | 640x480 | 8-12 | 70-80% |
| YOLOv8n | 480x360 | 20-25 | 50-60% |

## 🔌 集成接口

### 语音播报接口

在 `greeter.py` 中修改 `_on_greet` 回调:

```python
def _on_greet(self, name: str, message: str, is_new: bool):
    # 调用语音合成API
    tts_engine.speak(message)
```

### 云台控制接口

在 `greeter.py` 中处理 `pan_tilt` 输出:

```python
pan_angle, tilt_angle = action_result["pan_tilt"]
# 发送云台控制指令
ptz_controller.move(pan_angle, tilt_angle)
```

### 挥手动作联动

#### 自动触发

当检测到人且距离在范围内时，系统自动:
1. 执行机械臂挥手动作 (`/home/aidlux/demo_arm/wave_hand.py`)
2. 播放音频文件 (`/home/aidlux/auto.mp3`)
3. 遵守触发间隔限制(默认60秒)

#### Web GUI 控制面板

- **触发间隔设置**: 可实时修改最短触发间隔(0-3600秒)
- **手动触发**: 点击"触发挥手"按钮
- **强制触发**: 点击"强制触发"按钮(忽略间隔限制)
- **停止动作**: 立即停止当前动作
- **统计信息**: 显示触发次数、跳过次数、剩余冷却时间

#### 配置参数

```python
config = {
    "enable_wave_action": True,     # 启用挥手联动
    "wave_interval": 60,             # 触发间隔(秒)
    "wave_script": "/home/aidlux/demo_arm/wave_hand.py",  # 挥手脚本
    "audio_file": "/home/aidlux/auto.mp3",                # 音频文件
}
```

### ⚠️ 机械臂控制注意事项

**重要**: PallasSDK 与 Flask Web 框架存在兼容性问题，可能导致段错误。
当前实现使用以下方式避免问题：

1. **默认使用模拟模式**: 避免 PallasSDK 崩溃
2. **独立子进程**: 真实机械臂控制通过独立进程执行
3. **延迟导入**: PallasSDK 不在主进程中加载

详见: [PALLAS_ISSUE.md](PALLAS_ISSUE.md)

#### 1. 使用 Web GUI 控制

Web GUI 提供了机械臂控制面板 (模拟模式):
- **连接/断开**: 手动控制机械臂连接
- **回原点**: 机械臂回到初始位置
- **挥手**: 执行挥手动作
- **欢迎**: 执行欢迎动作
- **夹爪控制**: 张开/闭合夹爪

启动 Web GUI:
```bash
python web_gui.py
```

#### 2. 编程接口

```python
from src.arm_controller import ArmController

# 初始化并连接
arm = ArmController(ip="192.168.3.100")
arm.connect()

# 执行动作
arm.wave_hand()        # 挥手
arm.welcome_guest()    # 欢迎动作
arm.move_to_home()     # 回原点

# 夹爪控制
arm.gripper_open()
arm.gripper_close()

# 断开连接
arm.disconnect()
```

#### 3. 机械臂测试

```bash
# 测试机械臂连接和基本功能
python test_arm.py

# 使用模拟模式测试 (无需真实机械臂)
python test_arm.py --mock

# 指定IP地址
python test_arm.py --ip 192.168.3.100

# 单独测试某项功能
python test_arm.py --test movement  # 只测试关节运动
python test_arm.py --test gripper   # 只测试夹爪
python test_arm.py --test action    # 只测试预设动作
```

#### 4. 在主程序中启用机械臂

```bash
# 默认启用机械臂
python main.py

# 禁用机械臂
python main.py --no-arm

# 使用模拟模式
python main.py --mock-arm

# 指定机械臂IP
python main.py --arm-ip 192.168.3.100
```

#### 5. 迎宾自动触发

当检测到访客并触发迎宾时，系统会自动控制机械臂:
- **新访客**: 执行完整的欢迎动作 (举手 + 点头)
- **老访客**: 执行挥手动作

### ROS2 集成

参考项目中已有的 WebSocket 接口:

```python
from arm_websock import call_arm_service

# 机械臂联动
call_arm_service("left_init")  # 复位
```

## 🐛 常见问题

### Q: 模型下载失败?
A: 手动下载模型文件放到 `models/` 目录:
- YOLOv8: https://github.com/ultralytics/assets/releases

### Q: 人脸识别精度低?
A: 
1. 确保光线充足
2. 注册多角度人脸
3. 调整 `recognition_threshold` 参数

### Q: 距离估计不准?
A:
1. 使用 `c` 键重新标定
2. 确保人体完整出现在画面中

## 📄 许可证

MIT License

## 🙏 致谢

- [Ultralytics YOLOv8](https://github.com/ultralytics/ultralytics)
- [InsightFace](https://github.com/deepinsight/insightface)
- [OpenCV](https://opencv.org/)
