#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能迎宾机器人 - Web GUI
基于 Flask + WebSocket 的实时监控系统
"""

import os
import sys
import io
import base64
import threading
import time
from datetime import datetime
from typing import Optional, Dict, List

from flask import Flask, render_template, jsonify, request, Response, send_from_directory
from flask_socketio import SocketIO, emit
from werkzeug.utils import secure_filename
import cv2
import numpy as np

# 添加 src 到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'utils'))

from camera import Camera
from detector import HumanDetector
from face_recognizer import FaceRecognizer
from greeter import GreeterLogic, GreeterState
from visualization import Visualizer
# 注意: ArmController 使用延迟导入，避免 PallasSDK 与 Flask 冲突
from wave_action import WaveActionController, MockWaveActionController, WaveActionWebInterface
from wave_action_simple import SimpleWaveActionController
from audio_manager import AudioManager, get_audio_manager
# ArmController 和 MockArmController 延迟导入，见 init_components


class WebGUIServer:
    """
    Web GUI 服务器
    
    功能:
    - 实时视频流推送
    - 检测结果显示
    - 系统状态监控
    - 远程控制接口
    """
    
    def __init__(self, config: dict, host='0.0.0.0', port=5000):
        """
        初始化 Web GUI 服务器
        
        Args:
            config: 系统配置
            host: 服务器地址
            port: 服务器端口
        """
        self.config = config
        self.host = host
        self.port = port
        
        # Flask 应用
        self.app = Flask(__name__, template_folder='templates')
        self.app.config['SECRET_KEY'] = 'welcome_robot_secret_key'
        
        # 禁用 Flask/SocketIO 默认日志，避免刷屏
        import logging
        logging.getLogger('werkzeug').setLevel(logging.ERROR)
        logging.getLogger('engineio').setLevel(logging.ERROR)
        logging.getLogger('socketio').setLevel(logging.ERROR)
        
        self.socketio = SocketIO(self.app, cors_allowed_origins="*", async_mode='threading', logger=False, engineio_logger=False)
        
        # 系统组件
        self.camera: Optional[Camera] = None
        self.detector: Optional[HumanDetector] = None
        self.face_recognizer: Optional[FaceRecognizer] = None
        self.greeter: Optional[GreeterLogic] = None
        self.visualizer: Optional[Visualizer] = None
        self.arm_controller = None  # 机械臂控制器
        self.wave_controller = None  # 挥手动作控制器
        
        # 运行状态
        self.is_running = False
        self.processing_thread: Optional[threading.Thread] = None
        self.frame_count = 0
        self.last_fps_time = time.time()
        self.current_fps = 0
        
        # 最新帧和检测结果 (用于Web推送)
        self.latest_frame: Optional[np.ndarray] = None
        self.latest_detections: List[Dict] = []
        self.last_detection_time = 0
        self.detection_persist_time = 0.5  # 检测保持时间(秒)
        self.last_persons = []  # 上一帧检测结果(用于平滑)
        self.system_status = {
            'state': '待机',
            'fps': 0,
            'persons': 0,
            'ptz': '0,0',
            'visitors': 0,
            'arm_status': '未连接',
            'arm_connected': False,
            'timestamp': datetime.now().strftime('%H:%M:%S')
        }
        
        # 性能优化参数
        self.detect_interval = 1  # 每1帧检测一次，提高帧率
        self.push_interval = 2    # 每2帧推送一次
        self.jpeg_quality = 60    # JPEG质量(降低带宽)
        
        # 日志缓冲区
        self.log_buffer = []
        self.max_logs = 100
        
        # 注册路由和事件
        self._register_routes()
        self._register_socketio_events()
        
        self.log("Web GUI 服务器初始化完成")
    
    def log(self, message: str, level='info'):
        """记录日志"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        log_entry = {
            'time': timestamp,
            'level': level,
            'message': message
        }
        self.log_buffer.append(log_entry)
        if len(self.log_buffer) > self.max_logs:
            self.log_buffer.pop(0)
        
        print(f"[{timestamp}] {message}")
        
        # 推送到前端
        try:
            self.socketio.emit('log_update', log_entry)
        except:
            pass
    
    def _register_routes(self):
        """注册 HTTP 路由"""
        
        @self.app.route('/')
        def index():
            """主页"""
            return render_template('index.html')
        
        @self.app.route('/api/status')
        def api_status():
            """获取系统状态"""
            return jsonify(self.system_status)
        
        @self.app.route('/api/start', methods=['POST'])
        def api_start():
            """启动系统"""
            success = self.start_processing()
            return jsonify({'success': success})
        
        @self.app.route('/api/stop', methods=['POST'])
        def api_stop():
            """停止系统"""
            self.stop_processing()
            return jsonify({'success': True})
        
        @self.app.route('/api/snapshot')
        def api_snapshot():
            """获取当前帧截图"""
            if self.latest_frame is not None:
                _, buffer = cv2.imencode('.jpg', self.latest_frame)
                response = Response(buffer.tobytes(), mimetype='image/jpeg')
                return response
            return jsonify({'error': 'No frame available'}), 404
        
        @self.app.route('/api/register_face', methods=['POST'])
        def api_register_face():
            """上传照片注册人脸"""
            try:
                name = request.form.get('name', '').strip()
                if not name:
                    return jsonify({'success': False, 'message': '请输入姓名'})
                
                # 检查是否有文件上传
                if 'image' in request.files:
                    file = request.files['image']
                    if file.filename == '':
                        return jsonify({'success': False, 'message': '未选择文件'})
                    
                    # 读取上传的图片
                    file_bytes = file.read()
                    nparr = np.frombuffer(file_bytes, np.uint8)
                    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                    
                elif 'use_current' in request.form:
                    # 使用当前帧
                    if self.latest_frame is None:
                        return jsonify({'success': False, 'message': '无当前画面'})
                    image = self.latest_frame.copy()
                else:
                    return jsonify({'success': False, 'message': '请上传图片或使用当前画面'})
                
                if image is None:
                    return jsonify({'success': False, 'message': '无法读取图片'})
                
                # 检测人脸
                faces = self.face_recognizer.detect_faces(image)
                if not faces:
                    return jsonify({'success': False, 'message': '未检测到人脸，请上传清晰的正面照片'})
                
                # 选择最大的人脸
                face = max(faces, key=lambda f: 
                          (f["bbox"][2]-f["bbox"][0]) * (f["bbox"][3]-f["bbox"][1]))
                
                # 注册人脸
                success = self.face_recognizer.register_face(name, face)
                if success:
                    self.log(f'人脸注册成功: {name}', 'success')
                    return jsonify({'success': True, 'message': f'成功注册: {name}'})
                else:
                    return jsonify({'success': False, 'message': '人脸特征提取失败'})
                    
            except Exception as e:
                self.log(f'注册失败: {e}', 'error')
                return jsonify({'success': False, 'message': f'注册失败: {str(e)}'})
        
        # ========== 音频文件服务 ==========
        
        @self.app.route('/music/<path:filename>')
        def serve_music(filename):
            """提供音频文件访问"""
            music_dir = "/home/aidlux/human_detection/config/music"
            return send_from_directory(music_dir, filename)
        
        @self.app.route('/api/audio/list')
        def api_audio_list():
            """获取音频文件列表"""
            try:
                audio_manager = get_audio_manager()
                return jsonify({
                    'success': True,
                    'audio_files': audio_manager.get_audio_list(),
                    'default': audio_manager.get_default_audio()
                })
            except Exception as e:
                return jsonify({'success': False, 'message': str(e)})
    
    def _register_socketio_events(self):
        """注册 WebSocket 事件"""
        
        @self.socketio.on('connect')
        def handle_connect():
            """客户端连接"""
            self.log('Web 客户端已连接', 'info')
            emit('status_update', self.system_status)
            # 发送历史日志
            for log in self.log_buffer[-20:]:
                emit('log_update', log)
            # 发送音频列表
            try:
                audio_manager = get_audio_manager()
                emit('audio_list', {
                    'audio_files': audio_manager.get_audio_list(),
                    'default': audio_manager.get_default_audio()
                })
            except Exception as e:
                self.log(f'发送音频列表失败: {e}', 'warning')
        
        @self.socketio.on('disconnect')
        def handle_disconnect():
            """客户端断开"""
            self.log('Web 客户端已断开', 'info')
        
        @self.socketio.on('start_system')
        def handle_start_system():
            """启动系统"""
            if self.start_processing():
                emit('system_started', {'status': 'success'})
            else:
                emit('system_error', {'message': '启动失败'})
        
        @self.socketio.on('stop_system')
        def handle_stop_system():
            """停止系统"""
            self.stop_processing()
            emit('system_stopped', {'status': 'success'})
        
        @self.socketio.on('register_face')
        def handle_register_face(data):
            """注册人脸"""
            name = data.get('name', '')
            if name and self.latest_frame is not None and self.face_recognizer:
                # 检测人脸
                faces = self.face_recognizer.detect_faces(self.latest_frame)
                if faces:
                    success = self.face_recognizer.register_face(name, faces[0])
                    if success:
                        self.log(f'人脸注册成功: {name}', 'success')
                        emit('register_result', {'success': True, 'name': name})
                    else:
                        emit('register_result', {'success': False, 'message': '注册失败'})
                else:
                    emit('register_result', {'success': False, 'message': '未检测到人脸'})
            else:
                emit('register_result', {'success': False, 'message': '参数错误'})
        
        # ========== 机械臂控制接口 ==========
        
        @self.socketio.on('arm_connect')
        def handle_arm_connect():
            """连接机械臂"""
            if self.arm_controller:
                success = self.arm_controller.connect()
                emit('arm_result', {'success': success, 'action': 'connect'})
            else:
                emit('arm_result', {'success': False, 'action': 'connect', 'message': '控制器未初始化'})
        
        @self.socketio.on('arm_disconnect')
        def handle_arm_disconnect():
            """断开机械臂"""
            if self.arm_controller:
                self.arm_controller.disconnect()
                emit('arm_result', {'success': True, 'action': 'disconnect'})
        
        @self.socketio.on('arm_home')
        def handle_arm_home():
            """机械臂回原点"""
            if self.arm_controller and self.arm_controller.is_ready():
                success = self.arm_controller.move_to_home()
                emit('arm_result', {'success': success, 'action': 'home'})
            else:
                emit('arm_result', {'success': False, 'action': 'home', 'message': '机械臂未就绪'})
        
        @self.socketio.on('arm_wave')
        def handle_arm_wave():
            """执行挥手动作"""
            if self.arm_controller and self.arm_controller.is_ready():
                self.log("手动触发挥手动作", "info")
                success = self.arm_controller.wave_hand()
                emit('arm_result', {'success': success, 'action': 'wave'})
            else:
                emit('arm_result', {'success': False, 'action': 'wave', 'message': '机械臂未就绪'})
        
        @self.socketio.on('arm_welcome')
        def handle_arm_welcome():
            """执行欢迎动作"""
            if self.arm_controller and self.arm_controller.is_ready():
                self.log("手动触发欢迎动作", "info")
                success = self.arm_controller.welcome_guest()
                emit('arm_result', {'success': success, 'action': 'welcome'})
            else:
                emit('arm_result', {'success': False, 'action': 'welcome', 'message': '机械臂未就绪'})
        
        @self.socketio.on('arm_gripper')
        def handle_arm_gripper(data):
            """控制夹爪"""
            if self.arm_controller and self.arm_controller.is_ready():
                action = data.get('action', '')
                if action == 'open':
                    success = self.arm_controller.gripper_open()
                    emit('arm_result', {'success': success, 'action': 'gripper_open'})
                elif action == 'close':
                    success = self.arm_controller.gripper_close()
                    emit('arm_result', {'success': success, 'action': 'gripper_close'})
                else:
                    emit('arm_result', {'success': False, 'message': '未知动作'})
            else:
                emit('arm_result', {'success': False, 'action': 'gripper', 'message': '机械臂未就绪'})
        
        @self.socketio.on('get_arm_status')
        def handle_get_arm_status():
            """获取机械臂状态"""
            if self.arm_controller:
                emit('arm_status', {
                    'status': self.arm_controller.get_state().value,
                    'connected': self.system_status.get('arm_connected', False),
                    'positions': self.arm_controller.get_joint_positions()
                })
            else:
                emit('arm_status', {'status': '未初始化', 'connected': False})
    
    def _register_wave_socketio_events(self):
        """注册挥手动作的 WebSocket 事件"""
        
        @self.socketio.on('wave_trigger')
        def handle_wave_trigger(data):
            """手动触发挥手"""
            try:
                if not self.wave_controller:
                    emit('wave_error', {'message': '挥手控制器未初始化'})
                    return
                
                force = data.get('force', False)
                success = self.wave_controller.trigger(force=force)
                emit('wave_result', {
                    'success': success,
                    'forced': force,
                    'stats': self.wave_controller.get_stats()
                })
            except Exception as e:
                emit('wave_error', {'message': str(e)})
        
        @self.socketio.on('wave_set_interval')
        def handle_set_interval(data):
            """设置触发间隔"""
            try:
                if not self.wave_controller:
                    emit('wave_error', {'message': '挥手控制器未初始化'})
                    return
                
                interval = data.get('interval', 60)
                new_interval = self.wave_controller.set_interval(interval)
                emit('wave_config', {
                    'min_interval': new_interval,
                    'message': f'触发间隔已设置为 {new_interval}秒'
                })
            except Exception as e:
                emit('wave_error', {'message': str(e)})
        
        @self.socketio.on('wave_get_status')
        def handle_get_status():
            """获取状态"""
            try:
                if not self.wave_controller:
                    emit('wave_status', {'error': '挥手控制器未初始化'})
                    return
                
                emit('wave_status', self.wave_controller.get_stats())
            except Exception as e:
                emit('wave_error', {'message': str(e)})
        
        @self.socketio.on('wave_stop')
        def handle_stop():
            """停止动作"""
            try:
                if self.wave_controller:
                    self.wave_controller.stop()
                emit('wave_status', {
                    **(self.wave_controller.get_stats() if self.wave_controller else {}),
                    'message': '动作已停止'
                })
            except Exception as e:
                emit('wave_error', {'message': str(e)})
        
        @self.socketio.on('wave_reset_stats')
        def handle_reset_stats():
            """重置统计"""
            try:
                if self.wave_controller:
                    self.wave_controller.reset_stats()
                emit('wave_status', self.wave_controller.get_stats() if self.wave_controller else {})
            except Exception as e:
                emit('wave_error', {'message': str(e)})
    
    def init_components(self) -> bool:
        """初始化系统组件"""
        try:
            self.log("正在初始化系统组件...")
            
            # 摄像头
            self.log("初始化摄像头...")
            self.camera = Camera(
                source=self.config.get("camera_source", "/dev/video_header"),
                width=self.config.get("width", 640),
                height=self.config.get("height", 360),
                fps=self.config.get("fps", 30)
            )
            if not self.camera.open():
                self.log("摄像头打开失败", "error")
                return False
            
            # 人体检测器
            self.log("初始化人体检测器...")
            self.detector = HumanDetector(
                model_path=self.config.get("yolo_model", "yolov8n.pt"),
                confidence_threshold=self.config.get("confidence_threshold", 0.5),
                device="cpu"
            )
            
            # 人脸识别器
            self.log("初始化人脸识别器...")
            self.face_recognizer = FaceRecognizer(
                face_db_path=self.config.get("face_db_path", "data/face_database.pkl"),
                recognition_threshold=self.config.get("recognition_threshold", 0.6)
            )
            
            # 迎宾逻辑
            self.log("初始化迎宾逻辑...")
            self.greeter = GreeterLogic(
                welcome_distance=self.config.get("welcome_distance", 2.0),
                min_greet_interval=self.config.get("min_greet_interval", 10),
                follow_timeout=self.config.get("follow_timeout", 5),
                lost_timeout=self.config.get("lost_timeout", 3),
                enable_ptz=self.config.get("enable_ptz", True),
                frame_width=self.config.get("width", 640),
                frame_height=self.config.get("height", 360)
            )
            self.greeter.on_greet = self._on_greet
            self.greeter.on_person_lost = self._on_person_lost
            self.greeter.on_ptz_move = self._on_ptz_move
            
            # 注册机械臂状态回调
            # 注册机械臂状态回调 (仅在启用时)
            if self.arm_controller and hasattr(self.arm_controller, 'on_state_change'):
                self.arm_controller.on_state_change = self._on_arm_state_change
            
            # 可视化
            self.visualizer = Visualizer(
                width=self.config.get("width", 640),
                height=self.config.get("height", 360)
            )
            
            # 初始化机械臂控制器 (注意: 禁用自动连接，避免与 Flask 冲突)
            # 挥手动作通过独立子进程执行，不使用此控制器
            self.log("初始化机械臂控制器...")
            if self.config.get("enable_arm", False):  # 默认禁用，避免冲突
                try:
                    # 延迟导入，避免启动时加载 PallasSDK
                    from arm_controller import MockArmController
                    
                    arm_ip = self.config.get("arm_ip", "192.168.3.100")
                    use_mock = self.config.get("mock_arm", True)  # 默认使用模拟模式
                    
                    if use_mock:
                        self.arm_controller = MockArmController(ip=arm_ip)
                        self.arm_controller.connect()
                        self.log("机械臂使用模拟模式", "info")
                        self.system_status['arm_status'] = '模拟模式'
                        self.system_status['arm_connected'] = True
                    else:
                        # 警告: 真实机械臂连接可能导致 Flask 崩溃
                        self.log("警告: 真实机械臂连接与 Flask 有冲突，已禁用", "warning")
                        self.arm_controller = None
                        self.system_status['arm_status'] = '已禁用(冲突)'
                        self.system_status['arm_connected'] = False
                except Exception as e:
                    self.log(f"机械臂初始化失败: {e}", "warning")
                    self.system_status['arm_status'] = '不可用'
                    self.system_status['arm_connected'] = False
            else:
                self.log("机械臂控制已禁用 (挥手动作仍可用)", "info")
                self.system_status['arm_status'] = '已禁用'
                self.system_status['arm_connected'] = False
            
            # 初始化挥手动作控制器
            self.log("初始化挥手动作控制器...")
            if self.config.get("enable_wave_action", True):
                try:
                    wave_interval = self.config.get("wave_interval", 60)
                    use_mock = self.config.get("mock_wave", False)
                    # 使用完全独立的脚本，避免与 Flask 冲突
                    wave_script = self.config.get("wave_script", "/home/aidlux/human_detection/src/wave_hand_safe.py")
                    audio_file = self.config.get("audio_file", "/home/aidlux/auto.mp3")
                    
                    if use_mock:
                        self.wave_controller = MockWaveActionController(
                            min_interval=wave_interval
                        )
                        self.log("挥手动作控制器使用模拟模式", "info")
                    else:
                        # 使用简化版控制器，更可靠
                        from wave_action_simple import SimpleWaveActionController
                        self.wave_controller = SimpleWaveActionController(
                            audio_file=audio_file,
                            min_interval=wave_interval
                        )
                        self.log(f"挥手动作控制器初始化完成(简化版)，触发间隔: {wave_interval}秒", "success")
                    
                    # 设置回调
                    self.wave_controller.on_trigger = self._on_wave_trigger
                    self.wave_controller.on_complete = self._on_wave_complete
                    
                    # 注册 WebSocket 事件
                    self._register_wave_socketio_events()
                    
                    self.log("挥手动作联动已启用: 检测到人→原点→准备→挥手→原点+音频", "success")
                    
                except Exception as e:
                    self.log(f"挥手动作控制器初始化失败: {e}", "warning")
                    self.wave_controller = None
            
            self.log("系统组件初始化完成")
            return True
            
        except Exception as e:
            self.log(f"初始化失败: {e}", "error")
            return False
    
    def start_processing(self) -> bool:
        """启动处理线程"""
        if self.is_running:
            return True
        
        if not self.init_components():
            return False
        
        self.is_running = True
        self.processing_thread = threading.Thread(target=self._processing_loop, daemon=True)
        self.processing_thread.start()
        self.log("视频处理已启动")
        return True
    
    def stop_processing(self):
        """停止处理线程"""
        self.is_running = False
        if self.processing_thread:
            self.processing_thread.join(timeout=2.0)
        
        if self.camera:
            self.camera.release()
        
        # 断开机械臂
        if self.arm_controller:
            self.arm_controller.disconnect()
            self.arm_controller = None
        
        # 停止挥手动作
        if self.wave_controller:
            self.wave_controller.stop()
            self.wave_controller = None
        
        self.log("视频处理已停止")
    
    def _processing_loop(self):
        """视频处理循环"""
        self.frame_count = 0
        self.last_fps_time = time.time()
        
        while self.is_running:
            try:
                # 读取帧
                frame = self.camera.read()
                if frame is None:
                    continue
                
                self.frame_count += 1
                
                # 人体检测 (每N帧检测一次，提高帧率)
                persons = []
                current_time = time.time()
                
                if self.frame_count % self.detect_interval == 0:
                    persons = self.detector.detect(frame, track=True)
                    if persons:
                        self.last_detection_time = current_time
                        self.last_persons = persons
                else:
                    # 平滑机制：如果距离上次检测时间较短，保持上一帧结果
                    if current_time - self.last_detection_time < self.detection_persist_time:
                        persons = self.last_persons
                
                # 获取最近的人体
                closest = None
                face = None
                recognized_name = None
                
                if persons:
                    closest = min(persons, key=lambda p: p.get("distance", 999))
                    
                    # 触发挥手动作 (检测到有人且距离在范围内)
                    if self.wave_controller and closest:
                        distance = closest.get("distance", 999)
                        welcome_distance = self.config.get("welcome_distance", 10.0)
                        
                        # 限制日志频率 (每10秒最多输出一次)
                        current_time = time.time()
                        last_wave_log = getattr(self, '_last_wave_log', 0)
                        can_log = (current_time - last_wave_log) >= 10
                        
                        if distance <= welcome_distance:
                            # 每次检测都播放音频 (独立触发)
                            try:
                                audio_manager = get_audio_manager()
                                default_audio = audio_manager.get_default_audio()
                                if default_audio:
                                    self.socketio.emit('play_audio', {
                                        'url': default_audio['url'],
                                        'name': default_audio['name']
                                    })
                                    if can_log:
                                        self.log(f"[音频] 播放: {default_audio['name']}", "info")
                            except Exception as e:
                                self.log(f'[音频] 发送失败: {e}', 'warning')
                            
                            # 触发挥手动作
                            can_trigger = self.wave_controller.can_trigger()
                            
                            if can_trigger:
                                triggered = self.wave_controller.trigger()
                                if triggered:
                                    if can_log:
                                        self.log(f"[挥手] 已触发 (距离: {distance:.2f}m)", "success")
                                else:
                                    if can_log:
                                        self.log(f"[挥手] 触发失败", "warning")
                            else:
                                if can_log:
                                    self.log(f"[挥手] 动作执行中，跳过", "info")
                        else:
                            # 人在检测范围内但超出迎宾距离
                            if can_log:
                                self.log(f"[挥手] 距离过远: {distance:.1f}m", "debug")
                                self._last_wave_log = current_time
                    
                    # 人脸识别(降低频率，提高性能)
                    if self.frame_count % (self.detect_interval * 2) == 0:
                        x1, y1, x2, y2 = closest["bbox"]
                        face_roi = frame[max(0, y1-20):min(frame.shape[0], y2), 
                                       max(0, x1):min(frame.shape[1], x2)]
                        if face_roi.size > 0:
                            faces = self.face_recognizer.detect_faces(face_roi)
                            if faces:
                                face = faces[0]
                                fx1, fy1, fx2, fy2 = face["bbox"]
                                face["bbox"] = (x1 + fx1, y1 - 20 + fy1, 
                                              x1 + fx2, y1 - 20 + fy2)
                                recognized_name, _ = self.face_recognizer.recognize(face)
                
                # 迎宾逻辑
                action_result = self.greeter.process(closest, face, recognized_name)
                
                # 可视化
                display_frame = frame.copy()
                
                # 绘制检测框
                if persons:
                    display_frame = self.visualizer.draw_detection(display_frame, persons)
                
                # 绘制人脸
                if face:
                    display_frame = self.visualizer.draw_face(
                        display_frame, [face], [recognized_name]
                    )
                
                # 绘制信息面板
                fps = self._update_fps()
                state_text = self.greeter.get_state().value
                stats = self.greeter.get_stats()
                
                # 添加云台角度
                if self.config.get("enable_ptz", True):
                    pan = getattr(self, 'current_pan', 0)
                    tilt = getattr(self, 'current_tilt', 0)
                    state_text += f" | 云台:{pan:.0f},{tilt:.0f}"
                
                display_frame = self.visualizer.draw_info_panel(
                    display_frame, state_text, fps, stats
                )
                
                # 更新最新帧
                self.latest_frame = display_frame
                self.latest_detections = persons
                
                # 更新系统状态
                arm_status = '未连接'
                if self.arm_controller:
                    arm_status = self.arm_controller.get_state().value
                
                self.system_status = {
                    'state': self.greeter.get_state().value,
                    'fps': round(fps, 1),
                    'persons': len(persons),
                    'ptz': f"{getattr(self, 'current_pan', 0):.0f},{getattr(self, 'current_tilt', 0):.0f}",
                    'visitors': stats.get('total_visitors', 0),
                    'arm_status': arm_status,
                    'arm_connected': self.system_status.get('arm_connected', False),
                    'timestamp': datetime.now().strftime('%H:%M:%S')
                }
                
                # 推送视频帧 (降低频率，降低带宽)
                if self.frame_count % self.push_interval == 0:
                    self._push_frame(display_frame)
                
                # 推送状态 (每30帧推送一次)
                if self.frame_count % 30 == 0:
                    self.socketio.emit('status_update', self.system_status)
                
            except Exception as e:
                self.log(f"处理错误: {e}", "error")
                time.sleep(0.1)
    
    def _update_fps(self) -> float:
        """更新 FPS"""
        current_time = time.time()
        elapsed = current_time - self.last_fps_time
        
        if elapsed >= 1.0:
            self.current_fps = self.frame_count / elapsed
            self.frame_count = 0
            self.last_fps_time = current_time
        
        return self.current_fps
    
    def _push_frame(self, frame: np.ndarray):
        """推送视频帧到 Web"""
        try:
            # 压缩图像(降低质量提高帧率)
            encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), self.jpeg_quality]
            
            # 降低分辨率推送(可选)
            push_frame = frame
            if frame.shape[1] > 640:  # 如果宽度大于640，降低分辨率
                push_frame = cv2.resize(frame, (640, 360))
            
            _, buffer = cv2.imencode('.jpg', push_frame, encode_param)
            
            # 转为 base64
            jpg_as_text = base64.b64encode(buffer).decode('utf-8')
            
            # 发送
            self.socketio.emit('video_frame', {
                'image': f'data:image/jpeg;base64,{jpg_as_text}',
                'timestamp': datetime.now().strftime('%H:%M:%S')
            })
        except Exception as e:
            pass  # 忽略推送错误
    
    def _on_greet(self, name: str, message: str, is_new: bool):
        """迎宾回调"""
        self.log(f"[迎宾] {message}")
        self.socketio.emit('greeting', {
            'message': message,
            'name': name,
            'is_new': is_new
        })
        
        # 触发机械臂欢迎动作
        if self.arm_controller and self.arm_controller.is_ready():
            if is_new:
                # 新朋友 - 执行欢迎动作
                self.log("[机械臂] 执行欢迎动作", "info")
                self.arm_controller.welcome_guest()
            else:
                # 老朋友 - 简单挥手
                self.log("[机械臂] 执行挥手动作", "info")
                self.arm_controller.wave_hand()
    
    def _on_person_lost(self):
        """人员丢失回调"""
        self.log("目标丢失，返回待机")
    
    def _on_ptz_move(self, pan: float, tilt: float):
        """云台移动回调"""
        self.current_pan = pan
        self.current_tilt = tilt
    
    def _on_arm_state_change(self, state):
        """机械臂状态变化回调"""
        status_text = state.value
        self.system_status['arm_status'] = status_text
        self.log(f"[机械臂] 状态: {status_text}")
        self.socketio.emit('arm_status', {
            'status': status_text,
            'connected': state.name != 'DISCONNECTED'
        })
    
    def _on_wave_trigger(self):
        """挥手动作触发回调"""
        self.log("[挥手动作] 开始执行...", "info")
        self.socketio.emit('wave_status', {
            **self.wave_controller.get_stats(),
            'message': '挥手动作开始执行'
        })
    
    def _on_wave_complete(self, success: bool):
        """挥手动作完成回调"""
        msg = '挥手动作执行成功' if success else '挥手动作执行失败'
        self.log(f"[挥手动作] {msg}", 'success' if success else 'error')
        self.socketio.emit('wave_status', {
            **self.wave_controller.get_stats(),
            'message': msg,
            'success': success
        })
    
    def run(self):
        """运行服务器"""
        self.log(f"启动 Web GUI 服务器: http://{self.host}:{self.port}")
        print(f"\n请在浏览器中打开: http://{self.host}:{self.port}")
        print("按 Ctrl+C 停止服务器\n")
        
        try:
            self.socketio.run(self.app, host=self.host, port=self.port, debug=False, allow_unsafe_werkzeug=True)
        except KeyboardInterrupt:
            self.stop_processing()
            self.log("服务器已停止")


