#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
迎宾业务逻辑模块
整合人体检测、人脸识别和迎宾交互
"""

import cv2
import numpy as np
from typing import Optional, Dict, List, Callable, Tuple
from enum import Enum
import time
from datetime import datetime, timedelta
import threading
import queue


class PTZTracker:
    """
    简易云台追踪器
    基于目标位置计算云台角度
    """
    
    def __init__(self, 
                 pan_range: Tuple[float, float] = (-45, 45),
                 tilt_range: Tuple[float, float] = (-30, 30),
                 smooth_factor: float = 0.3,
                 dead_zone: float = 0.1):
        """
        初始化追踪器
        
        Args:
            pan_range: 水平角度范围
            tilt_range: 垂直角度范围
            smooth_factor: 平滑系数
            dead_zone: 死区比例 (画面中心多大范围内不移动)
        """
        self.pan_range = pan_range
        self.tilt_range = tilt_range
        self.smooth_factor = smooth_factor
        self.dead_zone = dead_zone
        
        self.current_pan = 0.0
        self.current_tilt = 0.0
        self.frame_width = 640
        self.frame_height = 480
        
        # 回调函数
        self.on_ptz_move: Optional[Callable[[float, float], None]] = None
    
    def set_frame_size(self, width: int, height: int):
        """设置画面尺寸"""
        self.frame_width = width
        self.frame_height = height
    
    def track(self, target_center: Optional[Tuple[int, int]]) -> Optional[Tuple[float, float]]:
        """
        追踪目标
        
        Args:
            target_center: 目标中心点 (x, y)，None 表示无目标
            
        Returns:
            云台角度 (pan, tilt)，如果无需移动返回 None
        """
        if target_center is None:
            return None
        
        cx, cy = target_center
        fx = self.frame_width / 2
        fy = self.frame_height / 2
        
        # 计算偏移比例 (-0.5 到 0.5)
        offset_x = (cx - fx) / self.frame_width
        offset_y = (cy - fy) / self.frame_height
        
        # 死区检查
        if abs(offset_x) < self.dead_zone and abs(offset_y) < self.dead_zone:
            return None
        
        # 计算目标角度
        target_pan = -offset_x * (self.pan_range[1] - self.pan_range[0]) / 2
        target_tilt = offset_y * (self.tilt_range[1] - self.tilt_range[0]) / 2
        
        # 限制范围
        target_pan = max(self.pan_range[0], min(self.pan_range[1], target_pan))
        target_tilt = max(self.tilt_range[0], min(self.tilt_range[1], target_tilt))
        
        # 平滑移动
        pan_move = (target_pan - self.current_pan) * self.smooth_factor
        tilt_move = (target_tilt - self.current_tilt) * self.smooth_factor
        
        # 更新当前角度
        self.current_pan += pan_move
        self.current_tilt += tilt_move
        
        # 调用回调
        if self.on_ptz_move:
            self.on_ptz_move(self.current_pan, self.current_tilt)
        
        return (self.current_pan, self.current_tilt)
    
    def reset(self):
        """重置角度"""
        self.current_pan = 0.0
        self.current_tilt = 0.0
        if self.on_ptz_move:
            self.on_ptz_move(0.0, 0.0)


class GreeterState(Enum):
    """迎宾状态机"""
    IDLE = "idle"           # 待机状态
    DETECTED = "detected"   # 检测到人体
    RECOGNIZING = "recognizing"  # 识别中
    GREETING = "greeting"   # 迎宾中
    FOLLOWING = "following" # 追踪中


class GreeterLogic:
    """
    迎宾逻辑核心
    
    功能:
    - 状态管理
    - 访客识别 (新/老访客)
    - 迎宾触发控制
    - 云台控制接口
    - 语音/屏幕交互接口
    """
    
    def __init__(self,
                 welcome_distance: float = 2.0,      # 迎宾触发距离 (米)
                 min_greet_interval: int = 10,        # 最短迎宾间隔 (秒)
                 follow_timeout: int = 5,             # 追踪超时 (秒)
                 lost_timeout: int = 3,               # 丢失超时 (秒)
                 enable_ptz: bool = True,             # 启用云台追踪
                 frame_width: int = 640,              # 画面宽度
                 frame_height: int = 480):            # 画面高度
        """
        初始化迎宾逻辑
        
        Args:
            welcome_distance: 迎宾触发距离阈值
            min_greet_interval: 对同一人最短迎宾间隔
            follow_timeout: 追踪状态超时时间
            lost_timeout: 目标丢失判定时间
            enable_ptz: 是否启用云台追踪
            frame_width: 画面宽度
            frame_height: 画面高度
        """
        self.welcome_distance = welcome_distance
        self.min_greet_interval = min_greet_interval
        self.follow_timeout = follow_timeout
        self.lost_timeout = lost_timeout
        
        # 状态机
        self.state = GreeterState.IDLE
        self.state_start_time = time.time()
        
        # 当前目标
        self.current_target = None
        self.target_lost_time = None
        
        # 迎宾历史
        self.greet_history = {}  # {name: last_greet_time}
        
        # 回调函数
        self.on_greet: Optional[Callable] = None          # 迎宾回调
        self.on_person_lost: Optional[Callable] = None    # 人员丢失回调
        self.on_state_change: Optional[Callable] = None   # 状态变化回调
        self.on_ptz_move: Optional[Callable[[float, float], None]] = None  # 云台移动回调
        
        # 云台追踪器
        self.enable_ptz = enable_ptz
        if enable_ptz:
            self.ptz_tracker = PTZTracker()
            self.ptz_tracker.set_frame_size(frame_width, frame_height)
            self.ptz_tracker.on_ptz_move = self._on_ptz_move
            print("[初始化] 云台追踪已启用")
        else:
            self.ptz_tracker = None
        
        # 统计信息
        self.stats = {
            "total_visitors": 0,
            "known_visitors": 0,
            "unknown_visitors": 0,
            "total_greets": 0
        }
        
        print("[初始化] 迎宾逻辑模块就绪")
        print(f"       迎宾距离: {welcome_distance}米")
        print(f"       迎宾间隔: {min_greet_interval}秒")
    
    def _on_ptz_move(self, pan: float, tilt: float):
        """云台移动回调"""
        if self.on_ptz_move:
            self.on_ptz_move(pan, tilt)
    
    def process(self, 
                person: Optional[Dict],
                face: Optional[Dict],
                recognized_name: Optional[str]) -> Dict:
        """
        处理一帧检测结果
        
        Args:
            person: 人体检测结果
            face: 人脸检测结果
            recognized_name: 识别到的人员姓名 (None 为未知)
            
        Returns:
            处理结果，包含动作指令
        """
        result = {
            "action": "none",
            "target": None,
            "greet": False,
            "greet_message": "",
            "pan_tilt": None  # (pan, tilt) 云台角度调整
        }
        
        current_time = time.time()
        
        # 状态机处理
        if self.state == GreeterState.IDLE:
            result = self._handle_idle(person, face, recognized_name, current_time)
        
        elif self.state == GreeterState.DETECTED:
            result = self._handle_detected(person, face, recognized_name, current_time)
        
        elif self.state == GreeterState.RECOGNIZING:
            result = self._handle_recognizing(person, face, recognized_name, current_time)
        
        elif self.state == GreeterState.GREETING:
            result = self._handle_greeting(person, face, recognized_name, current_time)
        
        elif self.state == GreeterState.FOLLOWING:
            result = self._handle_following(person, face, recognized_name, current_time)
        
        return result
    
    def _handle_idle(self, person, face, recognized_name, current_time):
        """待机状态处理"""
        result = {"action": "none", "target": None, "greet": False, 
                  "greet_message": "", "pan_tilt": None}
        
        if person is not None and person["distance"] <= self.welcome_distance:
            # 检测到有效范围内的人体
            self._transition_to(GreeterState.DETECTED)
            self.current_target = person
            result["target"] = person
            result["action"] = "detect"
        
        return result
    
    def _handle_detected(self, person, face, recognized_name, current_time):
        """检测到人体状态处理"""
        result = {"action": "detect", "target": self.current_target, 
                  "greet": False, "greet_message": "", "pan_tilt": None}
        
        if person is None:
            # 人体丢失
            if self.target_lost_time is None:
                self.target_lost_time = current_time
            elif current_time - self.target_lost_time > self.lost_timeout:
                self._transition_to(GreeterState.IDLE)
                self.current_target = None
                self.target_lost_time = None
                result["action"] = "lost"
        else:
            self.target_lost_time = None
            self.current_target = person
            result["target"] = person
            
            # 如果有人脸，进入识别状态
            if face is not None:
                self._transition_to(GreeterState.RECOGNIZING)
            else:
                # 无人脸，直接迎宾 (未知访客)
                self._transition_to(GreeterState.GREETING)
        
        return result
    
    def _handle_recognizing(self, person, face, recognized_name, current_time):
        """识别中状态处理"""
        result = {"action": "recognizing", "target": self.current_target,
                  "greet": False, "greet_message": "", "pan_tilt": None}
        
        if person is None:
            self._handle_lost(current_time)
            return result
        
        self.current_target = person
        result["target"] = person
        
        # 识别完成，进入迎宾状态
        self._transition_to(GreeterState.GREETING)
        
        return result
    
    def _handle_greeting(self, person, face, recognized_name, current_time):
        """迎宾状态处理"""
        # 生成迎宾语
        is_new, greet_msg = self._generate_greeting(recognized_name)
        
        result = {
            "action": "greet",
            "target": self.current_target,
            "greet": True,
            "greet_message": greet_msg,
            "recognized_name": recognized_name,
            "is_new_visitor": is_new,
            "pan_tilt": None
        }
        
        # 执行回调
        if self.on_greet:
            self.on_greet(recognized_name, greet_msg, is_new)
        
        # 更新统计
        self.stats["total_greets"] += 1
        
        # 进入追踪状态
        self._transition_to(GreeterState.FOLLOWING)
        
        return result
    
    def _handle_following(self, person, face, recognized_name, current_time):
        """追踪状态处理 (含云台追踪)"""
        result = {"action": "follow", "target": self.current_target,
                  "greet": False, "greet_message": "", "pan_tilt": None}
        
        state_duration = current_time - self.state_start_time
        
        if person is None:
            if self.target_lost_time is None:
                self.target_lost_time = current_time
            elif current_time - self.target_lost_time > self.lost_timeout:
                # 丢失目标，返回待机
                self._transition_to(GreeterState.IDLE)
                self.current_target = None
                self.target_lost_time = None
                result["action"] = "lost"
                
                if self.on_person_lost:
                    self.on_person_lost()
                
                # 重置云台
                if self.ptz_tracker:
                    self.ptz_tracker.reset()
        else:
            self.target_lost_time = None
            self.current_target = person
            result["target"] = person
            
            # 云台追踪
            if self.ptz_tracker and self.enable_ptz:
                person_center = person.get("center")
                pan_tilt = self.ptz_tracker.track(person_center)
                if pan_tilt:
                    result["pan_tilt"] = pan_tilt
            
            # 追踪超时检查
            if state_duration > self.follow_timeout:
                self._transition_to(GreeterState.IDLE)
                self.current_target = None
                result["action"] = "timeout"
                
                # 重置云台
                if self.ptz_tracker:
                    self.ptz_tracker.reset()
        
        return result
    
    def _handle_lost(self, current_time):
        """处理目标丢失"""
        if self.target_lost_time is None:
            self.target_lost_time = current_time
        elif current_time - self.target_lost_time > self.lost_timeout:
            self._transition_to(GreeterState.IDLE)
            self.current_target = None
            self.target_lost_time = None
    
    def _generate_greeting(self, name: Optional[str]) -> tuple:
        """
        生成迎宾语
        
        Returns:
            (是否是新访客, 迎宾语)
        """
        current_time = datetime.now()
        hour = current_time.hour
        
        # 判断时段
        if 5 <= hour < 12:
            time_greeting = "早上好"
        elif 12 <= hour < 14:
            time_greeting = "中午好"
        elif 14 <= hour < 18:
            time_greeting = "下午好"
        else:
            time_greeting = "晚上好"
        
        # 检查是否是新访客
        is_new = True
        last_greet = None
        
        visitor_key = name if name else "unknown"
        
        if visitor_key in self.greet_history:
            last_greet = self.greet_history[visitor_key]
            time_diff = (current_time - last_greet).total_seconds()
            is_new = time_diff > self.min_greet_interval * 60  # 转换为分钟
        
        # 生成问候语
        if name:
            if is_new:
                greet_msg = f"{name}，{time_greeting}！欢迎光临！"
            else:
                greet_msg = f"{name}，欢迎回来！"
        else:
            greet_msg = f"{time_greeting}！欢迎光临！"
        
        # 更新历史
        self.greet_history[visitor_key] = current_time
        
        # 更新统计
        if is_new:
            self.stats["total_visitors"] += 1
            if name:
                self.stats["known_visitors"] += 1
            else:
                self.stats["unknown_visitors"] += 1
        
        return is_new, greet_msg
    
    def _calculate_pan_tilt(self, person: Dict) -> tuple:
        """
        计算云台调整角度
        
        Returns:
            (pan_angle, tilt_angle) 角度值
        """
        # 获取人体中心相对于画面中心的位置
        cx, cy = person["center"]
        
        # 假设画面中心为 (0.5, 0.5)
        # 计算偏移比例 (-0.5 到 0.5)
        # 这里需要知道画面尺寸，暂时使用假设值
        
        # 简化计算: 假设画面 640x480
        frame_cx, frame_cy = 320, 240
        
        offset_x = (cx - frame_cx) / 320  # -1 到 1
        offset_y = (cy - frame_cy) / 240  # -1 到 1
        
        # 转换为角度 (假设云台最大 ±45 度)
        max_pan = 45
        max_tilt = 30
        
        pan_angle = -offset_x * max_pan   # 反向
        tilt_angle = offset_y * max_tilt
        
        return (pan_angle, tilt_angle)
    
    def _transition_to(self, new_state: GreeterState):
        """状态转换"""
        old_state = self.state
        self.state = new_state
        self.state_start_time = time.time()
        
        if old_state != new_state and self.on_state_change:
            self.on_state_change(old_state, new_state)
        
        print(f"[状态] {old_state.value} -> {new_state.value}")
    
    def get_state(self) -> GreeterState:
        """获取当前状态"""
        return self.state
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        return self.stats.copy()
    
    def reset(self):
        """重置状态"""
        self.state = GreeterState.IDLE
        self.current_target = None
        self.target_lost_time = None
        print("[信息] 迎宾逻辑已重置")


class GreetingQueue:
    """
    迎宾队列
    用于管理多个访客迎宾请求
    """
    
    def __init__(self, max_size: int = 10):
        self.queue = queue.Queue(maxsize=max_size)
        self.processing = False
        self.current_task = None
    
    def add(self, greeting_data: Dict):
        """添加迎宾任务"""
        try:
            self.queue.put_nowait(greeting_data)
        except queue.Full:
            print("[警告] 迎宾队列已满")
    
    def get_next(self) -> Optional[Dict]:
        """获取下一个迎宾任务"""
        try:
            return self.queue.get_nowait()
        except queue.Empty:
            return None
    
    def is_empty(self) -> bool:
        """检查队列是否为空"""
        return self.queue.empty()
    
    def size(self) -> int:
        """获取队列大小"""
        return self.queue.qsize()


if __name__ == "__main__":
    print("迎宾逻辑模块测试")
    greeter = GreeterLogic()
    print("初始化完成！")
