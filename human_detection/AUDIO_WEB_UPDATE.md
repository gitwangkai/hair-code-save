# 网页端音频播放功能

## 功能说明

音频播放从服务器端改为**网页端播放**，使用 HTML5 Audio API。

## 文件变更

### 新增文件
- `src/audio_manager.py` - 音频文件管理器

### 修改文件
- `web_gui.py` - 添加音频服务和 WebSocket 事件

## 功能特点

### 1. 音频下拉列表
- 网页加载时自动扫描 `config/music/` 目录
- 显示所有音频文件 (.mp3, .wav, .ogg, .aac)
- 默认选中 `auto.mp3`

### 2. 浏览器端播放
- 使用 HTML5 `<audio>` 标签
- 音频通过 HTTP 流式传输
- 无需服务器端解码

### 3. 检测触发播放
- 检测到人时，后端发送 `play_audio` 命令
- 前端接收命令并播放选中的音频
- 音频和挥手动作并行执行

## 使用说明

### 添加音频文件
将音频文件放到 `config/music/` 目录：
```bash
cp your_music.mp3 /home/aidlux/human_detection/config/music/
```

刷新网页即可在下拉列表中看到。

### 默认音频
默认使用 `config/music/auto.mp3`，可以在网页下拉列表中切换。

## 测试

### 1. 测试音频管理器
```bash
python3 test_audio_web.py
```

### 2. 启动 Web GUI
```bash
python3 web_gui.py
```

### 3. 浏览器访问
打开网页后，在"挥手动作"面板中：
- 查看音频下拉列表
- 选择要播放的音频
- 走到摄像头前测试

## 技术实现

### 后端 (Python)
```python
# 扫描音频文件
audio_manager = AudioManager()
audio_files = audio_manager.get_audio_list()

# 发送音频列表到前端
socketio.emit('audio_list', {'audio_files': audio_files})

# 检测到人时发送播放命令
socketio.emit('play_audio', {'url': '/music/auto.mp3', 'name': 'auto.mp3'})
```

### 前端 (JavaScript)
```javascript
// 接收音频列表
socket.on('audio_list', function(data) {
    // 填充下拉列表
});

// 接收播放命令
socket.on('play_audio', function(data) {
    var player = document.getElementById('audioPlayer');
    player.src = data.url;
    player.play();
});
```

### HTTP 路由
- `GET /music/<filename>` - 访问音频文件
- `GET /api/audio/list` - 获取音频列表

## 注意事项

1. **浏览器兼容性**: 需要支持 HTML5 Audio 的现代浏览器
2. **自动播放策略**: 某些浏览器需要用户交互后才能自动播放
3. **音频格式**: 推荐使用 MP3 格式，兼容性最好
4. **文件大小**: 建议音频文件不超过 10MB

## 故障排除

### 问题: 下拉列表无音频文件
**检查**:
```bash
ls -la /home/aidlux/human_detection/config/music/
```

### 问题: 音频无法播放
**检查**:
1. 浏览器控制台是否有错误
2. 音频格式是否受支持 (MP3最可靠)
3. 音频文件是否损坏

### 问题: 检测到人但不播放音频
**检查**:
1. 网页是否已选择音频文件
2. 浏览器是否阻止自动播放
3. WebSocket 连接是否正常
