# PallasSDK 兼容性问题说明

## 问题描述

PallasSDK (机械臂控制库) 与 Flask/FastAPI 等 Web 框架存在严重的兼容性问题：

1. **段错误 (Segmentation Fault)**: 同时导入 PallasSDK 和运行 Flask 会导致进程崩溃
2. **UDP 绑定失败**: 在某些网络环境下会出现 `[Error] -51 UDP bound failed`
3. **内存冲突**: PallasSDK 与 Python 的某些库存在内存冲突

## 解决方案

### 当前实现

1. **完全隔离执行**: 挥手动作通过独立的子进程执行 (`wave_hand_standalone.py`)
2. **延迟导入**: PallasSDK 仅在独立进程中导入，不在主 Flask 进程中加载
3. **模拟模式**: 默认启用模拟模式，避免 PallasSDK 崩溃

### 配置文件

```python
config = {
    # 挥手动作配置
    "enable_wave_action": True,
    "wave_interval": 60,
    "wave_script": "/home/aidlux/demo_arm/wave_hand_standalone.py",
    "audio_file": "/home/aidlux/auto.mp3",
    "mock_wave": True,  # 默认使用模拟模式
}
```

### 使用真实机械臂

如果需要在 Web GUI 中使用真实机械臂，建议：

1. **单独运行挥手脚本**: 不通过 Web GUI，直接执行脚本
   ```bash
   python3 /home/aidlux/demo_arm/wave_hand.py
   ```

2. **使用 ROS2 接口**: 如果系统支持 ROS2，可以通过 ROS2 话题控制机械臂

3. **修改硬件**: 使用串口或 EtherCAT 直接控制，绕过 PallasSDK 的 UDP 通信

## 测试

### 测试模拟模式
```bash
python3 test_wave_integration.py
```

### 测试真实机械臂 (独立进程)
```bash
python3 /home/aidlux/demo_arm/wave_hand_standalone.py
```

### 检查 PallasSDK 状态
```bash
# 检查是否可以导入
python3 -c "from PallasSDK import Controller; print('OK')"

# 测试连接
python3 -c "
from PallasSDK import Controller
ctrl = Controller()
ctrl.Connect('192.168.3.100')
print('Connected')
"
```

## 故障排除

### 问题: Web GUI 启动后立即崩溃
**原因**: PallasSDK 与 Flask 冲突
**解决**: 确保配置中 `mock_wave: True`

### 问题: 段错误 (Segmentation fault)
**原因**: PallasSDK 内存冲突
**解决**: 使用独立子进程执行机械臂操作

### 问题: UDP bound failed
**原因**: 网络端口被占用或权限问题
**解决**: 检查是否有其他程序占用相关端口，或使用 root 权限运行

## 联系支持

如果问题持续存在，请联系：
- 机械臂厂商获取 PallasSDK 更新
- 检查是否有新版本的 SDK 修复了兼容性问题
