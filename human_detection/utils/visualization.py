#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
可视化工具模块
提供检测结果显示和UI绘制功能 (支持中文)
"""

import cv2
import numpy as np
from typing import List, Dict, Optional, Tuple
from PIL import Image, ImageDraw, ImageFont
import time
import os


class Visualizer:
    """
    可视化器 (支持中文显示)
    
    功能:
    - 绘制检测框和标签
    - 显示状态信息 (中文)
    - FPS 显示
    - 迎宾信息展示
    """
    
    # 颜色定义 (BGR)
    COLORS = {
        "person": (0, 255, 0),      # 绿色 - 人体
        "face": (255, 0, 0),        # 蓝色 - 人脸
        "text": (255, 255, 255),    # 白色 - 文字
        "bg": (0, 0, 0),            # 黑色 - 背景
        "highlight": (0, 165, 255), # 橙色 - 高亮
        "success": (0, 255, 0),     # 绿色 - 成功
        "warning": (0, 255, 255),   # 黄色 - 警告
        "info": (255, 255, 0)       # 青色 - 信息
    }
    
    def __init__(self, width: int = 640, height: int = 480):
        """
        初始化可视化器
        
        Args:
            width: 画面宽度
            height: 画面高度
        """
        self.width = width
        self.height = height
        
        # FPS 计算
        self.fps_history = []
        self.last_time = time.time()
        
        # 迎宾信息
        self.greet_message = ""
        self.greet_expire_time = 0
        
        # 状态信息
        self.state_text = "待机中"
        self.stats_text = ""
        
        # 加载中文字体
        self.font = self._load_font()
    
    def _load_font(self):
        """加载中文字体"""
        # 尝试加载系统中文字体
        font_paths = [
            "/usr/share/fonts/aidlux/NotoSansCJKsc-Regular.otf",  # AidLux
            "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
            "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
            "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
            "/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc",
        ]
        
        for font_path in font_paths:
            if os.path.exists(font_path):
                try:
                    # 使用 PIL 加载字体
                    font = ImageFont.truetype(font_path, 20)
                    print(f"[字体] 已加载: {font_path}")
                    return font
                except Exception as e:
                    print(f"[警告] 字体加载失败: {font_path}, {e}")
                    continue
        
        # 使用默认字体
        print("[警告] 使用中文字体失败，使用默认字体")
        return ImageFont.load_default()
    
    def _cv2_to_pil(self, cv2_img):
        """OpenCV 图像转 PIL 图像"""
        return Image.fromarray(cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB))
    
    def _pil_to_cv2(self, pil_img):
        """PIL 图像转 OpenCV 图像"""
        return cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
    
    def _draw_text(self, frame: np.ndarray, text: str, position: Tuple[int, int],
                   font_size: int = 20, color: Tuple = (255, 255, 255),
                   bg_color: Optional[Tuple] = None) -> np.ndarray:
        """
        使用 PIL 绘制中文文字
        
        Args:
            frame: OpenCV 图像
            text: 要绘制的文字
            position: (x, y) 位置
            font_size: 字体大小
            color: 文字颜色 (BGR)
            bg_color: 背景颜色 (BGR)，None 表示无背景
            
        Returns:
            绘制后的图像
        """
        pil_img = self._cv2_to_pil(frame)
        draw = ImageDraw.Draw(pil_img)
        
        # 加载指定大小的字体
        font = self.font
        if font_size != 20:
            try:
                font_paths = [
                    "/usr/share/fonts/aidlux/NotoSansCJKsc-Regular.otf",
                    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
                ]
                for fp in font_paths:
                    if os.path.exists(fp):
                        font = ImageFont.truetype(fp, font_size)
                        break
            except:
                font = self.font
        
        # 获取文字大小
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x, y = position
        
        # 绘制背景
        if bg_color:
            # BGR to RGB
            bg_rgb = (bg_color[2], bg_color[1], bg_color[0])
            draw.rectangle([x, y, x + text_width, y + text_height], fill=bg_rgb)
        
        # 绘制文字 (颜色 BGR to RGB)
        text_rgb = (color[2], color[1], color[0])
        draw.text((x, y), text, font=font, fill=text_rgb)
        
        return self._pil_to_cv2(pil_img)
    
    def draw_detection(self, 
                      frame: np.ndarray,
                      detections: List[Dict],
                      draw_track_id: bool = True) -> np.ndarray:
        """
        绘制人体检测结果
        
        Args:
            frame: 输入图像
            detections: 检测结果列表
            draw_track_id: 是否绘制追踪ID
            
        Returns:
            绘制后的图像
        """
        for det in detections:
            x1, y1, x2, y2 = det["bbox"]
            confidence = det["confidence"]
            distance = det.get("distance", -1)
            track_id = det.get("track_id")
            
            # 绘制边界框
            color = self.COLORS["person"]
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            
            # 准备标签
            label_parts = []
            if draw_track_id and track_id is not None:
                label_parts.append(f"ID:{track_id}")
            label_parts.append(f"{confidence:.2f}")
            if distance > 0:
                label_parts.append(f"{distance:.1f}m")
            
            label = " | ".join(label_parts)
            
            # 绘制标签背景 (使用 OpenCV 绘制英文标签)
            label_size, _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
            label_y = y1 - 10 if y1 - 10 > 10 else y1 + 20
            cv2.rectangle(frame, 
                         (x1, label_y - label_size[1] - 5),
                         (x1 + label_size[0], label_y + 5),
                         color, -1)
            
            # 绘制标签文字
            cv2.putText(frame, label, (x1, label_y),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.COLORS["text"], 1)
            
            # 绘制中心点
            cx, cy = det["center"]
            cv2.circle(frame, (cx, cy), 3, self.COLORS["highlight"], -1)
        
        return frame
    
    def draw_face(self, 
                 frame: np.ndarray,
                 faces: List[Dict],
                 recognized_names: List[Optional[str]]) -> np.ndarray:
        """
        绘制人脸检测结果
        
        Args:
            frame: 输入图像
            faces: 人脸列表
            recognized_names: 识别到的姓名列表
            
        Returns:
            绘制后的图像
        """
        for i, (face, name) in enumerate(zip(faces, recognized_names)):
            x1, y1, x2, y2 = face["bbox"]
            confidence = face["confidence"]
            
            # 根据识别结果选择颜色
            if name:
                color = self.COLORS["success"]
                label = f"{name}"
            else:
                color = self.COLORS["face"]
                label = "未知"
            
            # 绘制边界框
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            
            # 绘制中文标签
            label_y = y1 - 10 if y1 - 10 > 10 else y2 + 20
            frame = self._draw_text(frame, label, (x1, label_y), 
                                   font_size=18, color=self.COLORS["text"],
                                   bg_color=color)
            
            # 绘制关键点
            if face.get("kps") is not None:
                for kp in face["kps"]:
                    cv2.circle(frame, tuple(kp), 2, self.COLORS["highlight"], -1)
        
        return frame
    
    def draw_info_panel(self, 
                       frame: np.ndarray,
                       state: str,
                       fps: float,
                       stats: Optional[Dict] = None) -> np.ndarray:
        """
        绘制信息面板 (支持中文)
        
        Args:
            frame: 输入图像
            state: 当前状态
            fps: 当前 FPS
            stats: 统计信息
            
        Returns:
            绘制后的图像
        """
        # 绘制半透明背景
        overlay = frame.copy()
        cv2.rectangle(overlay, (5, 5), (280, 130), self.COLORS["bg"], -1)
        cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)
        
        # 绘制状态 (中文)
        state_color = self.COLORS["info"]
        frame = self._draw_text(frame, f"状态: {state}", (10, 10), 
                               font_size=20, color=state_color)
        
        # 绘制 FPS
        fps_color = self.COLORS["success"] if fps > 15 else self.COLORS["warning"]
        frame = self._draw_text(frame, f"FPS: {fps:.1f}", (10, 35), 
                               font_size=18, color=fps_color)
        
        # 绘制统计信息
        if stats:
            stats_text = f"访客:{stats.get('total_visitors', 0)} " \
                        f"已知:{stats.get('known_visitors', 0)} " \
                        f"未知:{stats.get('unknown_visitors', 0)}"
            frame = self._draw_text(frame, stats_text, (10, 60), 
                                   font_size=16, color=self.COLORS["text"])
            
            greet_text = f"迎宾次数: {stats.get('total_greets', 0)}"
            frame = self._draw_text(frame, greet_text, (10, 85), 
                                   font_size=16, color=self.COLORS["text"])
        
        return frame
    
    def draw_greeting(self, frame: np.ndarray, message: str) -> np.ndarray:
        """
        绘制迎宾信息 (大字中文)
        
        Args:
            frame: 输入图像
            message: 迎宾语
            
        Returns:
            绘制后的图像
        """
        if not message:
            return frame
        
        # 计算文字位置 (居中)
        h, w = frame.shape[:2]
        
        # 绘制背景
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, h - 80), (w, h), self.COLORS["highlight"], -1)
        cv2.addWeighted(overlay, 0.8, frame, 0.2, 0, frame)
        
        # 绘制中文文字
        frame = self._draw_text(frame, message, (20, h - 60), 
                               font_size=24, color=self.COLORS["text"])
        
        return frame
    
    def draw_center_cross(self, frame: np.ndarray) -> np.ndarray:
        """绘制画面中心十字线"""
        h, w = frame.shape[:2]
        cx, cy = w // 2, h // 2
        
        # 十字线
        cv2.line(frame, (cx - 20, cy), (cx + 20, cy), self.COLORS["info"], 1)
        cv2.line(frame, (cx, cy - 20), (cx, cy + 20), self.COLORS["info"], 1)
        
        # 中心点
        cv2.circle(frame, (cx, cy), 3, self.COLORS["highlight"], -1)
        
        return frame
    
    def draw_distance_zone(self, frame: np.ndarray, 
                          max_distance: float = 2.0) -> np.ndarray:
        """
        绘制有效距离区域
        
        在画面上显示迎宾有效范围的视觉提示
        """
        h, w = frame.shape[:2]
        
        # 绘制距离标尺 (中文)
        frame = self._draw_text(frame, f"迎宾范围: {max_distance}m", 
                               (w - 180, h - 20), 
                               font_size=16, color=self.COLORS["info"])
        
        return frame
    
    def update_fps(self) -> float:
        """更新并返回当前 FPS"""
        current_time = time.time()
        fps = 1.0 / (current_time - self.last_time)
        self.last_time = current_time
        
        self.fps_history.append(fps)
        if len(self.fps_history) > 30:
            self.fps_history.pop(0)
        
        return np.mean(self.fps_history)
    
    def show_greeting(self, message: str, duration: float = 3.0):
        """设置迎宾信息显示"""
        self.greet_message = message
        self.greet_expire_time = time.time() + duration
    
    def get_active_greeting(self) -> str:
        """获取当前有效的迎宾信息"""
        if time.time() < self.greet_expire_time:
            return self.greet_message
        return ""


def create_welcome_screen(name: Optional[str] = None, 
                         width: int = 640, 
                         height: int = 480) -> np.ndarray:
    """
    创建欢迎界面
    
    Args:
        name: 访客姓名 (None 表示未知访客)
        width: 画面宽度
        height: 画面高度
        
    Returns:
        欢迎界面图像
    """
    # 创建渐变背景
    image = np.zeros((height, width, 3), dtype=np.uint8)
    
    # 绘制欢迎文字 (使用默认字体，因为这是静态界面)
    if name:
        welcome_text = f"欢迎, {name}!"
    else:
        welcome_text = "欢迎光临!"
    
    text_size, _ = cv2.getTextSize(welcome_text, cv2.FONT_HERSHEY_SIMPLEX, 2, 4)
    text_x = (width - text_size[0]) // 2
    text_y = height // 2
    
    cv2.putText(image, welcome_text, (text_x, text_y),
               cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 4)
    
    return image


if __name__ == "__main__":
    print("可视化工具测试")
    
    # 创建测试图像
    test_frame = np.zeros((480, 640, 3), dtype=np.uint8)
    
    visualizer = Visualizer()
    
    # 测试中文显示
    test_frame = visualizer.draw_info_panel(test_frame, "检测中", 25.0, 
                                            {"total_visitors": 10})
    test_frame = visualizer.draw_greeting(test_frame, "欢迎光临！")
    
    cv2.imwrite("visualization_test.jpg", test_frame)
    print("测试图像已保存: visualization_test.jpg")
    print("可视化测试完成")
