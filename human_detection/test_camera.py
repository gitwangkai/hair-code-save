#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
摄像头测试脚本 - 专门针对 AidLux 平台
"""

import cv2
import sys
import time

def test_camera(device, width=320, height=240, timeout=10):
    """
    测试指定摄像头设备
    
    Args:
        device: 摄像头设备路径或索引
        width: 宽度
        height: 高度
        timeout: 测试超时时间(秒)
    """
    print("=" * 50)
    print(f"测试摄像头: {device}")
    print(f"目标分辨率: {width}x{height}")
    print("=" * 50)
    
    # 打开摄像头
    print("\n[1/4] 打开摄像头...")
    
    if isinstance(device, str) and device.startswith('/dev/'):
        cap = cv2.VideoCapture(device, cv2.CAP_V4L2)
    else:
        cap = cv2.VideoCapture(device)
    
    if not cap.isOpened():
        print(f"[失败] 无法打开摄像头: {device}")
        return False
    
    print(f"[成功] 摄像头已打开")
    
    # 设置参数
    print("\n[2/4] 设置摄像头参数...")
    
    # 尝试设置 MJPEG 格式
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    
    # 读取实际参数
    actual_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    actual_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    actual_fps = cap.get(cv2.CAP_PROP_FPS)
    
    print(f"[信息] 实际分辨率: {actual_width}x{actual_height}")
    print(f"[信息] 实际帧率: {actual_fps}")
    
    # 测试读取
    print("\n[3/4] 测试读取帧...")
    
    frame_count = 0
    start_time = time.time()
    last_frame = None
    
    while time.time() - start_time < timeout:
        ret, frame = cap.read()
        
        if not ret:
            print("[警告] 读取帧失败")
            continue
        
        frame_count += 1
        last_frame = frame
        
        # 显示 FPS
        elapsed = time.time() - start_time
        if elapsed > 0:
            fps = frame_count / elapsed
            if frame_count % 30 == 0:  # 每30帧打印一次
                print(f"[运行中] 已捕获 {frame_count} 帧, FPS: {fps:.1f}")
        
        # 显示图像 (如果环境支持 GUI)
        try:
            cv2.imshow(f"Camera Test - {device}", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("[信息] 用户中断")
                break
        except Exception as e:
            # 无 GUI 环境，只保存一帧
            if frame_count == 1:
                print(f"[信息] 无 GUI 环境，跳过显示 (这是正常的)")
    
    # 保存测试图像
    print("\n[4/4] 保存测试图像...")
    if last_frame is not None:
        filename = f"camera_test_{device.replace('/', '_')}.jpg"
        cv2.imwrite(filename, last_frame)
        print(f"[成功] 测试图像已保存: {filename}")
        print(f"[信息] 图像尺寸: {last_frame.shape}")
    
    # 统计
    elapsed = time.time() - start_time
    avg_fps = frame_count / elapsed if elapsed > 0 else 0
    
    print("\n" + "=" * 50)
    print("测试结果:")
    print(f"  总帧数: {frame_count}")
    print(f"  运行时间: {elapsed:.1f} 秒")
    print(f"  平均 FPS: {avg_fps:.1f}")
    print("=" * 50)
    
    # 释放
    cap.release()
    try:
        cv2.destroyAllWindows()
    except:
        pass  # 无 GUI 环境忽略
    
    return frame_count > 0


def find_working_camera():
    """自动查找可用的摄像头"""
    print("\n🔍 正在搜索可用摄像头...\n")
    
    # 测试的设备列表
    devices_to_test = [
        "/dev/video_header",  # AidLux 顶部摄像头
        "/dev/video6",        # header 的实际设备
        "/dev/video_rear",    # 后置摄像头
        "/dev/video4",        # rear 的实际设备
        "/dev/video0",        # 默认设备
        0,                    # 索引 0
        1,                    # 索引 1
    ]
    
    working_cameras = []
    
    for device in devices_to_test:
        print(f"\n{'='*50}")
        print(f"测试设备: {device}")
        print('='*50)
        
        try:
            if test_camera(device, width=320, height=240, timeout=3):
                working_cameras.append(device)
                print(f"✅ 设备 {device} 可用")
            else:
                print(f"❌ 设备 {device} 不可用")
        except Exception as e:
            print(f"❌ 设备 {device} 测试失败: {e}")
    
    print("\n" + "=" * 50)
    print("可用摄像头列表:")
    if working_cameras:
        for cam in working_cameras:
            print(f"  ✅ {cam}")
    else:
        print("  ❌ 未找到可用摄像头")
    print("=" * 50)
    
    return working_cameras


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="AidLux 摄像头测试工具")
    parser.add_argument("--device", "-d", type=str, default="/dev/video_header",
                       help="摄像头设备 (默认: /dev/video_header)")
    parser.add_argument("--width", "-W", type=int, default=320,
                       help="宽度 (默认: 320)")
    parser.add_argument("--height", "-H", type=int, default=240,
                       help="高度 (默认: 240)")
    parser.add_argument("--find", "-f", action="store_true",
                       help="自动查找所有可用摄像头")
    
    args = parser.parse_args()
    
    if args.find:
        find_working_camera()
    else:
        # 测试指定摄像头
        device = args.device
        # 尝试转换为数字
        try:
            device = int(device)
        except ValueError:
            pass
        
        success = test_camera(device, args.width, args.height)
        sys.exit(0 if success else 1)
