#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
人体检测模块 - 基于 YOLOv8
完整版方案，支持高精度人体检测和追踪
"""

import cv2
import numpy as np
from typing import List, Dict, Tuple, Optional
from ultralytics import YOLO
import os


class HumanDetector:
    """
    人体检测器 - 使用 YOLOv8
    
    功能:
    - 实时人体检测
    - 人员追踪 (支持多目标)
    - 距离估计 (基于人体高度)
    """
    
    def __init__(self, 
                 model_path: str = "yolov8n.pt",
                 confidence_threshold: float = 0.5,
                 device: str = "cpu"):
        """
        初始化检测器
        
        Args:
            model_path: YOLOv8 模型路径或名称
                       - yolov8n.pt: Nano (最快, 适合ARM)
                       - yolov8s.pt: Small (平衡)
                       - yolov8m.pt: Medium (精度高)
            confidence_threshold: 置信度阈值
            device: 运行设备 (cpu/cuda)
        """
        self.confidence_threshold = confidence_threshold
        self.device = device
        
        print(f"[初始化] 正在加载 YOLOv8 模型: {model_path}")
        
        # 加载模型 (自动下载)
        self.model = YOLO(model_path)
        self.model.to(device)
        
        # 人员追踪器
        self.trackers = {}
        self.next_id = 0
        
        # 相机参数 (用于距离估计，需要根据实际标定)
        self.focal_length = 500  # 焦距 (像素)
        self.avg_person_height = 170  # 平均人体高度 (cm)
        
        print(f"[成功] 模型加载完成，设备: {device}")
    
    def detect(self, frame: np.ndarray, track: bool = True) -> List[Dict]:
        """
        检测图像中的人体
        
        Args:
            frame: 输入图像 (BGR格式)
            track: 是否启用追踪
            
        Returns:
            检测结果列表，每个元素包含:
            - bbox: (x1, y1, x2, y2) 边界框
            - confidence: 置信度
            - center: (cx, cy) 中心点
            - track_id: 追踪ID (如果启用追踪)
            - distance: 估计距离 (米)
        """
        if track:
            return self._detect_and_track(frame)
        else:
            return self._detect_only(frame)
    
    def _detect_only(self, frame: np.ndarray) -> List[Dict]:
        """仅检测，不追踪"""
        results = self.model(frame, verbose=False)
        return self._parse_results(results, frame.shape)
    
    def _detect_and_track(self, frame: np.ndarray) -> List[Dict]:
        """检测并追踪"""
        results = self.model(frame, verbose=False)
        detections = self._parse_results(results, frame.shape)
        
        # 更新追踪器
        self._update_trackers(detections)
        
        return detections
    
    def _parse_results(self, results, frame_shape) -> List[Dict]:
        """解析 YOLO 检测结果"""
        detections = []
        h, w = frame_shape[:2]
        
        for result in results:
            boxes = result.boxes
            
            for box in boxes:
                # 获取类别
                cls = int(box.cls[0])
                
                # 只保留 person 类别 (COCO 中 person = 0)
                if cls != 0:
                    continue
                
                confidence = float(box.conf[0])
                
                # 过滤低置信度
                if confidence < self.confidence_threshold:
                    continue
                
                # 获取边界框
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                
                # 确保坐标在图像范围内
                x1, y1 = max(0, x1), max(0, y1)
                x2, y2 = min(w, x2), min(h, y2)
                
                # 计算中心点
                cx = (x1 + x2) // 2
                cy = (y1 + y2) // 2
                
                # 估计距离 (基于人体高度)
                person_height_px = y2 - y1
                distance = self._estimate_distance(person_height_px)
                
                detections.append({
                    "bbox": (x1, y1, x2, y2),
                    "confidence": confidence,
                    "center": (cx, cy),
                    "track_id": None,
                    "distance": distance,
                    "height_px": person_height_px
                })
        
        return detections
    
    def _update_trackers(self, detections: List[Dict]):
        """更新人员追踪"""
        # 简单的 IOU 追踪
        assigned_ids = set()
        
        for det in detections:
            best_iou = 0
            best_id = None
            
            for track_id, tracker in self.trackers.items():
                if track_id in assigned_ids:
                    continue
                    
                iou = self._calculate_iou(det["bbox"], tracker["bbox"])
                if iou > best_iou and iou > 0.3:  # IOU 阈值
                    best_iou = iou
                    best_id = track_id
            
            if best_id is not None:
                det["track_id"] = best_id
                self.trackers[best_id] = det
                assigned_ids.add(best_id)
            else:
                # 新目标
                det["track_id"] = self.next_id
                self.trackers[self.next_id] = det
                assigned_ids.add(self.next_id)
                self.next_id += 1
        
        # 清理消失的追踪器
        self.trackers = {k: v for k, v in self.trackers.items() if k in assigned_ids}
    
    def _calculate_iou(self, box1: Tuple, box2: Tuple) -> float:
        """计算两个边界框的 IOU"""
        x1_1, y1_1, x2_1, y2_1 = box1
        x1_2, y1_2, x2_2, y2_2 = box2
        
        # 计算交集
        xi1 = max(x1_1, x1_2)
        yi1 = max(y1_1, y1_2)
        xi2 = min(x2_1, x2_2)
        yi2 = min(y2_1, y2_2)
        
        if xi2 <= xi1 or yi2 <= yi1:
            return 0.0
        
        inter_area = (xi2 - xi1) * (yi2 - yi1)
        
        # 计算并集
        box1_area = (x2_1 - x1_1) * (y2_1 - y1_1)
        box2_area = (x2_2 - x1_2) * (y2_2 - y1_2)
        union_area = box1_area + box2_area - inter_area
        
        return inter_area / union_area if union_area > 0 else 0
    
    def _estimate_distance(self, person_height_px: int) -> float:
        """
        估计人员距离
        
        使用针孔相机模型:
        distance = (focal_length * real_height) / pixel_height
        
        注意: 需要根据实际情况标定 focal_length
        """
        if person_height_px <= 0:
            return -1
        
        distance_cm = (self.focal_length * self.avg_person_height) / person_height_px
        return round(distance_cm / 100, 2)  # 转换为米
    
    def get_closest_person(self, 
                          detections: List[Dict],
                          max_distance: float = 2.0) -> Optional[Dict]:
        """
        获取最近的人员 (用于迎宾场景)
        
        Args:
            detections: 检测结果列表
            max_distance: 最大有效距离 (米)
            
        Returns:
            最近的人员，如果没有则在 None
        """
        valid_dets = [d for d in detections 
                     if d["distance"] > 0 and d["distance"] <= max_distance]
        
        if not valid_dets:
            return None
        
        # 按距离排序
        return min(valid_dets, key=lambda d: d["distance"])
    
    def calibrate_distance(self, known_distance_m: float, person_height_px: int):
        """
        标定距离估计参数
        
        使用方法:
        1. 让人站在已知距离 (如 2 米)
        2. 测量图像中人体高度 (像素)
        3. 调用此方法自动计算 focal_length
        """
        self.focal_length = (known_distance_m * 100 * person_height_px) / self.avg_person_height
        print(f"[标定] 焦距已更新: {self.focal_length:.2f} 像素")


if __name__ == "__main__":
    # 测试
    print("人体检测器测试")
    detector = HumanDetector(model_path="yolov8n.pt")
    print("初始化完成！")
