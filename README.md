# 🤖 海尔机器人机械臂控制代码库

基于 NX-7 仿生机械臂（PallasSDK）的人体检测与挥手迎宾系统

## 📁 项目结构

```
├── demo_arm/           # 挥手测试代码
├── human_detection/    # 人体检测与挥手项目
├── aidcode/           # 其他代码
├── openclaw/          # OpenClaw配置
└── root_scripts/      # 根目录关键脚本
```

## 🚀 快速开始

```bash
# 运行挥手程序
cd demo_arm
python wave_hand.py

# 运行人体检测
cd human_detection
python main.py
```

## 📝 说明

- 模型文件 (.onnx, .pt) 未包含，需要单独下载
- 地图文件 (.pgm, .pbstream) 未包含

## 🔗 GitHub

https://github.com/gitwangkai/hair-code-save
