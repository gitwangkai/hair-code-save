#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
云台追踪测试脚本
测试云台追踪功能和可视化效果
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
from greeter import PTZTracker

# 全局运行标志
running = True

def signal_handler(sig, frame):
    global running
    print("\n[信号] 收到中断，正在退出...")
    running = False

signal.signal(signal.SIGINT, signal_handler)

print("=" * 60)
print("云台追踪测试")
print("=" * 60)

# 初始化
print("\n[1/4] 初始化摄像头...")
camera = Camera(source="/dev/video_header", width=640, height=360, fps=30)
if not camera.open():
    print("[错误] 摄像头打开失败")
    sys.exit(1)

print("\n[2/4] 初始化人体检测器...")
detector = HumanDetector(model_path="yolov8n.pt", confidence_threshold=0.5, device="cpu")

print("\n[3/4] 初始化可视化...")
visualizer = Visualizer(width=640, height=360)

print("\n[4/4] 初始化云台追踪器...")
ptz_tracker = PTZTracker(
    pan_range=(-45, 45),
    tilt_range=(-30, 30),
    smooth_factor=0.3,
    dead_zone=0.1
)
ptz_tracker.set_frame_size(640, 360)

# 云台移动回调
ptz_angles = (0.0, 0.0)
def on_ptz_move(pan, tilt):
    global ptz_angles
    ptz_angles = (pan, tilt)

ptz_tracker.on_ptz_move = on_ptz_move

# 创建保存目录
os.makedirs("detections", exist_ok=True)

print("\n" + "=" * 60)
print("开始测试! 按 Ctrl+C 退出")
print("=" * 60)
print("\n测试说明:")
print("  - 当检测到人体时，云台会自动追踪")
print("  - 画面右上角显示当前云台角度")
print("  - 死区内不会移动 (避免抖动)")
print("  - 平滑系数 0.3 (兼顾响应速度和平滑度)")
print()

frame_count = 0
detection_count = 0
ptz_move_count = 0
start_time = time.time()

while running:
    # 读取帧
    frame = camera.read()
    if frame is None:
        continue
    
    frame_count += 1
    
    # 人体检测 (每2帧检测一次)
    if frame_count % 2 == 0:
        persons = detector.detect(frame, track=True)
        
        # 获取最近的人体
        closest = None
        if persons:
            closest = min(persons, key=lambda p: p.get("distance", 999))
        
        # 云台追踪
        ptz_result = None
        if closest:
            center = closest.get("center")
            ptz_result = ptz_tracker.track(center)
            if ptz_result:
                ptz_move_count += 1
        else:
            # 无目标时保持当前角度
            pass
        
        # 可视化
        display_frame = frame.copy()
        
        # 绘制人体检测
        if persons:
            detection_count += 1
            display_frame = visualizer.draw_detection(display_frame, persons)
        
        # 绘制信息面板 (包含云台角度)
        fps = visualizer.update_fps()
        pan, tilt = ptz_angles
        status_text = f"追踪中 | 云台:{pan:.0f}°, {tilt:.0f}°"
        
        # 使用简单的英文避免字体问题
        stats = {
            "total_visitors": detection_count,
            "known_visitors": 0,
            "unknown_visitors": 0,
            "total_greets": ptz_move_count
        }
        
        display_frame = visualizer.draw_info_panel(
            display_frame, status_text, fps, stats
        )
        
        # 绘制中心十字和死区
        h, w = display_frame.shape[:2]
        cx, cy = w // 2, h // 2
        dead_zone_x = int(w * ptz_tracker.dead_zone)
        dead_zone_y = int(h * ptz_tracker.dead_zone)
        
        # 绘制死区框
        cv2.rectangle(display_frame, 
                     (cx - dead_zone_x, cy - dead_zone_y),
                     (cx + dead_zone_x, cy + dead_zone_y),
                     (128, 128, 128), 1)
        
        # 绘制目标连线
        if closest:
            tx, ty = closest["center"]
            cv2.line(display_frame, (cx, cy), (tx, ty), (0, 255, 255), 2)
        
        # 保存图像
        if frame_count % 50 == 0:
            filename = f"detections/ptz_test_{frame_count:06d}.jpg"
            cv2.imwrite(filename, display_frame)
        
        # 打印状态
        if frame_count % 30 == 0:
            elapsed = time.time() - start_time
            fps_real = frame_count / elapsed
            status = f"帧:{frame_count} 检测:{len(persons)}人 云台:{pan:5.1f},{tilt:5.1f} FPS:{fps_real:.1f}"
            print(f"\r{status}", end="", flush=True)

# 清理
print("\n\n[清理] 释放资源...")
camera.release()

# 统计
elapsed = time.time() - start_time
print("\n" + "=" * 60)
print("测试结果:")
print(f"  总帧数: {frame_count}")
print(f"  检测次数: {detection_count}")
print(f"  云台移动次数: {ptz_move_count}")
print(f"  运行时间: {elapsed:.1f} 秒")
print(f"  平均 FPS: {frame_count/elapsed:.1f}")
print(f"  最终云台角度: Pan={ptz_angles[0]:.1f}°, Tilt={ptz_angles[1]:.1f}°")
print("=" * 60)

# 列出保存的测试结果
saved_files = sorted([f for f in os.listdir("detections") if f.startswith("ptz_test")])[-5:]
if saved_files:
    print("\n最近保存的测试图像:")
    for f in saved_files:
        print(f"  - detections/{f}")
