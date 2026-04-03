# 挥手动作问题修复总结

## 问题诊断

### 错误码 -11 (SIGSEGV 段错误)
```
[WaveAction] 挥手执行失败 (返回码: -11)
```

**根本原因**: PallasSDK 与 Python 多线程/Flask 存在严重的内存冲突
- 即使通过子进程执行，PallasSDK 仍会崩溃
- 可能是 SDK 本身的线程安全问题
- 也可能是 Python GIL 与 C++ 库的冲突

### 无法回到安全位置
- 之前的代码在失败时可能没有正确执行恢复动作
- 段错误导致进程直接退出，没有执行清理代码

## 修复方案

### 方案1: 使用独立 Shell 脚本 (推荐)

创建 `/tmp/wave_hand_runner.sh` 脚本，完全脱离 Python 进程管理：

```bash
#!/bin/bash
cd /home/aidlux/demo_arm
timeout 20 python3 wave_hand.py 2>&1
exit $?
```

**优点**:
- 完全独立于 Flask 进程
- 即使崩溃也不会影响 Web 服务
- 简单易维护

**缺点**:
- 无法精确控制挥手动作
- 段错误仍然会发生，但被隔离

### 方案2: 使用 multiprocessing spawn (已尝试)

使用 `multiprocessing.get_context('spawn')` 创建完全隔离的进程。

**结果**: 仍然段错误，说明问题在 PallasSDK 本身

### 方案3: 修改 wave_hand_safe.py (已更新)

新增功能：
1. `atexit.register()` - 确保退出时回到安全位
2. `finally:` 块 - 确保异常时恢复
3. `_cleanup()` 方法 - 专门的清理逻辑
4. 信号处理 - 捕获中断信号执行恢复

### 方案4: 使用简化版控制器

`wave_action_simple.py` - 最简实现，使用 shell 脚本方式

## 推荐使用方式

### 方法A: 直接执行原始脚本 (最可靠)

```bash
# 在终端直接执行，不通过 Web
cd /home/aidlux/demo_arm
python3 wave_hand.py
```

### 方法B: 使用简化版控制器

修改 `web_gui.py`：
```python
from wave_action_simple import SimpleWaveActionController as WaveActionController
```

### 方法C: 禁用挥手功能，使用纯音频

如果机械臂控制不稳定，可以只保留音频播放：
```python
# 在配置中设置
"mock_wave": True  # 只播放音频，不执行挥手
```

## 故障排除

### 问题: 仍然返回 -11
**解决**: 这是 PallasSDK 的固有问题，建议：
1. 检查 PallasSDK 版本是否最新
2. 联系厂商获取兼容性更好的版本
3. 考虑使用其他控制方式（如 ROS2、Modbus）

### 问题: 音频也不播放
**检查**:
```bash
# 测试音频播放器
ffplay -nodisp -autoexit /home/aidlux/auto.mp3

# 或
mpg123 /home/aidlux/auto.mp3
```

### 问题: Web GUI 崩溃
**解决**: 确保使用 `wave_action_simple.py` 或 `mock_wave: True`

## 长期解决方案

1. **更新 PallasSDK** - 联系厂商获取修复版本
2. **使用替代方案**:
   - 使用厂商提供的 ROS2 接口
   - 使用 Modbus/TCP 直接控制
   - 使用 WebSocket 接口（如已有的 arm_websock.py）

3. **硬件隔离**:
   - 在独立设备上运行机械臂控制
   - 通过网络协议与主系统通信

## 测试命令

```bash
# 测试独立执行
cd /home/aidlux/demo_arm
python3 wave_hand.py

# 测试安全版本
cd /home/aidlux/human_detection
python3 src/wave_hand_safe.py

# 测试包装器
python3 src/wave_hand_wrapper.py

# 测试简化版
python3 src/wave_action_simple.py
```