def create_html_template():
    """创建 HTML 模板"""
    template_dir = os.path.join(os.path.dirname(__file__), 'templates')
    os.makedirs(template_dir, exist_ok=True)
    
    html_content = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>智能迎宾机器人 - 监控系统</title>
    <script src="https://cdn.socket.io/4.5.4/socket.io.min.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            min-height: 100vh;
            color: #fff;
        }
        
        .header {
            background: rgba(0,0,0,0.3);
            padding: 15px 30px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }
        
        .header h1 {
            font-size: 24px;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .status-bar {
            display: flex;
            gap: 20px;
            font-size: 14px;
        }
        
        .status-item {
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .status-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #10b981;
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        
        .main-container {
            display: grid;
            grid-template-columns: 1fr 350px;
            gap: 20px;
            padding: 20px;
            max-width: 1600px;
            margin: 0 auto;
        }
        
        .video-section {
            background: rgba(0,0,0,0.3);
            border-radius: 12px;
            overflow: hidden;
            position: relative;
        }
        
        .video-container {
            position: relative;
            width: 100%;
            padding-bottom: 56.25%; /* 16:9 */
            background: #000;
        }
        
        .video-container img {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            object-fit: contain;
        }
        
        .video-placeholder {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            color: #666;
        }
        
        .video-placeholder .icon {
            font-size: 48px;
            margin-bottom: 10px;
        }
        
        .control-panel {
            display: flex;
            gap: 10px;
            padding: 15px;
            background: rgba(0,0,0,0.2);
            border-top: 1px solid rgba(255,255,255,0.1);
        }
        
        .btn {
            padding: 10px 20px;
            border: none;
            border-radius: 6px;
            font-size: 14px;
            cursor: pointer;
            transition: all 0.3s;
            display: flex;
            align-items: center;
            gap: 5px;
        }
        
        .btn-primary {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        
        .btn-success {
            background: #10b981;
            color: white;
        }
        
        .btn-danger {
            background: #ef4444;
            color: white;
        }
        
        .btn-secondary {
            background: rgba(255,255,255,0.1);
            color: white;
        }
        
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        }
        
        .btn:disabled {
            opacity: 0.5;
            cursor: not-allowed;
            transform: none;
        }
        
        .sidebar {
            display: flex;
            flex-direction: column;
            gap: 20px;
        }
        
        .card {
            background: rgba(0,0,0,0.3);
            border-radius: 12px;
            padding: 20px;
            border: 1px solid rgba(255,255,255,0.1);
        }
        
        .card h3 {
            font-size: 16px;
            margin-bottom: 15px;
            color: #a0aec0;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
        }
        
        .stat-item {
            background: rgba(255,255,255,0.05);
            padding: 15px;
            border-radius: 8px;
            text-align: center;
        }
        
        .stat-value {
            font-size: 24px;
            font-weight: bold;
            color: #667eea;
        }
        
        .stat-label {
            font-size: 12px;
            color: #a0aec0;
            margin-top: 5px;
        }
        
        .log-container {
            background: rgba(0,0,0,0.5);
            border-radius: 8px;
            padding: 10px;
            height: 300px;
            overflow-y: auto;
            font-family: 'Courier New', monospace;
            font-size: 12px;
        }
        
        .log-entry {
            padding: 4px 0;
            border-bottom: 1px solid rgba(255,255,255,0.05);
        }
        
        .log-time {
            color: #6b7280;
        }
        
        .log-info { color: #60a5fa; }
        .log-success { color: #34d399; }
        .log-warning { color: #fbbf24; }
        .log-error { color: #f87171; }
        
        .greeting-banner {
            position: fixed;
            bottom: 30px;
            left: 50%;
            transform: translateX(-50%) translateY(100px);
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px 40px;
            border-radius: 50px;
            font-size: 20px;
            font-weight: bold;
            box-shadow: 0 10px 40px rgba(102, 126, 234, 0.4);
            transition: transform 0.5s ease;
            z-index: 1000;
        }
        
        .greeting-banner.show {
            transform: translateX(-50%) translateY(0);
        }
        
        .register-modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.8);
            z-index: 2000;
            align-items: center;
            justify-content: center;
        }
        
        .register-modal.show {
            display: flex;
        }
        
        .modal-content {
            background: #1a1a2e;
            padding: 30px;
            border-radius: 12px;
            width: 400px;
        }
        
        .modal-content h3 {
            margin-bottom: 20px;
        }
        
        .modal-content input {
            width: 100%;
            padding: 12px;
            border: 1px solid rgba(255,255,255,0.2);
            border-radius: 6px;
            background: rgba(0,0,0,0.3);
            color: white;
            font-size: 16px;
            margin-bottom: 20px;
        }
        
        .modal-buttons {
            display: flex;
            gap: 10px;
            justify-content: flex-end;
        }
        
        @media (max-width: 1200px) {
            .main-container {
                grid-template-columns: 1fr;
            }
            
            .sidebar {
                flex-direction: row;
                flex-wrap: wrap;
            }
            
            .card {
                flex: 1;
                min-width: 300px;
            }
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🤖 智能迎宾机器人监控系统</h1>
        <div class="status-bar">
            <div class="status-item">
                <div class="status-dot" id="statusDot"></div>
                <span id="statusText">离线</span>
            </div>
            <div class="status-item">
                <span>FPS: <strong id="fpsValue">0</strong></span>
            </div>
            <div class="status-item">
                <span>检测: <strong id="personCount">0</strong>人</span>
            </div>
        </div>
    </div>
    
    <div class="main-container">
        <div class="video-section">
            <div class="video-container">
                <div class="video-placeholder" id="videoPlaceholder">
                    <div class="icon">📹</div>
                    <div>点击"开始监控"启动视频流</div>
                </div>
                <img id="videoStream" style="display: none;">
            </div>
            <div class="control-panel">
                <button class="btn btn-success" id="btnStart" onclick="startSystem()">
                    ▶️ 开始监控
                </button>
                <button class="btn btn-danger" id="btnStop" onclick="stopSystem()" disabled>
                    ⏹️ 停止
                </button>
                <button class="btn btn-secondary" onclick="takeSnapshot()">
                    📷 截图
                </button>
                <button class="btn btn-primary" onclick="showRegisterModal()">
                    👤 注册人脸
                </button>
            </div>
        </div>
        
        <div class="sidebar">
            <div class="card">
                <h3>📊 统计数据</h3>
                <div class="stats-grid">
                    <div class="stat-item">
                        <div class="stat-value" id="statVisitors">0</div>
                        <div class="stat-label">总访客</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value" id="statKnown">0</div>
                        <div class="stat-label">已知访客</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value" id="statUnknown">0</div>
                        <div class="stat-label">未知访客</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value" id="statPTZ">0°</div>
                        <div class="stat-label">云台角度</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value" id="statArm" style="font-size: 14px;">未连接</div>
                        <div class="stat-label">机械臂</div>
                    </div>
                </div>
            </div>
            
            <div class="card">
                <h3>📝 系统日志</h3>
                <div class="log-container" id="logContainer">
                    <div class="log-entry">系统就绪，等待启动...</div>
                </div>
            </div>
            
            <div class="card">
                <h3>🦾 机械臂控制</h3>
                <div class="arm-status" id="armStatusText" style="text-align: center; padding: 10px; background: rgba(255,255,255,0.05); border-radius: 6px; margin-bottom: 15px; color: #a0aec0;">
                    状态: <span id="armStatusValue">未连接</span>
                </div>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px;">
                    <button class="btn btn-secondary" id="btnArmConnect" onclick="armConnect()" style="padding: 8px; font-size: 12px;">
                        🔌 连接
                    </button>
                    <button class="btn btn-secondary" id="btnArmHome" onclick="armHome()" style="padding: 8px; font-size: 12px;" disabled>
                        🏠 回原点
                    </button>
                    <button class="btn btn-primary" id="btnArmWave" onclick="armWave()" style="padding: 8px; font-size: 12px;" disabled>
                        👋 挥手
                    </button>
                    <button class="btn btn-primary" id="btnArmWelcome" onclick="armWelcome()" style="padding: 8px; font-size: 12px;" disabled>
                        🎉 欢迎
                    </button>
                    <button class="btn btn-secondary" id="btnArmOpen" onclick="armGripper('open')" style="padding: 8px; font-size: 12px;" disabled>
                        ✋ 张开夹爪
                    </button>
                    <button class="btn btn-secondary" id="btnArmClose" onclick="armGripper('close')" style="padding: 8px; font-size: 12px;" disabled>
                        ✊ 闭合夹爪
                    </button>
                </div>
            </div>
            
            <div class="card">
                <h3>👋 挥手动作</h3>
                <div style="margin-bottom: 15px;">
                    <label style="display: block; margin-bottom: 5px; color: #a0aec0; font-size: 12px;">触发间隔 (秒)</label>
                    <div style="display: flex; gap: 8px;">
                        <input type="number" id="waveIntervalInput" value="60" min="0" max="3600" 
                               style="flex: 1; padding: 8px; background: rgba(0,0,0,0.3); border: 1px solid rgba(255,255,255,0.2); border-radius: 6px; color: white; font-size: 12px;">
                        <button class="btn btn-secondary" onclick="updateWaveInterval()" style="padding: 8px 12px; font-size: 12px;">
                            设置
                        </button>
                    </div>
                </div>
                
                <!-- 音频选择 -->
                <div style="margin-bottom: 15px;">
                    <label style="display: block; margin-bottom: 5px; color: #a0aec0; font-size: 12px;">提示音频</label>
                    <select id="audioSelect" onchange="onAudioChange()" 
                            style="width: 100%; padding: 8px; background: rgba(0,0,0,0.3); border: 1px solid rgba(255,255,255,0.2); border-radius: 6px; color: white; font-size: 12px;">
                        <option>加载中...</option>
                    </select>
                    <!-- 音频播放器 -->
                    <audio id="audioPlayer" preload="auto" style="width: 100%; margin-top: 8px; height: 30px;">
                        您的浏览器不支持音频播放
                    </audio>
                </div>
                
                <div class="wave-status" id="waveStatusText" style="text-align: center; padding: 10px; background: rgba(255,255,255,0.05); border-radius: 6px; margin-bottom: 15px; color: #a0aec0; font-size: 12px;">
                    状态: <span id="waveStatusValue">待机</span>
                </div>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px;">
                    <button class="btn btn-primary" id="btnWaveTrigger" onclick="waveTrigger()" style="padding: 8px; font-size: 12px;">
                        👋 触发挥手
                    </button>
                    <button class="btn btn-secondary" id="btnWaveForce" onclick="waveForceTrigger()" style="padding: 8px; font-size: 12px;">
                        ⚡ 强制触发
                    </button>
                    <button class="btn btn-secondary" id="btnWaveStop" onclick="waveStop()" style="padding: 8px; font-size: 12px;">
                        ⏹️ 停止动作
                    </button>
                    <button class="btn btn-secondary" id="btnWaveReset" onclick="waveResetStats()" style="padding: 8px; font-size: 12px;">
                        🔄 重置统计
                    </button>
                </div>
                <div style="margin-top: 15px; padding: 10px; background: rgba(0,0,0,0.2); border-radius: 6px; font-size: 11px;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                        <span style="color: #a0aec0;">触发次数:</span>
                        <span id="waveTriggerCount" style="color: #667eea;">0</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                        <span style="color: #a0aec0;">跳过次数:</span>
                        <span id="waveSkipCount" style="color: #fbbf24;">0</span>
                    </div>
                    <div style="display: flex; justify-content: space-between;">
                        <span style="color: #a0aec0;">剩余冷却:</span>
                        <span id="waveCooldown" style="color: #10b981;">0秒</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <div class="greeting-banner" id="greetingBanner">
        欢迎光临！
    </div>
    
    <div class="register-modal" id="registerModal">
        <div class="modal-content">
            <h3>注册新访客</h3>
            <input type="text" id="registerName" placeholder="请输入姓名..." maxlength="20">
            <div class="modal-buttons">
                <button class="btn btn-secondary" onclick="hideRegisterModal()">取消</button>
                <button class="btn btn-primary" onclick="registerFace()">确认注册</button>
            </div>
        </div>
    </div>
    
    <script>
        // Socket.IO 连接
        const socket = io({
            transports: ['polling'],
            upgrade: false,
            reconnection: true,
            reconnectionAttempts: 10,
            reconnectionDelay: 1000
        });
        
        let isRunning = false;
        let audioFiles = [];
        let currentAudio = null;
        
        // 音频列表更新
        socket.on('audio_list', function(data) {
            audioFiles = data.audio_files || [];
            const select = document.getElementById('audioSelect');
            
            if (audioFiles.length === 0) {
                select.innerHTML = '<option>无音频文件</option>';
                return;
            }
            
            select.innerHTML = '';
            audioFiles.forEach(function(audio) {
                const option = document.createElement('option');
                option.value = audio.url;
                option.textContent = audio.name;
                select.appendChild(option);
            });
            
            // 设置默认选中
            if (data.default) {
                select.value = data.default.url;
                loadAudio(data.default.url);
            }
            
            addLog(`已加载 ${audioFiles.length} 个音频文件`, 'success');
        });
        
        // 播放音频命令
        socket.on('play_audio', function(data) {
            console.log('收到播放命令:', data);
            addLog(`播放音频: ${data.name}`, 'info');
            playAudio(data.url);
        });
        
        // 加载音频到播放器
        function loadAudio(url) {
            const player = document.getElementById('audioPlayer');
            player.src = url;
            player.load();
        }
        
        // 播放音频
        function playAudio(url) {
            const player = document.getElementById('audioPlayer');
            if (url && player.src !== url) {
                player.src = url;
                player.load();
            }
            player.play().catch(function(e) {
                console.error('播放失败:', e);
                addLog('音频播放失败(可能需要用户交互)', 'warning');
            });
        }
        
        // 音频选择变化
        function onAudioChange() {
            const select = document.getElementById('audioSelect');
            const url = select.value;
            loadAudio(url);
            addLog(`已选择音频: ${select.options[select.selectedIndex].text}`, 'info');
        }
        
        // 连接成功
        socket.on('connect', function() {
            console.log('Connected to server');
            addLog('已连接到服务器', 'success');
        });
        
        // 断开连接
        socket.on('disconnect', function() {
            console.log('Disconnected from server');
            addLog('与服务器断开连接', 'warning');
            updateStatus('离线', false);
        });
        
        // 视频帧
        socket.on('video_frame', function(data) {
            const img = document.getElementById('videoStream');
            const placeholder = document.getElementById('videoPlaceholder');
            
            img.src = data.image;
            img.style.display = 'block';
            placeholder.style.display = 'none';
        });
        
        // 状态更新
        socket.on('status_update', function(status) {
            document.getElementById('fpsValue').textContent = status.fps;
            document.getElementById('personCount').textContent = status.persons;
            document.getElementById('statVisitors').textContent = status.visitors;
            
            // 解析云台角度
            const ptz = status.ptz.split(',');
            document.getElementById('statPTZ').textContent = 
                `P:${parseInt(ptz[0])}° T:${parseInt(ptz[1])}°`;
        });
        
        // 日志更新
        socket.on('log_update', function(log) {
            addLog(log.message, log.level);
        });
        
        // 系统启动
        socket.on('system_started', function() {
            isRunning = true;
            updateStatus('运行中', true);
            document.getElementById('btnStart').disabled = true;
            document.getElementById('btnStop').disabled = false;
            addLog('系统启动成功', 'success');
            
            // 定期获取挥手状态
            startWaveStatusUpdate();
        });
        
        // 定期获取挥手状态
        let waveStatusInterval;
        function startWaveStatusUpdate() {
            if (waveStatusInterval) clearInterval(waveStatusInterval);
            waveStatusInterval = setInterval(function() {
                if (isRunning) {
                    socket.emit('wave_get_status');
                }
            }, 1000);  // 每秒更新一次
        }
        
        // 系统停止
        socket.on('system_stopped', function() {
            isRunning = false;
            updateStatus('已停止', false);
            document.getElementById('btnStart').disabled = false;
            document.getElementById('btnStop').disabled = true;
            addLog('系统已停止', 'info');
        });
        
        // 错误
        socket.on('system_error', function(data) {
            addLog('错误: ' + data.message, 'error');
        });
        
        // 迎宾
        socket.on('greeting', function(data) {
            showGreeting(data.message);
            addLog('迎宾: ' + data.message, 'success');
            
            // 更新统计
            if (data.is_new) {
                document.getElementById('statKnown').textContent = 
                    parseInt(document.getElementById('statKnown').textContent) + 1;
            } else {
                document.getElementById('statUnknown').textContent = 
                    parseInt(document.getElementById('statUnknown').textContent) + 1;
            }
        });
        
        // 注册结果
        socket.on('register_result', function(data) {
            if (data.success) {
                addLog('人脸注册成功: ' + data.name, 'success');
                hideRegisterModal();
                alert('注册成功: ' + data.name);
            } else {
                addLog('注册失败: ' + data.message, 'error');
                alert('注册失败: ' + data.message);
            }
        });
        
        // 启动系统
        function startSystem() {
            socket.emit('start_system');
        }
        
        // 停止系统
        function stopSystem() {
            socket.emit('stop_system');
            document.getElementById('videoStream').style.display = 'none';
            document.getElementById('videoPlaceholder').style.display = 'flex';
        }
        
        // 截图
        function takeSnapshot() {
            const img = document.getElementById('videoStream');
            if (img.style.display === 'none') {
                alert('请先启动监控');
                return;
            }
            
            const link = document.createElement('a');
            link.download = 'snapshot_' + new Date().getTime() + '.jpg';
            link.href = img.src;
            link.click();
            addLog('截图已保存', 'success');
        }
        
        // 显示注册弹窗
        function showRegisterModal() {
            if (!isRunning) {
                alert('请先启动监控');
                return;
            }
            document.getElementById('registerModal').classList.add('show');
            document.getElementById('registerName').focus();
        }
        
        // 隐藏注册弹窗
        function hideRegisterModal() {
            document.getElementById('registerModal').classList.remove('show');
            document.getElementById('registerName').value = '';
        }
        
        // 注册人脸
        function registerFace() {
            const name = document.getElementById('registerName').value.trim();
            if (!name) {
                alert('请输入姓名');
                return;
            }
            socket.emit('register_face', {name: name});
        }
        
        // 更新状态显示
        function updateStatus(text, isOnline) {
            document.getElementById('statusText').textContent = text;
            const dot = document.getElementById('statusDot');
            dot.style.background = isOnline ? '#10b981' : '#ef4444';
            dot.style.animation = isOnline ? 'pulse 2s infinite' : 'none';
        }
        
        // ========== 机械臂控制 ==========
        
        // 机械臂状态更新
        socket.on('arm_status', function(data) {
            const statusEl = document.getElementById('armStatusValue');
            const statArmEl = document.getElementById('statArm');
            
            statusEl.textContent = data.status;
            statArmEl.textContent = data.status;
            
            // 根据状态更新颜色
            if (data.connected) {
                statusEl.style.color = '#10b981';
                statArmEl.style.color = '#10b981';
            } else {
                statusEl.style.color = '#ef4444';
                statArmEl.style.color = '#ef4444';
            }
            
            // 更新按钮状态
            updateArmButtons(data.status === 'ready');
        });
        
        // 机械臂操作结果
        socket.on('arm_result', function(data) {
            if (data.success) {
                addLog('机械臂操作成功: ' + data.action, 'success');
            } else {
                addLog('机械臂操作失败: ' + (data.message || data.action), 'error');
            }
        });
        
        // 更新机械臂按钮状态
        function updateArmButtons(enabled) {
            document.getElementById('btnArmHome').disabled = !enabled;
            document.getElementById('btnArmWave').disabled = !enabled;
            document.getElementById('btnArmWelcome').disabled = !enabled;
            document.getElementById('btnArmOpen').disabled = !enabled;
            document.getElementById('btnArmClose').disabled = !enabled;
        }
        
        // 连接机械臂
        function armConnect() {
            socket.emit('arm_connect');
            addLog('正在连接机械臂...', 'info');
        }
        
        // 机械臂回原点
        function armHome() {
            socket.emit('arm_home');
            addLog('机械臂回原点', 'info');
        }
        
        // 挥手动作
        function armWave() {
            socket.emit('arm_wave');
            addLog('执行挥手动作', 'info');
        }
        
        // 欢迎动作
        function armWelcome() {
            socket.emit('arm_welcome');
            addLog('执行欢迎动作', 'info');
        }
        
        // 夹爪控制
        function armGripper(action) {
            socket.emit('arm_gripper', {action: action});
            addLog('夹爪' + (action === 'open' ? '张开' : '闭合'), 'info');
        }
        
        // ========== 挥手动作控制 ==========
        
        // 挥手状态更新
        socket.on('wave_status', function(data) {
            const statusEl = document.getElementById('waveStatusValue');
            
            // 更新状态文本
            if (data.is_running) {
                statusEl.textContent = '执行中...';
                statusEl.style.color = '#fbbf24';
            } else if (data.remaining_cooldown > 0) {
                statusEl.textContent = '冷却中';
                statusEl.style.color = '#f87171';
            } else {
                statusEl.textContent = '待机';
                statusEl.style.color = '#10b981';
            }
            
            // 更新统计
            document.getElementById('waveTriggerCount').textContent = data.trigger_count || 0;
            document.getElementById('waveSkipCount').textContent = data.skip_count || 0;
            document.getElementById('waveCooldown').textContent = 
                (data.remaining_cooldown || 0).toFixed(1) + '秒';
            
            // 显示消息
            if (data.message) {
                addLog(data.message, data.success !== undefined ? (data.success ? 'success' : 'error') : 'info');
            }
        });
        
        // 挥手配置更新
        socket.on('wave_config', function(data) {
            addLog(data.message || '配置已更新', 'success');
            document.getElementById('waveIntervalInput').value = data.min_interval;
        });
        
        // 触发挥手
        function waveTrigger() {
            socket.emit('wave_trigger', {force: false});
        }
        
        // 强制触发
        function waveForceTrigger() {
            socket.emit('wave_trigger', {force: true});
        }
        
        // 停止动作
        function waveStop() {
            socket.emit('wave_stop');
        }
        
        // 重置统计
        function waveResetStats() {
            socket.emit('wave_reset_stats');
            addLog('统计已重置', 'info');
        }
        
        // 更新触发间隔
        function updateWaveInterval() {
            const interval = parseInt(document.getElementById('waveIntervalInput').value);
            if (isNaN(interval) || interval < 0) {
                alert('请输入有效的间隔时间(秒)');
                return;
            }
            socket.emit('wave_set_interval', {interval: interval});
        }
        
        // 添加日志
        function addLog(message, level) {
            const container = document.getElementById('logContainer');
            const entry = document.createElement('div');
            entry.className = 'log-entry';
            
            const time = new Date().toLocaleTimeString('zh-CN', {hour12: false});
            entry.innerHTML = `<span class="log-time">[${time}]</span> <span class="log-${level}">${message}</span>`;
            
            container.appendChild(entry);
            container.scrollTop = container.scrollHeight;
            
            // 限制日志数量
            while (container.children.length > 100) {
                container.removeChild(container.firstChild);
            }
        }
        
        // 显示迎宾横幅
        let greetingTimeout;
        function showGreeting(message) {
            const banner = document.getElementById('greetingBanner');
            banner.textContent = message;
            banner.classList.add('show');
            
            clearTimeout(greetingTimeout);
            greetingTimeout = setTimeout(() => {
                banner.classList.remove('show');
            }, 5000);
        }
        
        // 按 Enter 确认注册
        document.getElementById('registerName').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                registerFace();
            }
        });
        
        // 点击遮罩关闭弹窗
        document.getElementById('registerModal').addEventListener('click', function(e) {
            if (e.target === this) {
                hideRegisterModal();
            }
        });
    </script>
</body>
</html>'''
    
    template_path = os.path.join(template_dir, 'index.html')
    with open(template_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"HTML 模板已创建: {template_path}")


if __name__ == "__main__":
    # 创建 HTML 模板
    create_html_template()
    
    # 配置 - 优化帧率和画质
    config = {
        "camera_source": "/dev/video_header",
        "width": 640,              # 640x480 画质
        "height": 480,             # 提高分辨率
        "fps": 30,                 # 30fps
        "yolo_model": "yolov8n.pt",
        "confidence_threshold": 0.5,
        "recognition_threshold": 0.6,
        "face_db_path": "data/face_database.pkl",
        "welcome_distance": 10.0,  # 迎宾距离(米)，10米内都触发
        "min_greet_interval": 5,   # 减少迎宾间隔
        "follow_timeout": 5,
        "lost_timeout": 3,
        "enable_ptz": True,
        # 挥手动作配置 - 每次检测都触发
        "enable_wave_action": True,
        "wave_interval": 0,        # 0秒间隔，每次检测都触发挥手
        "audio_file": "/home/aidlux/auto.mp3",
        "mock_wave": False         # False=调用独立脚本
    }
    
    # 创建并运行服务器 (使用随机端口避免冲突)
    import random
    port = random.randint(5000, 9000)
    server = WebGUIServer(config, host='0.0.0.0', port=port)
    server.run()
