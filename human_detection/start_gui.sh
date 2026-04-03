#!/bin/bash
# 智能迎宾机器人 Web GUI 启动脚本

echo "=========================================="
echo "  智能迎宾机器人 - Web GUI 启动脚本"
echo "=========================================="
echo ""

# 检查 Python
echo "[检查] Python 环境..."
python3 --version || { echo "错误: 未找到 Python3"; exit 1; }

# 进入目录
cd "$(dirname "$0")"

# 检查依赖
echo "[检查] Python 依赖..."
python3 -c "import flask, flask_socketio, cv2" 2>/dev/null || {
    echo "正在安装依赖..."
    pip3 install flask flask-socketio
}

# 创建必要目录
mkdir -p templates detections data models/insightface/models

# 清理旧进程
echo "[清理] 停止旧进程..."
pkill -f "python3.*web_gui.py" 2>/dev/null
sleep 2

# 启动服务器
echo ""
echo "[启动] Web GUI 服务器..."
echo ""

python3 web_gui.py &

# 等待服务器启动
sleep 4

# 获取端口
PORT=$(lsof -i -P -n | grep python | grep LISTEN | awk '{print $9}' | cut -d: -f2 | head -1)

if [ -n "$PORT" ]; then
    echo ""
    echo "=========================================="
    echo "  ✅ 服务器启动成功!"
    echo "=========================================="
    echo ""
    echo "  📱 请在浏览器中打开:"
    echo ""
    echo "     http://$(hostname -I | awk '{print $1}'):$PORT"
    echo ""
    echo "  或本地访问:"
    echo "     http://localhost:$PORT"
    echo ""
    echo "=========================================="
    echo "  按回车键停止服务器..."
    echo "=========================================="
    read
    
    echo "[停止] 正在关闭服务器..."
    pkill -f "python3.*web_gui.py"
    echo "✅ 服务器已停止"
else
    echo "❌ 服务器启动失败，请检查日志"
    exit 1
fi
