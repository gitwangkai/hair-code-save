# 🔧 问题修复说明

## 已修复的问题

### 1. 画面卡顿 - ✅ 已优化

**问题**: Web GUI 中画面卡顿明显

**解决方案**:
- 降低检测频率：从每2帧检测改为每3帧检测
- 降低图像质量：JPEG质量从70%降到60%
- 降低推送分辨率：超过640px时自动缩放
- 优化推送间隔：每2帧推送一次
- 使用检测平滑机制保持流畅性

**修改文件**:
- `web_gui.py`: 添加性能优化参数
- `web_gui.py`: `_processing_loop()` 检测间隔优化
- `web_gui.py`: `_push_frame()` 图像压缩优化

**配置参数**:
```python
self.detect_interval = 3    # 每3帧检测一次
self.push_interval = 2      # 每2帧推送一次
self.jpeg_quality = 60      # JPEG质量60%
```

---

### 2. 画面倒转 - ✅ 已修复

**问题**: 摄像头画面上下颠倒

**解决方案**:
- 在 `camera.read()` 方法中添加 `flip` 参数
- 默认开启垂直翻转

**修改文件**:
- `src/camera.py`: `read()` 方法添加 flip 参数

**使用方法**:
```python
# 默认开启翻转
frame = camera.read()  # 或 camera.read(flip=True)

# 如需关闭翻转
frame = camera.read(flip=False)
```

---

### 3. 人脸注册失败 - ✅ 已改进

**问题**: 实时注册人脸时检测失败

**解决方案**:
- 添加照片上传注册功能
- 支持两种注册方式：
  1. 使用当前监控画面
  2. 上传本地照片文件

**修改文件**:
- `web_gui.py`: 添加 `/api/register_face` 接口
- `templates/index.html`: 添加文件上传UI

**使用方法**:
1. 点击 Web GUI 中的 "👤 注册人脸" 按钮
2. 输入姓名
3. 选择注册方式：
   - "📷 使用当前画面" - 截取当前监控画面
   - "📁 上传照片" - 选择本地清晰的正面照片
4. 点击 "确认注册"

---

### 4. 人体检测闪烁 - ✅ 已优化

**问题**: 部分帧检测不到人体，导致检测框闪烁

**解决方案**:
- 添加检测平滑机制
- 保持上一帧检测结果 0.5 秒
- 在检测间隔期间显示保持的检测结果

**修改文件**:
- `web_gui.py`: 添加检测平滑参数

**实现逻辑**:
```python
# 检测间隔期间保持上一帧结果
if current_time - self.last_detection_time < self.detection_persist_time:
    persons = self.last_persons
```

---

## 性能对比

| 指标 | 修复前 | 修复后 | 提升 |
|------|--------|--------|------|
| 检测频率 | 每2帧 | 每3帧 | 减少33%计算量 |
| JPEG质量 | 70% | 60% | 带宽降低约15% |
| 推送频率 | 每3帧 | 每2帧 | 画面更流畅 |
| 检测平滑 | 无 | 0.5秒保持 | 减少闪烁 |

---

## 快速测试

### 测试画面翻转
```bash
cd /home/aidlux/human_detection
python3 -c "
from camera import Camera
import cv2
cam = Camera('/dev/video_header')
cam.open()
frame = cam.read(flip=True)  # 翻转
cv2.imwrite('flipped.jpg', frame)
cam.release()
print('已保存 flipped.jpg')
"
```

### 测试帧率
```bash
python3 test_fixes.py
```

### 启动 Web GUI
```bash
./start_gui.sh
```

---

## 文件变更列表

1. `src/camera.py` - 添加画面翻转功能
2. `web_gui.py` - 性能优化、照片上传注册、检测平滑
3. `templates/index.html` - 添加文件上传UI
4. `test_fixes.py` - 新增测试脚本
5. `FIXES_README.md` - 本文档

---

## 后续优化建议

1. **进一步降低分辨率**: 可尝试 480x270 以获得更高帧率
2. **启用硬件加速**: 如果 AidLux 支持 NPU/GPU 加速
3. **检测模型量化**: 使用 INT8 量化的 YOLO 模型
4. **缓存人脸特征**: 避免重复计算已识别人员

---

## 反馈

如有其他问题，请检查：
1. 浏览器控制台是否有报错
2. 服务器日志是否有异常
3. 网络带宽是否充足
