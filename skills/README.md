# Skills 目录

> 存放所有 Kimi Code CLI Skill 的目录

## 目录结构

```
skills/
├── README.md              # 本文件
└── arm_control/           # 机械臂控制 Skill
    ├── SKILL.md           # 详细文档
    ├── README.md          # 快速开始
    ├── examples/          # 示例代码
    └── templates/         # 配置文件
```

## 可用 Skills

### 执行层

| Skill | 描述 | 状态 | 路径 |
|-------|------|------|------|
| [arm_control](./arm_control/) | NX-7 机械臂控制 | ✅ 已验证 | `skills/arm_control/` |
| [chassis_control](./chassis_control/) | 底盘运动控制 | ✅ 已验证 | `skills/chassis_control/` |
| [head_control](./head_control/) | 显示器云台控制 | ✅ 已验证 | `skills/head_control/` |
| [action_runner](./action_runner/) | 复合动作执行器 | ✅ 已验证 | `skills/action_runner/` |
| ~~obstacle_avoidance~~ | ~~激光雷达避障控制~~ | ~~已禁用~~ | ~~`skills/obstacle_avoidance_bak/`~~ |

### 感知层

| Skill | 描述 | 状态 | 路径 |
|-------|------|------|------|
| [ultrasonic_perception](./ultrasonic_perception/) | 单路前向超声波避障 | ✅ 已验证 | `skills/ultrasonic_perception/` |

## 快速使用复合动作

```bash
# 进入目录
cd /home/aidlux/skills/action_runner

# 查看可用动作
python3 action_runner.py --list

# 执行复合动作
python3 action_runner.py "forward(1); wave(); nod(1)"

# 并行执行
python3 action_runner.py "forward(1); parallel(wave(), rotate(360)); nod(1)"
```

## 添加新 Skill

创建新 Skill 时，请遵循以下结构：

```
skills/
└── your_skill_name/
    ├── SKILL.md           # 详细文档（必须）
    ├── README.md          # 快速开始
    ├── examples/          # 示例代码
    └── ...
```

### SKILL.md 模板

```markdown
# Skill 名称

> **一句话描述**：简明扼要地描述这个 Skill 的功能

## 能力

- 能力1
- 能力2
- 能力3

## 使用场景

| 场景 | 描述 |
|------|------|
| 场景1 | 描述 |
| 场景2 | 描述 |

## 快速开始

### 1. 安装/配置

```bash
# 安装命令
```

### 2. 基础用法

```python
# 示例代码
```

### 3. 验证

```bash
# 验证命令
```

## 详细用法

### API/接口说明

```python
# 详细代码示例
```

## 故障排除

| 问题 | 解决方案 |
|------|----------|
| 问题1 | 解决方案1 |
| 问题2 | 解决方案2 |

## 最佳实践

- 建议1
- 建议2

## 版本信息

- **Skill 版本**: v1.0.0
- **更新日期**: YYYY-MM-DD
```

## 注意事项

- 所有 Skill 文档使用 Markdown 格式
- 代码示例必须是可运行的
- 故障排除要覆盖常见问题

### 智能层

| Skill | 描述 | 状态 | 路径 |
|-------|------|------|------|
| [nlp_skill_caller](./nlp_skill_caller/) | 自然语言 Skill 调用 | ✅ 已验证 | `skills/nlp_skill_caller/` |
