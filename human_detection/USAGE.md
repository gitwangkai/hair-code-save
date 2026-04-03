# 智能迎宾机器人 - 使用说明

## 快速启动

### 1. 启动 Web GUI

```bash
cd /home/aidlux/human_detection
python3 web_gui.py
```

然后在浏览器中打开显示的地址（通常是 `http://localhost:5000`）

### 2. 功能说明

#### 挥手动作联动

当检测到人且距离在 2 米范围内时，系统会自动：
1. 执行机械臂挥手动作
2. 播放音频文件 `/home/aidlux/auto.mp3`

**触发间隔**: 默认 60 秒，可在 Web GUI 中实时修改

#### 手动触发

在 Web GUI 的"挥手动作"面板中：
- **触发挥手**: 手动触发挥手动作
- **强制触发**: 忽略间隔限制立即触发
- **设置间隔**: 修改触发间隔时间

### 3. 配置修改

编辑 `web_gui.py` 中的 `config` 字典：

```python
config = {
    # 摄像头配置
    "camera_source": "/dev/video_header",
    "width": 640,
    "height": 360,
    
    # 检测配置
    "welcome_distance": 2.0,  # 迎宾触发距离(米)
    "detect_interval": 3,      # 检测间隔(帧)
    
    # 挥手动作配置
    "enable_wave_action": True,
    "wave_interval": 60,       # 触发间隔(秒)
    "audio_file": "/home/aidlux/auto.mp3",
    "mock_wave": False,        # False=执行真实动作, True=仅模拟
}
```

## 故障排除

### 问题: 检测到人不触发挥手

**检查步骤**:
1. 查看 Web GUI 日志，确认是否显示 "[挥手] 检测到人"
2. 检查距离是否在范围内（默认 2 米）
3. 检查是否在冷却中（默认 60 秒间隔）
4. 检查"挥手动作"面板中的状态显示

**调试**:
```bash
# 运行检测触发测试
python3 test_detection_trigger.py
```

### 问题: 挥手动作失败

**可能原因**:
1. 机械臂未连接或电源未开启
2. PallasSDK 段错误（已知问题）
3. 音频设备不可用

**解决**:
- 检查机械臂电源和网络连接
- 使用模拟模式测试: 设置 `"mock_wave": True`
- 检查音频播放器: `ffplay /home/aidlux/auto.mp3`

### 问题: 音频不播放

**检查**:
```bash
# 测试音频文件
ffplay -nodisp -autoexit /home/aidlux/auto.mp3

# 或
mpg123 /home/aidlux/auto.mp3
```

**解决**:
```bash
# 安装音频播放器
sudo apt-get install ffmpeg mpg123
```

### 问题: Web GUI 崩溃

**原因**: PallasSDK 与 Flask 冲突

**解决**: 
- 确保使用简化版控制器（默认已启用）
- 禁用机械臂控制，仅保留挥手动作

## 测试命令

```bash
# 测试挥手动作
python3 src/wave_hand_safe.py

# 测试检测触发
python3 test_detection_trigger.py

# 测试完整流程
python3 test_wave_complete.py

# 检查配置
python3 check_config.py
```

## 文件说明

| 文件 | 说明 |
|------|------|
| `web_gui.py` | Web 服务器主程序 |
| `src/wave_action_simple.py` | 简化版挥手控制器 |
| `src/wave_hand_safe.py` | 安全版挥手脚本 |
| `config.json` | 配置文件 |
| `test_detection_trigger.py` | 检测触发测试 |

## 注意事项

1. **触发间隔**: 建议不小于 30 秒，避免频繁触发
2. **检测距离**: 根据实际场景调整 `welcome_distance`
3. **机械臂冲突**: PallasSDK 与 Flask 有兼容性问题，使用独立进程执行
4. **音频设备**: 服务器环境可能无音频输出，属于正常现象
