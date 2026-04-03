# 智能迎宾机器人 - 配置说明

## 挥手动作联动配置

### 配置项说明

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `enable_wave_action` | bool | True | 是否启用挥手动作联动 |
| `wave_interval` | int | 60 | 最短触发间隔(秒) |
| `wave_script` | str | `/home/aidlux/demo_arm/wave_hand.py` | 挥手脚本路径 |
| `audio_file` | str | `/home/aidlux/auto.mp3` | 音频文件路径 |
| `mock_wave` | bool | False | 使用模拟模式(无需真实硬件) |

### 动态修改触发间隔

在 Web GUI 中，可以实时修改触发间隔:

1. 打开 Web GUI 页面
2. 在"挥手动作"面板中找到"触发间隔"输入框
3. 输入新的间隔时间(秒)
4. 点击"设置"按钮

修改立即生效，无需重启系统。

### 配置示例

#### 基础配置 (web_gui.py / main.py)

```python
config = {
    # ... 其他配置 ...
    
    # 挥手动作配置
    "enable_wave_action": True,     # 启用挥手联动
    "wave_interval": 60,             # 60秒触发间隔
    "wave_script": "/home/aidlux/demo_arm/wave_hand.py",
    "audio_file": "/home/aidlux/auto.mp3",
}
```

#### 开发测试配置

```python
config = {
    # ... 其他配置 ...
    
    # 挥手动作配置 (测试模式)
    "enable_wave_action": True,
    "wave_interval": 5,              # 5秒间隔(方便测试)
    "mock_wave": True,               # 使用模拟模式
}
```

#### 生产环境配置

```python
config = {
    # ... 其他配置 ...
    
    # 挥手动作配置 (生产模式)
    "enable_wave_action": True,
    "wave_interval": 120,            # 2分钟间隔
    "wave_script": "/home/aidlux/demo_arm/wave_hand.py",
    "audio_file": "/home/aidlux/auto.mp3",
}
```

### 触发逻辑

```
检测到人体
    ↓
距离 <= welcome_distance (默认2米)?
    ↓ 是
检查冷却时间
    ↓ 已过
执行挥手动作 + 播放音频
    ↓
开始冷却计时
```

### 注意事项

1. **间隔时间设置**: 建议不小于30秒，避免过于频繁的机械臂运动
2. **音频播放器**: 确保系统安装了 `mpg123` 或 `ffplay`
3. **脚本权限**: 确保挥手脚本有执行权限
4. **资源释放**: 停止系统时会自动停止挥手动作

### 常见问题

**Q: 如何完全禁用挥手功能?**
A: 设置 `enable_wave_action: False` 或直接使用 `--no-wave` 命令行参数

**Q: 如何快速测试挥手功能?**
A: 使用模拟模式: `python web_gui.py` 并在配置中设置 `mock_wave: True`

**Q: 触发间隔可以设为0吗?**
A: 可以，但不推荐。设为0表示没有间隔限制，每次检测到人都会触发。

**Q: 手动触发会受间隔限制吗?**
A: 正常手动触发受间隔限制，使用"强制触发"按钮可忽略限制。
