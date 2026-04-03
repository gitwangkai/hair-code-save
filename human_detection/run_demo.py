#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速演示脚本 - 测试人体检测功能
不加载人脸识别模型，只测试摄像头和人体检测
"""

import cv2
import sys
import os
sys.path.insert(0, 'src')
sys.path.insert(0, 'utils')

from camera import Camera
from detector import HumanDetector
from visualization import Visualizer
import time

print("=" * 60)
print("智能迎宾机器人 - 快速演示")
print("=" * 60)

# 1. 初始化摄像头
print("\n[1/3] 初始化摄像头...")
camera = Camera(
    source="/dev/video_header",
    width=640,
    height=360,  # 实际分辨率
    fps=30
)

if not camera.open():
    print("[错误] 摄像头打开失败")
    sys.exit(1)

print("[成功] 摄像头已就绪")

# 2. 初始化检测器
print("\n[2/3] 初始化人体检测器...")
try:
    detector = HumanDetector(
        model_path="yolov8n.pt",
        confidence_threshold=0.5,
        device="cpu"
    )
    print("[成功] 检测器已就绪")
except Exception as e:
    print(f"[错误] 检测器初始化失败: {e}")
    camera.release()
    sys.exit(1)

# 3. 初始化可视化
visualizer = Visualizer(width=640, height=360)

print("\n[3/3] 开始检测循环...")
print("按 Ctrl+C 停止\n")

try:
    frame_count = 0
    start_time = time.time()
    
    while True:
        # 读取帧
        frame = camera.read()
        if frame is None:
            continue
        
        frame_count += 1
        
        # 人体检测 (每3帧检测一次，提高性能)
        if frame_count % 3 == 0:
            persons = detector.detect(frame, track=True)
            
            # 可视化
            display_frame = frame.copy()
            
            if persons:
                display_frame = visualizer.draw_detection(display_frame, persons)
                
                # 打印检测信息
                for p in persons:
                    dist = p.get('distance', -1)
                    print(f"\r检测到人体 | 距离: {dist:.1f}m | 置信度: {p['confidence']:.2f}", end="")
            else:
                print(f"\r未检测到人体...", end="")
            
            # 保存截图 (每100帧)
            if frame_count % 100 == 0:
                filename = f"detection_{frame_count}.jpg"
                cv2.imwrite(filename, display_frame)
                print(f"\n[截图] 已保存: {filename}")
        
        # FPS 统计
        if frame_count % 30 == 0:
            elapsed = time.time() - start_time
            fps = frame_count / elapsed
            print(f"\n[FPS] {fps:.1f}")

except KeyboardInterrupt:
    print("\n\n[信息] 用户中断")

finally:
    print("\n[清理] 释放资源...")
    camera.release()
    
    # 统计
    elapsed = time.time() - start_time
    print(f"\n运行统计:")
    print(f"  总帧数: {frame_count}")
    print(f"  运行时间: {elapsed:.1f} 秒")
    print(f"  平均 FPS: {frame_count/elapsed:.1f}")
    print("\n演示结束!")
