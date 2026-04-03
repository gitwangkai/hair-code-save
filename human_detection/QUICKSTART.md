# 智能迎宾机器人 - 快速开始

## 启动方式

### 方式1: Web GUI (推荐)
```bash
python3 web_gui.py
```
然后在浏览器打开显示的地址 (如 `http://localhost:5000`)

### 方式2: 交互式菜单
```bash
./start_with_arm.sh
```

### 方式3: 主程序
```bash
python3 main.py
```

## 挥手动作功能

### 自动触发
- 检测到人且距离 ≤ 2米时自动触发
- 执行 `/home/aidlux/demo_arm/wave_hand.py` 挥手脚本
- 播放 `/home/aidlux/auto.mp3` 音频
- 默认触发间隔: 60秒

### Web GUI 控制
打开 Web GUI 后，在右侧"挥手动作"面板:
- **触发间隔**: 可实时修改(0-3600秒)
- **触发挥手**: 手动触发
- **强制触发**: 忽略间隔限制
- **停止动作**: 立即停止
- **统计信息**: 触发次数、跳过次数、剩余冷却

### 修改触发间隔

**方式1: Web GUI (推荐)**
直接在页面上修改并点击"设置"

**方式2: 修改配置文件**
编辑 `web_gui.py` 中的 `config`:
```python
config = {
    # ...
    "wave_interval": 30,  # 改为30秒
}
```

## 测试功能

### 测试挥手联动
```bash
python3 test_wave_integration.py
```

### 测试机械臂
```bash
python3 test_arm.py --mock
```

### 模拟模式 (无需硬件)
```python
# 在 web_gui.py 的 config 中设置
"mock_wave": True
```

## 故障排除

### 挥手动作失败

如果看到 `挥手动作失败` 错误:

1. **检查机械臂连接**:
   ```bash
   python3 check_config.py
   ```

2. **测试单独执行挥手脚本**:
   ```bash
   python3 /home/aidlux/demo_arm/wave_hand_safe.py
   ```

3. **使用模拟模式测试**:
   ```python
   # 在 web_gui.py 配置中设置
   "mock_wave": True
   ```

4. **常见问题**:
   - 机械臂电源未开启 → 检查电源
   - 网络不通 → 检查网线/WiFi
   - IP地址错误 → 修改配置中的 `arm_ip`

### 音频播放失败

1. 检查音频文件存在:
   ```bash
   ls -la /home/aidlux/auto.mp3
   ```

2. 安装播放器:
   ```bash
   sudo apt-get install mpg123
   ```

## 常见问题

**Q: 如何关闭挥手功能?**
```bash
# 方式1: 修改配置
"enable_wave_action": False

# 方式2: 设置极大间隔
"wave_interval": 999999
```

**Q: 触发间隔最小可以设多少?**
- 最小 0 秒 (每次检测都触发)
- 建议不小于 30 秒

**Q: 如何更换音频文件?**
修改配置:
```python
"audio_file": "/path/to/your/audio.mp3"
```
