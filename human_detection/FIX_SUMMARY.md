# 修复说明

## 问题修复

### 1. 取消 Web 端机械臂连接
**修复方式**: 
- Web GUI 不再直接连接机械臂
- 改为调用独立脚本 `wave_hand_standalone.py`
- 脚本自包含: 连接→挥手→断开

### 2. 检测到直接挥手
**修复方式**:
- `wave_action_simple.py` 直接调用独立脚本
- 脚本内部管理连接和断开
- Web 端只负责检测和触发

## 新的调用流程

```
Web GUI 检测到人
    ↓
wave_action_simple.py 触发
    ↓
调用 wave_hand_standalone.py (子进程)
    ↓
独立脚本执行:
  1. 连接机械臂
  2. 执行挥手动作
  3. 断开机械臂
    ↓
并行播放音频
    ↓
完成
```

## 文件说明

| 文件 | 作用 |
|------|------|
| `src/wave_hand_standalone.py` | 独立挥手脚本，自包含连接/执行/断开 |
| `src/wave_action_simple.py` | Web 端控制器，调用独立脚本 |
| `src/wave_hand_safe.py` | 基础挥手脚本 (被独立脚本调用) |

## 测试方法

### 1. 测试独立脚本 (验证机械臂)
```bash
cd /home/aidlux/human_detection
python3 src/wave_hand_standalone.py
```
如果这一步成功，说明机械臂连接正常。

### 2. 测试检测触发 (验证 Web 端)
```bash
python3 -c "
import sys
sys.path.insert(0, 'src')
from wave_action_simple import SimpleWaveActionController

ctrl = SimpleWaveActionController(min_interval=3)
ctrl.trigger()

import time
while ctrl.is_running:
    time.sleep(1)
    print('.', end='', flush=True)

print('\n完成:', ctrl.get_stats())
"
```

### 3. 启动 Web GUI
```bash
python3 web_gui.py
```
在浏览器中打开，然后检测到人，观察日志输出。

## 配置说明

在 `web_gui.py` 中：
```python
config = {
    "enable_wave_action": True,
    "wave_interval": 60,      # 触发间隔(秒)
    "audio_file": "/home/aidlux/auto.mp3",
    "mock_wave": False,       # False=真实机械臂, True=模拟
}
```

## 故障排除

### 问题: 独立脚本可以执行，Web 端不行
**检查**: 
1. 确认 `wave_hand_standalone.py` 路径正确
2. 检查 Web GUI 日志输出
3. 检查是否有触发间隔限制

### 问题: 检测到人但不触发
**检查**:
1. 查看 Web GUI 日志是否显示 "[挥手] 检测到人"
2. 检查 `wave_interval` 间隔设置
3. 检查 `welcome_distance` 距离设置

### 问题: 触发但机械臂不动
**检查**:
1. 先单独执行 `wave_hand_standalone.py` 验证机械臂
2. 检查机械臂 IP 是否正确 (192.168.3.100)
3. 检查机械臂电源和网络

## 关键代码变更

### wave_action_simple.py
```python
# 不再直接连接机械臂，而是调用独立脚本
def _run_wave_script(self):
    result = subprocess.run(
        ["timeout", "25", "python3", self.wave_script],
        ...
    )
```

### wave_hand_standalone.py
```python
# 自包含完整流程
def main():
    controller = WaveHandController()
    
    if controller.connect():      # 1. 连接
        controller.wave_hand()    # 2. 执行
        controller.disconnect()   # 3. 断开
```

### web_gui.py 触发逻辑
```python
# 检测到人时直接触发，不管理连接
if distance <= welcome_distance:
    if self.wave_controller.can_trigger():
        self.wave_controller.trigger()  # 调用独立脚本
```
