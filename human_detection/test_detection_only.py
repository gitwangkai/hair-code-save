#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
人体检测测试 - 跳过人脸识别，专注测试核心检测功能
"""

import sys
import os
sys.path.insert(0, 'src')
sys.path.insert(0, 'utils')

import cv2
import time
import signal
from camera import Camera
from detector import HumanDetector
from visualization import Visualizer

# 全局运行标志
running = True

def signal_handler(sig, frame):
    global running
    print("\n[信号] 收到中断，正在退出...")
    running = False

signal.signal(signal.SIGINT, signal_handler)

print("=" * 60)
print("人体检测测试 (无人脸识别)")
print("=" * 60)

# 初始化
print("\n[1/3] 初始化摄像头...")
camera = Camera(source="/dev/video_header", width=640, height=360, fps=30)
if not camera.open():
    print("[错误] 摄像头打开失败")
    sys.exit(1)

print("\n[2/3] 初始化人体检测器...")
detector = HumanDetector(model_path="yolov8n.pt", confidence_threshold=0.5, device="cpu")

print("\n[3/3] 初始化可视化...")
visualizer = Visualizer(width=640, height=360)

# 创建保存目录
os.makedirs("detections", exist_ok=True)

print("\n" + "=" * 60)
print("开始检测! 按 Ctrl+C 退出")
print("=" * 60)

frame_count = 0
detection_count = 0
start_time = time.time()
last_save_time = 0

while running:
    # 读取帧
    frame = camera.read()
    if frame is None:
        continue
    
    frame_count += 1
    
    # 人体检测 (每2帧检测一次)
    if frame_count % 2 == 0:
        persons = detector.detect(frame, track=True)
        
        # 可视化
        display_frame = frame.copy()
        display_frame = visualizer.draw_detection(display_frame, persons)
        display_frame = visualizer.draw_info_panel(
            display_frame, 
            "检测中" if running else "停止", 
            visualizer.update_fps(),
            {"total_visitors": detection_count}
        )
        
        # 保存检测结果
        if persons:
            detection_count += 1
            # 保存带检测框的图像
            if time.time() - last_save_time > 2:  # 每2秒保存一次
                filename = f"detections/person_{frame_count:06d}.jpg"
                cv2.imwrite(filename, display_frame)
                print(f"\n[检测到人体] 已保存: {filename}")
                print(f"  距离: {persons[0].get('distance', -1):.1f}m")
                print(f"  置信度: {persons[0]['confidence']:.2f}")
                last_save_time = time.time()
        
        # 定期打印状态
        if frame_count % 30 == 0:
            elapsed = time.time() - start_time
            fps = frame_count / elapsed
            status = f"帧:{frame_count} 检测:{detection_count} FPS:{fps:.1f}"
            print(f"\r{status}", end="", flush=True)

# 清理
print("\n\n[清理] 释放资源...")
camera.release()

# 统计
elapsed = time.time() - start_time
print("\n" + "=" * 60)
print("测试结果:")
print(f"  总帧数: {frame_count}")
print(f"  检测到人体次数: {detection_count}")
print(f"  运行时间: {elapsed:.1f} 秒")
print(f"  平均 FPS: {frame_count/elapsed:.1f}")

# 列出保存的检测结果
saved_files = [f for f in os.listdir("detections") if f.endswith('.jpg')]
if saved_files:
    print(f"\n  保存的检测结果: {len(saved_files)} 张")
    for f in saved_files[:5]:  # 只显示前5个
        print(f"    - {f}")
else:
    print("\n  未保存检测结果 (未检测到人体)")

print("=" * 60)
