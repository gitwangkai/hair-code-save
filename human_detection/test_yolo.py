#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
YOLOv8 测试脚本 - 验证模型下载和推理
"""

import cv2
import numpy as np
from ultralytics import YOLO
import time

print("=" * 50)
print("YOLOv8 测试")
print("=" * 50)

# 加载模型 (会自动下载)
print("\n[1/3] 加载模型...")
model = YOLO("yolov8n.pt")
print("✅ 模型加载成功")

# 创建测试图像
print("\n[2/3] 创建测试图像...")
test_image = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
print("✅ 测试图像创建成功")

# 推理测试
print("\n[3/3] 推理测试...")
start_time = time.time()
results = model(test_image, verbose=False)
end_time = time.time()

print(f"✅ 推理完成")
print(f"   耗时: {(end_time - start_time)*1000:.1f}ms")

# 显示检测结果
for result in results:
    boxes = result.boxes
    print(f"   检测到 {len(boxes)} 个目标")
    
    for box in boxes:
        cls = int(box.cls[0])
        conf = float(box.conf[0])
        class_name = model.names[cls]
        print(f"   - {class_name}: {conf:.2f}")

print("\n" + "=" * 50)
print("YOLOv8 测试通过！")
print("=" * 50)
