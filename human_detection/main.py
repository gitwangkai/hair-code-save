#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能迎宾机器人 - 主程序
整合人体检测、人脸识别和迎宾交互

使用方法:
    python main.py
    
按键:
    q - 退出
    s - 保存截图
    r - 注册当前人脸
    c - 标定距离
"""

import cv2
import numpy as np
import os
import sys
import argparse
import signal
import time

# 添加 src 到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'utils'))

from camera import Camera, list_cameras
from detector import HumanDetector
from face_recognizer import FaceRecognizer
from greeter import GreeterLogic, GreeterState
from visualization import Visualizer
from arm_controller import ArmController, MockArmController


class WelcomeRobot:
    """
    智能迎宾机器人主类
    """
    
    def __init__(self, config: dict):
        """
        初始化迎宾机器人
        
        Args:
            config: 配置字典
        """
        self.config = config
        self.running = False
        
        # 初始化组件
        print("=" * 50)
        print("智能迎宾机器人初始化")
        print("=" * 50)
        
        # 0. 配置
        print(f"\n[配置] 分辨率: {config.get('width', 640)}x{config.get('height', 480)}")
        print(f"       云台追踪: {'启用' if config.get('enable_ptz', True) else '禁用'}")
        
        # 1. 摄像头
        print("\n[1/5] 初始化摄像头...")
        self.camera = Camera(
            source=config.get("camera_source", 0),
            width=config.get("width", 640),
            height=config.get("height", 480),
            fps=config.get("fps", 30)
        )
        
        # 2. 人体检测器
        print("\n[2/5] 初始化人体检测器...")
        self.detector = HumanDetector(
            model_path=config.get("yolo_model", "yolov8n.pt"),
            confidence_threshold=config.get("confidence_threshold", 0.5),
            device="cpu"
        )
        
        # 3. 人脸识别器
        print("\n[3/5] 初始化人脸识别器...")
        self.face_recognizer = FaceRecognizer(
            face_db_path=config.get("face_db_path", "data/face_database.pkl"),
            recognition_threshold=config.get("recognition_threshold", 0.6)
        )
        
        # 4. 迎宾逻辑
        print("\n[4/5] 初始化迎宾逻辑与云台追踪...")
        self.greeter = GreeterLogic(
            welcome_distance=config.get("welcome_distance", 2.0),
            min_greet_interval=config.get("min_greet_interval", 10),
            follow_timeout=config.get("follow_timeout", 5),
            lost_timeout=config.get("lost_timeout", 3),
            enable_ptz=config.get("enable_ptz", True),
            frame_width=config.get("width", 640),
            frame_height=config.get("height", 480)
        )
        
        # 设置回调
        self.greeter.on_greet = self._on_greet
        self.greeter.on_person_lost = self._on_person_lost
        self.greeter.on_ptz_move = self._on_ptz_move
        
        # 云台状态
        self.current_ptz = (0.0, 0.0)
        
        # 6. 机械臂
        self.arm_controller = None
        if config.get("enable_arm", True):
            print("\n[6/6] 初始化机械臂...")
            try:
                arm_ip = config.get("arm_ip", "192.168.3.100")
                use_mock = config.get("mock_arm", False)
                
                if use_mock:
                    self.arm_controller = MockArmController(ip=arm_ip)
                    print("       使用模拟模式")
                else:
                    self.arm_controller = ArmController(ip=arm_ip)
                    print(f"       目标IP: {arm_ip}")
                
                if self.arm_controller.connect():
                    print("       ✓ 机械臂连接成功")
                else:
                    print("       ! 机械臂连接失败，使用模拟模式")
                    self.arm_controller = MockArmController(ip=arm_ip)
                    self.arm_controller.connect()
            except Exception as e:
                print(f"       ! 机械臂初始化失败: {e}")
                self.arm_controller = None
        else:
            print("\n[6/6] 机械臂已禁用")
        
        # 7. 可视化
        print("\n[5/5] 初始化可视化...")
        self.visualizer = Visualizer(
            width=config.get("width", 640),
            height=config.get("height", 480)
        )
        
        print("\n" + "=" * 50)
        print("初始化完成！")
        print("=" * 50)
        print("\n功能说明:")
        print("  - 人体检测: 2米范围内自动检测")
        print("  - 人脸识别: 自动识别已注册人员")
        print("  - 云台追踪: 自动跟随目标移动")
        print("  - 迎宾功能: 检测到人员时主动问候")
        print("  - 机械臂互动: 迎宾时自动挥动手臂")
    
    def run(self, test_mode: bool = False, max_frames: int = 500):
        """主运行循环
        
        Args:
            test_mode: 测试模式 (无 GUI，自动保存结果)
            max_frames: 最大运行帧数 (测试模式用)
        """
        # 打开摄像头
        if not self.camera.open():
            print("[错误] 无法打开摄像头，退出")
            return
        
        self.running = True
        
        # 设置信号处理
        signal.signal(signal.SIGINT, self._signal_handler)
        
        print("\n开始运行...")
        if test_mode:
            print(f"测试模式: 将运行 {max_frames} 帧并自动保存结果")
            print(f"检测结果将保存到 detections/ 目录")
            os.makedirs("detections", exist_ok=True)
        else:
            print("按键: q=退出, s=截图, r=注册人脸, c=标定距离")
        print("-" * 50)
        
        try:
            while self.running:
                # 读取帧
                frame = self.camera.read()
                if frame is None:
                    continue
                
                self.current_frame = frame.copy()
                self.frame_count += 1
                
                # 处理帧
                result_frame = self._process_frame(frame)
                
                # 显示 (如果有 GUI)
                has_gui = True
                try:
                    cv2.imshow("智能迎宾机器人", result_frame)
                    key = cv2.waitKey(1) & 0xFF
                except cv2.error:
                    # 无 GUI 环境
                    has_gui = False
                    key = 0
                    
                    # 测试模式：自动保存有检测结果的帧
                    if test_mode:
                        if hasattr(self, 'last_detections') and self.last_detections:
                            if self.frame_count % 10 == 0:  # 每10帧保存一次
                                filename = f"detections/detection_{self.frame_count:06d}.jpg"
                                cv2.imwrite(filename, result_frame)
                                print(f"\r[保存] 检测结果: {filename}", end="")
                    else:
                        # 非测试模式，定期保存截图
                        if self.frame_count % 100 == 0:
                            filename = f"frame_{self.frame_count:06d}.jpg"
                            cv2.imwrite(filename, result_frame)
                            print(f"\n[截图] 已保存: {filename}")
                
                # 测试模式：检查最大帧数
                if test_mode and self.frame_count >= max_frames:
                    print(f"\n[测试完成] 已达到最大帧数 {max_frames}")
                    break
                if key == ord('q'):
                    break
                elif key == ord('s'):
                    self._save_screenshot()
                elif key == ord('r'):
                    # 无交互式输入，跳过
                    print("[提示] 无 GUI 模式，跳过注册")
                elif key == ord('c'):
                    self._calibrate_distance()
                
        except Exception as e:
            print(f"[错误] 运行异常: {e}")
            import traceback
            traceback.print_exc()
        
        finally:
            self.shutdown()
    
    def _process_frame(self, frame: np.ndarray) -> np.ndarray:
        """
        处理单帧图像
        
        Args:
            frame: 输入图像
            
        Returns:
            处理后的图像
        """
        # 1. 人体检测
        persons = self.detector.detect(frame, track=True)
        
        # 保存检测结果供测试模式使用
        self.last_detections = persons
        
        # 2. 选择最近的人体
        closest_person = self.detector.get_closest_person(
            persons, max_distance=self.config.get("welcome_distance", 2.0)
        )
        
        # 3. 人脸检测 (只在有近距离人体时进行)
        face = None
        recognized_name = None
        
        if closest_person is not None:
            # 裁剪人体区域进行人脸检测
            x1, y1, x2, y2 = closest_person["bbox"]
            
            # 稍微扩大区域确保包含人脸
            margin = int((y2 - y1) * 0.2)
            face_roi = frame[max(0, y1-margin):min(frame.shape[0], y2), 
                           max(0, x1):min(frame.shape[1], x2)]
            
            if face_roi.size > 0:
                faces = self.face_recognizer.detect_faces(face_roi)
                
                if faces:
                    # 选择最大的人脸
                    face = max(faces, key=lambda f: 
                              (f["bbox"][2]-f["bbox"][0]) * (f["bbox"][3]-f["bbox"][1]))
                    
                    # 调整人脸坐标到原图
                    fx1, fy1, fx2, fy2 = face["bbox"]
                    face["bbox"] = (x1 + fx1, y1 - margin + fy1, 
                                   x1 + fx2, y1 - margin + fy2)
                    
                    # 识别人脸
                    recognized_name, score = self.face_recognizer.recognize(face)
        
        # 4. 迎宾逻辑处理
        action_result = self.greeter.process(closest_person, face, recognized_name)
        
        # 5. 可视化
        display_frame = frame.copy()
        
        # 绘制人体检测
        if persons:
            display_frame = self.visualizer.draw_detection(display_frame, persons)
        
        # 绘制人脸
        if face:
            display_frame = self.visualizer.draw_face(
                display_frame, [face], [recognized_name]
            )
        
        # 绘制信息面板
        fps = self.visualizer.update_fps()
        state_text = self.greeter.get_state().value
        stats = self.greeter.get_stats()
        
        # 添加云台角度到状态
        if self.config.get("enable_ptz", True):
            pan, tilt = self.current_ptz
            state_text += f" | 云台:{pan:.0f},{tilt:.0f}"
        
        display_frame = self.visualizer.draw_info_panel(
            display_frame, state_text, fps, stats
        )
        
        # 绘制迎宾信息
        if action_result.get("greet"):
            self.visualizer.show_greeting(
                action_result["greet_message"], 
                duration=3.0
            )
        
        active_greeting = self.visualizer.get_active_greeting()
        if active_greeting:
            display_frame = self.visualizer.draw_greeting(
                display_frame, active_greeting
            )
        
        # 绘制中心十字和距离区域
        display_frame = self.visualizer.draw_center_cross(display_frame)
        display_frame = self.visualizer.draw_distance_zone(
            display_frame, self.config.get("welcome_distance", 2.0)
        )
        
        return display_frame
    
    def _on_greet(self, name: str, message: str, is_new: bool):
        """迎宾回调"""
        print(f"\n[迎宾] {message}")
        print(f"       姓名: {name if name else '未知'}")
        print(f"       新访客: {'是' if is_new else '否'}")
        
        # 触发机械臂动作
        if self.arm_controller and self.arm_controller.is_ready():
            if is_new:
                print("[机械臂] 执行欢迎动作")
                self.arm_controller.welcome_guest()
            else:
                print("[机械臂] 执行挥手动作")
                self.arm_controller.wave_hand()
        
        # TODO: 触发语音播报
        # TODO: 触发屏幕显示欢迎界面
    
    def _on_person_lost(self):
        """人员丢失回调"""
        print("[信息] 目标丢失，返回待机")
    
    def _on_ptz_move(self, pan: float, tilt: float):
        """云台移动回调"""
        self.current_ptz = (pan, tilt)
        # 这里可以添加实际控制云台的代码
        # 例如: 发送串口命令或 ROS2 消息
        # print(f"\r[云台] Pan: {pan:.1f}°, Tilt: {tilt:.1f}°", end="")
    
    def _save_screenshot(self):
        """保存截图"""
        if self.current_frame is not None:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.jpg"
            cv2.imwrite(filename, self.current_frame)
            print(f"[截图] 已保存: {filename}")
    
    def _register_face_interactive(self):
        """交互式注册人脸"""
        if self.current_frame is None:
            print("[错误] 没有可用图像")
            return
        
        # 检测人脸
        faces = self.face_recognizer.detect_faces(self.current_frame)
        
        if not faces:
            print("[错误] 未检测到人脸")
            return
        
        if len(faces) > 1:
            print(f"[警告] 检测到 {len(faces)} 个人脸，将注册第一个")
        
        face = faces[0]
        
        # 输入姓名
        print("\n请输入姓名 (直接回车取消):")
        name = input("> ").strip()
        
        if name:
            success = self.face_recognizer.register_face(name, face)
            if success:
                print(f"[成功] 已注册: {name}")
        else:
            print("[取消] 注册已取消")
    
    def _calibrate_distance(self):
        """标定距离"""
        print("\n[标定] 请让人站在 2 米处，然后按回车")
        input("按回车继续...")
        
        if self.current_frame is not None:
            persons = self.detector.detect(self.current_frame, track=False)
            if persons:
                # 选择最大的人体
                person = max(persons, key=lambda p: p["height_px"])
                height_px = person["height_px"]
                
                self.detector.calibrate_distance(2.0, height_px)
                print(f"[成功] 已标定，人体高度: {height_px}px")
            else:
                print("[错误] 未检测到人体")
    
    def _signal_handler(self, signum, frame):
        """信号处理"""
        print("\n[信号] 收到中断信号，正在退出...")
        self.running = False
    
    def shutdown(self):
        """关闭系统"""
        print("\n正在关闭系统...")
        self.running = False
        self.camera.release()
        
        # 关闭机械臂
        if self.arm_controller:
            print("[机械臂] 断开连接...")
            self.arm_controller.disconnect()
        
        try:
            cv2.destroyAllWindows()
        except:
            pass
        print("[完成] 系统已关闭")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="智能迎宾机器人")
    parser.add_argument("--camera", "-c", type=str, default="/dev/video_header",
                       help="摄像头设备 (默认: /dev/video_header)")
    parser.add_argument("--width", "-W", type=int, default=640,
                       help="画面宽度 (默认: 640)")
    parser.add_argument("--height", "-H", type=int, default=480,
                       help="画面高度 (默认: 480)")
    parser.add_argument("--model", "-m", type=str, default="yolov8n.pt",
                       help="YOLO模型 (默认: yolov8n.pt)")
    parser.add_argument("--distance", "-d", type=float, default=2.0,
                       help="迎宾距离 (米, 默认: 2.0)")
    parser.add_argument("--list-cameras", action="store_true",
                       help="列出可用摄像头")
    parser.add_argument("--test-mode", "-t", action="store_true",
                       help="测试模式 (无GUI，自动保存结果)")
    parser.add_argument("--max-frames", type=int, default=500,
                       help="测试模式最大帧数 (默认: 500)")
    parser.add_argument("--no-ptz", action="store_true",
                       help="禁用云台追踪")
    parser.add_argument("--no-arm", action="store_true",
                       help="禁用机械臂")
    parser.add_argument("--arm-ip", type=str, default="192.168.3.100",
                       help="机械臂IP地址 (默认: 192.168.3.100)")
    parser.add_argument("--mock-arm", action="store_true",
                       help="使用机械臂模拟模式")
    
    args = parser.parse_args()
    
    # 列出摄像头
    if args.list_cameras:
        print("可用摄像头:")
        cameras = list_cameras()
        for cam in cameras:
            print(f"  索引 {cam['index']}: {cam['resolution']}")
        return
    
    # 配置
    config = {
        "camera_source": args.camera if args.camera != "/dev/video_header" else "/dev/video_header",
        "width": args.width,
        "height": args.height,
        "fps": 30,
        "yolo_model": args.model,
        "confidence_threshold": 0.5,
        "recognition_threshold": 0.6,
        "face_db_path": "data/face_database.pkl",
        "welcome_distance": args.distance,
        "min_greet_interval": 10,
        "follow_timeout": 5,
        "lost_timeout": 3,
        "enable_ptz": not args.no_ptz,  # 默认启用云台
        "enable_arm": not args.no_arm,  # 默认启用机械臂
        "arm_ip": args.arm_ip,
        "mock_arm": args.mock_arm
    }
    
    # 创建必要目录
    os.makedirs("data", exist_ok=True)
    os.makedirs("models/insightface", exist_ok=True)
    
    # 启动机器人
    robot = WelcomeRobot(config)
    robot.run(test_mode=args.test_mode, max_frames=args.max_frames)


if __name__ == "__main__":
    main()
