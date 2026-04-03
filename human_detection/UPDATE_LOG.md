# 更新日志

## 2026-03-31 更新

### 1. 禁用日志刷屏
**问题**: Socket.IO 日志太多，刷屏严重

**修复**: 在 `web_gui.py` 中禁用 Flask/SocketIO 默认日志
```python
logging.getLogger('werkzeug').setLevel(logging.ERROR)
logging.getLogger('engineio').setLevel(logging.ERROR)
logging.getLogger('socketio').setLevel(logging.ERROR)

self.socketio = SocketIO(..., logger=False, engineio_logger=False)
```

现在只会显示重要的系统日志，不再刷屏。

### 2. 修改迎宾距离为10米
**问题**: 原来只在2米内触发，范围太小

**修复**: 将 `welcome_distance` 从 2.0 改为 10.0
```python
"welcome_distance": 10.0,  # 10米内都触发
```

现在人在摄像头前10米内都会触发挥手。

## 当前配置

```python
config = {
    "enable_wave_action": True,
    "wave_interval": 60,          # 触发间隔60秒
    "welcome_distance": 10.0,     # 迎宾距离10米
    "audio_file": "/home/aidlux/auto.mp3",
}
```

## 使用说明

启动 Web GUI:
```bash
python3 web_gui.py
```

现在日志会清爽很多，不会再刷屏。
10米内有人都会自动触发挥手。
