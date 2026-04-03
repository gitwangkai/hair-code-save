#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
人脸识别模块 - 基于 InsightFace
支持人脸检测、特征提取和身份识别
"""

import cv2
import numpy as np
import os
import pickle
from typing import List, Dict, Tuple, Optional
from datetime import datetime


class FaceRecognizer:
    """
    人脸识别器
    
    功能:
    - 人脸检测
    - 人脸特征提取
    - 人脸库管理 (注册/删除/识别)
    - 身份匹配
    """
    
    def __init__(self, 
                 face_db_path: str = "data/face_database.pkl",
                 recognition_threshold: float = 0.6,
                 detector_size: Tuple[int, int] = (640, 640)):
        """
        初始化人脸识别器
        
        Args:
            face_db_path: 人脸数据库保存路径
            recognition_threshold: 识别阈值 (越小越严格)
            detector_size: 检测器输入尺寸
        """
        self.face_db_path = face_db_path
        self.recognition_threshold = recognition_threshold
        self.detector_size = detector_size
        
        # 加载 InsightFace
        self._load_model()
        
        # 加载人脸数据库
        self.face_db = {}
        self._load_database()
        
        # 访客统计
        self.visitor_history = {}
        
        print(f"[初始化] 人脸识别器就绪，已注册 {len(self.face_db)} 人")
    
    def _load_model(self):
        """加载 InsightFace 模型"""
        try:
            import insightface
            from insightface.app import FaceAnalysis
            
            print("[加载] 正在加载 InsightFace 模型...")
            
            # 使用轻量级模型 (buffalo_s 或 buffalo_l)
            self.app = FaceAnalysis(name='buffalo_s', root='models/insightface')
            self.app.prepare(ctx_id=-1, det_size=self.detector_size)
            
            print("[成功] InsightFace 模型加载完成")
            
        except Exception as e:
            print(f"[错误] 模型加载失败: {e}")
            print("[提示] 使用备选方案: OpenCV DNN 人脸检测")
            self._init_fallback()
    
    def _init_fallback(self):
        """初始化备选方案 (OpenCV DNN)"""
        self.app = None
        
        # 加载 OpenCV DNN 人脸检测器
        model_dir = "models/opencv_face_detector"
        prototxt = os.path.join(model_dir, "deploy.prototxt")
        model = os.path.join(model_dir, "res10_300x300_ssd_iter_140000.caffemodel")
        
        if os.path.exists(prototxt) and os.path.exists(model):
            self.face_net = cv2.dnn.readNetFromCaffe(prototxt, model)
        else:
            self.face_net = None
            print("[警告] 未找到人脸检测模型")
    
    def detect_faces(self, frame: np.ndarray) -> List[Dict]:
        """
        检测图像中的所有人脸
        
        Args:
            frame: 输入图像 (BGR格式)
            
        Returns:
            人脸列表，每个包含:
            - bbox: (x1, y1, x2, y2)
            - kps: 关键点 (5个点)
            - embedding: 特征向量 (如果 InsightFace 可用)
            - confidence: 检测置信度
        """
        if self.app is None:
            return self._detect_faces_fallback(frame)
        
        # 转换 BGR -> RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # 检测人脸
        faces = self.app.get(rgb_frame)
        
        results = []
        for face in faces:
            # 获取边界框
            bbox = face.bbox.astype(int)
            x1, y1, x2, y2 = bbox[0], bbox[1], bbox[2], bbox[3]
            
            # 获取关键点
            kps = face.kps.astype(int) if hasattr(face, 'kps') else None
            
            # 获取特征向量
            embedding = face.embedding if hasattr(face, 'embedding') else None
            
            # 检测置信度
            det_score = float(face.det_score) if hasattr(face, 'det_score') else 0.9
            
            results.append({
                "bbox": (x1, y1, x2, y2),
                "kps": kps,
                "embedding": embedding,
                "confidence": det_score
            })
        
        return results
    
    def _detect_faces_fallback(self, frame: np.ndarray) -> List[Dict]:
        """备选人脸检测 (OpenCV DNN)"""
        if self.face_net is None:
            return []
        
        h, w = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0,
                                     (300, 300), (104.0, 177.0, 123.0))
        
        self.face_net.setInput(blob)
        detections = self.face_net.forward()
        
        results = []
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            
            if confidence > 0.5:
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                x1, y1, x2, y2 = box.astype(int)
                
                results.append({
                    "bbox": (x1, y1, x2, y2),
                    "kps": None,
                    "embedding": None,
                    "confidence": float(confidence)
                })
        
        return results
    
    def recognize(self, face_data: Dict) -> Tuple[Optional[str], float]:
        """
        识别单个人脸
        
        Args:
            face_data: 人脸数据 (包含 embedding)
            
        Returns:
            (姓名, 相似度) 如果无法识别则姓名为 None
        """
        if face_data["embedding"] is None:
            return None, 0.0
        
        if not self.face_db:
            return None, 0.0
        
        embedding = face_data["embedding"]
        
        # 计算与数据库中所有人脸的相似度
        best_match = None
        best_score = float('inf')
        
        for name, db_embedding in self.face_db.items():
            # 计算欧氏距离
            dist = np.linalg.norm(embedding - db_embedding)
            
            if dist < best_score:
                best_score = dist
                best_match = name
        
        # 判断是否匹配成功
        if best_score < self.recognition_threshold:
            return best_match, best_score
        else:
            return None, best_score
    
    def register_face(self, name: str, face_data: Dict) -> bool:
        """
        注册新人脸
        
        Args:
            name: 人员姓名
            face_data: 人脸数据
            
        Returns:
            是否注册成功
        """
        if face_data["embedding"] is None:
            print("[错误] 无法提取人脸特征")
            return False
        
        self.face_db[name] = face_data["embedding"]
        self._save_database()
        
        print(f"[成功] 已注册: {name}")
        return True
    
    def remove_face(self, name: str) -> bool:
        """删除人脸"""
        if name in self.face_db:
            del self.face_db[name]
            self._save_database()
            print(f"[成功] 已删除: {name}")
            return True
        return False
    
    def _load_database(self):
        """加载人脸数据库"""
        if os.path.exists(self.face_db_path):
            try:
                with open(self.face_db_path, 'rb') as f:
                    self.face_db = pickle.load(f)
                print(f"[加载] 人脸数据库: {len(self.face_db)} 人")
            except Exception as e:
                print(f"[错误] 加载数据库失败: {e}")
                self.face_db = {}
        else:
            print("[提示] 人脸数据库不存在，将创建新数据库")
            os.makedirs(os.path.dirname(self.face_db_path), exist_ok=True)
            self.face_db = {}
    
    def _save_database(self):
        """保存人脸数据库"""
        try:
            with open(self.face_db_path, 'wb') as f:
                pickle.dump(self.face_db, f)
        except Exception as e:
            print(f"[错误] 保存数据库失败: {e}")
    
    def record_visitor(self, name: Optional[str], face_bbox: Tuple):
        """
        记录访客信息
        
        Returns:
            是否是新访客
        """
        current_time = datetime.now()
        
        # 生成临时ID (未知人员)
        if name is None:
            name = f"visitor_{face_bbox[0]}_{face_bbox[1]}"
        
        if name not in self.visitor_history:
            self.visitor_history[name] = {
                "first_visit": current_time,
                "visit_count": 1,
                "last_visit": current_time
            }
            return True  # 新访客
        else:
            self.visitor_history[name]["visit_count"] += 1
            self.visitor_history[name]["last_visit"] = current_time
            return False  # 老访客
    
    def get_visitor_info(self, name: str) -> Optional[Dict]:
        """获取访客信息"""
        return self.visitor_history.get(name)
    
    def extract_face_image(self, frame: np.ndarray, 
                          bbox: Tuple, 
                          expand_ratio: float = 0.2) -> np.ndarray:
        """
        从图像中提取人脸区域
        
        Args:
            frame: 原图
            bbox: 人脸边界框 (x1, y1, x2, y2)
            expand_ratio: 扩展比例
            
        Returns:
            人脸区域图像
        """
        h, w = frame.shape[:2]
        x1, y1, x2, y2 = bbox
        
        # 扩展边界框
        width = x2 - x1
        height = y2 - y1
        
        x1 = max(0, int(x1 - width * expand_ratio))
        y1 = max(0, int(y1 - height * expand_ratio))
        x2 = min(w, int(x2 + width * expand_ratio))
        y2 = min(h, int(y2 + height * expand_ratio))
        
        return frame[y1:y2, x1:x2]
    
    def align_face(self, frame: np.ndarray, face_data: Dict, 
                   output_size: Tuple[int, int] = (112, 112)) -> np.ndarray:
        """
        对齐人脸 (用于注册高质量人脸)
        
        需要关键点信息
        """
        if face_data["kps"] is None:
            # 无关键点，直接裁剪
            return self.extract_face_image(frame, face_data["bbox"])
        
        # 使用关键点进行对齐 (简化的仿射变换)
        kps = face_data["kps"]
        
        # 标准位置 (112x112 图像中的典型人脸关键点位置)
        dst_pts = np.array([
            [38, 38],    # 左眼
            [74, 38],    # 右眼
            [56, 60],    # 鼻子
            [40, 82],    # 左嘴角
            [72, 82]     # 右嘴角
        ], dtype=np.float32)
        
        # 源关键点
        src_pts = kps.astype(np.float32)
        
        # 计算仿射变换
        M = cv2.estimateAffinePartial2D(src_pts, dst_pts)[0]
        
        # 应用变换
        aligned = cv2.warpAffine(frame, M, output_size)
        
        return aligned


if __name__ == "__main__":
    print("人脸识别器测试")
    recognizer = FaceRecognizer()
    print("初始化完成！")
