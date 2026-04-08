# 自然语言 Skill 调用器

通过自然语言指令控制机器人执行复合动作

## 功能

将自然语言指令转换为 Skill 调用序列：
- **obstacle_avoidance**: 避障监控
- **chassis_control**: 底盘移动  
- **arm_control**: 挥手动作
- **head_control**: 点头动作

## 使用方式

### 直接运行

```bash
cd /home/aidlux/skills/nlp_skill_caller
python3 nlp_skill_caller.py
```

### 作为模块调用

```python
from nlp_skill_caller import NLPSkillCaller

caller = NLPSkillCaller()
caller.execute_natural_command("前进1米挥手，右转360度，左转前进1米点头，返回")
```

## 支持的指令

| 自然语言 | 执行的 Skills |
|---------|--------------|
| 前进1米 | chassis_control/move(1.0) |
| 后退 | chassis_control/move(-1.0) |
| 右转360度 | chassis_control/rotate(-360) |
| 左转90度 | chassis_control/rotate(90) |
| 挥手 | arm_control/wave() |
| 点头 | head_control/nod() |
| 返回 | chassis_control/move(-1.0) + rotate + move |

## 复合动作示例

指令：
> "前进1米开始挥手，挥手时同步向右旋转360度然后左转前进一米点头，最后原路返回"

转换为 Skill 序列：
```
1. chassis/move(1.0) + arm/wave() [并行]
2. chassis/rotate(-360) [挥手继续]
3. chassis/rotate(90) + chassis/move(1.0) + head/nod()
4. chassis/move(-1.0) + chassis/rotate(-90) + chassis/move(-1.0)
```

## 避障保护

所有移动 Skills 都通过 obstacle_avoidance 监控：
- 前方 < 0.5m：禁止前进
- 左方 < 0.5m：禁止左转
- 右方 < 0.5m：禁止右转

## 依赖

- obstacle_avoidance Skill
- chassis_control Skill
- arm_control Skill
- ROS2 Humble
