#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
摄像头驱动模块
支持多种摄像头接入方式
"""

import cv2
import numpy as np
from typing import Optional, Tuple
import threading
import queue
import time


class Camera:
    """
    摄像头类
    
    功能:
    - 摄像头捕获
    - 帧缓冲
    - 分辨率/帧率设置
    """
    
    def __init__(self, 
                 source: str = "/dev/video_header",
                 width: int = 640,
                 height: int = 480,
                 fps: int = 30,
                 buffer_size: int = 1):
        """
        初始化摄像头
        
        Args:
            source: 摄像头索引或视频文件路径
            width: 图像宽度
            height: 图像高度
            fps: 目标帧率
            buffer_size: 帧缓冲区大小
        """
        self.source = source
        self.width = width
        self.height = height
        self.fps = fps
        self.buffer_size = buffer_size
        
        self.cap = None
        self.is_running = False
        self.frame_queue = queue.Queue(maxsize=buffer_size)
        
        # 统计信息
        self.frame_count = 0
        self.last_fps_time = time.time()
        self.current_fps = 0
    
    def open(self) -> bool:
        """打开摄像头"""
        try:
            # AidLux 平台使用 V4L2 后端
            print(f"[信息] 正在打开摄像头: {self.source}")
            
            if isinstance(self.source, str) and self.source.startswith('/dev/'):
                # Linux 设备路径，使用 V4L2
                self.cap = cv2.VideoCapture(self.source, cv2.CAP_V4L2)
            else:
                # 数字索引，尝试 V4L2 否则默认
                self.cap = cv2.VideoCapture(self.source, cv2.CAP_V4L2)
            
            if not self.cap.isOpened():
                print(f"[警告] V4L2 打开失败，尝试默认后端...")
                self.cap = cv2.VideoCapture(self.source)
            
            if not self.cap.isOpened():
                print(f"[错误] 无法打开摄像头: {self.source}")
                return False
            
            # 设置 MJPEG 格式 (AidLux 摄像头支持)
            print("[信息] 设置摄像头参数...")
            self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
            
            # 设置分辨率
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
            self.cap.set(cv2.CAP_PROP_FPS, self.fps)
            
            # 设置缓冲区大小 (减少延迟)
            self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
            
            # 读取一帧测试
            ret, frame = self.cap.read()
            if not ret:
                print("[错误] 无法读取图像")
                return False
            
            # 获取实际参数
            actual_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            actual_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            actual_fps = self.cap.get(cv2.CAP_PROP_FPS)
            
            print(f"[成功] 摄像头已打开")
            print(f"       分辨率: {actual_width}x{actual_height}")
            print(f"       帧率: {actual_fps}")
            
            self.is_running = True
            return True
            
        except Exception as e:
            print(f"[错误] 打开摄像头失败: {e}")
            return False
    
    def read(self, flip: bool = True) -> Optional[np.ndarray]:
        """读取一帧图像
        
        Args:
            flip: 是否垂直翻转画面(摄像头倒装时使用)
        """
        if self.cap is None or not self.is_running:
            return None
        
        ret, frame = self.cap.read()
        
        if ret:
            # 垂直翻转画面
            if flip:
                frame = cv2.flip(frame, 0)
            
            self.frame_count += 1
            self._update_fps()
            return frame
        else:
            return None
    
    def _update_fps(self):
        """更新 FPS 统计"""
        current_time = time.time()
        elapsed = current_time - self.last_fps_time
        
        if elapsed >= 1.0:
            self.current_fps = self.frame_count / elapsed
            self.frame_count = 0
            self.last_fps_time = current_time
    
    def get_fps(self) -> float:
        """获取当前 FPS"""
        return self.current_fps
    
    def start_async(self):
        """启动异步捕获线程"""
        if not self.is_running:
            return
        
        self.capture_thread = threading.Thread(target=self._capture_loop)
        self.capture_thread.daemon = True
        self.capture_thread.start()
    
    def _capture_loop(self):
        """后台捕获循环"""
        while self.is_running:
            ret, frame = self.cap.read()
            
            if ret:
                # 更新队列 (保持最新帧)
                if self.frame_queue.full():
                    try:
                        self.frame_queue.get_nowait()
                    except queue.Empty:
                        pass
                
                try:
                    self.frame_queue.put_nowait(frame)
                except queue.Full:
                    pass
                
                self.frame_count += 1
                self._update_fps()
    
    def read_async(self) -> Optional[np.ndarray]:
        """从缓冲区读取帧"""
        try:
            return self.frame_queue.get_nowait()
        except queue.Empty:
            return None
    
    def release(self):
        """释放摄像头资源"""
        self.is_running = False
        
        if hasattr(self, 'capture_thread'):
            self.capture_thread.join(timeout=1.0)
        
        if self.cap is not None:
            self.cap.release()
            self.cap = None
        
        print("[信息] 摄像头已释放")
    
    def __enter__(self):
        self.open()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()


class CameraManager:
    """
    摄像头管理器
    支持多摄像头和自动切换
    """
    
    def __init__(self):
        self.cameras = {}
        self.active_camera = None
    
    def add_camera(self, name: str, camera: Camera):
        """添加摄像头"""
        self.cameras[name] = camera
    
    def switch_camera(self, name: str) -> bool:
        """切换活动摄像头"""
        if name in self.cameras:
            self.active_camera = self.cameras[name]
            return True
        return False
    
    def read(self) -> Optional[np.ndarray]:
        """读取当前活动摄像头的帧"""
        if self.active_camera:
            return self.active_camera.read()
        return None
    
    def release_all(self):
        """释放所有摄像头"""
        for camera in self.cameras.values():
            camera.release()


def list_cameras():
    """列出可用摄像头"""
    available = []
    
    for i in range(10):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            available.append({
                "index": i,
                "resolution": f"{width}x{height}"
            })
            cap.release()
    
    return available


if __name__ == "__main__":
    print("可用摄像头:")
    cameras = list_cameras()
    for cam in cameras:
        print(f"  索引 {cam['index']}: {cam['resolution']}")
