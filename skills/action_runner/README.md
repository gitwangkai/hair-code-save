# Action Runner - 复合动作执行器

> 一键执行复合动作，支持顺序和并行执行

## 快速开始

```bash
# 进入目录
cd /home/aidlux/skills/action_runner

# 查看可用动作
python3 action_runner.py --list

# 执行复合动作（顺序）
python3 action_runner.py "forward(1); wave(); nod(1)"

# 执行复合动作（并行）
python3 action_runner.py "forward(1); parallel(wave(), rotate(360)); nod(1)"

# 执行配置文件
python3 action_runner.py --file configs/greeting.yaml
```

## 语法说明

### 顺序执行
动作按顺序依次执行：
```bash
"forward(1); wave(); nod(1)"
```

### 并行执行
使用 `parallel()` 同时执行多个动作：
```bash
"forward(1); parallel(wave(), rotate(360)); nod(1)"
```

## 可用动作

| 模块 | 动作 | 参数 | 说明 |
|------|------|------|------|
| chassis | forward(distance) | 距离(米) | 前进 |
| chassis | backward(distance) | 距离(米) | 后退 |
| chassis | rotate(angle) | 角度(度) | 旋转 |
| chassis | stop() | - | 停止 |
| arm | wave() | - | 挥手 |
| arm | home() | - | 归位 |
| head | nod(times) | 次数 | 点头 |
| head | up() | - | 抬头 |
| head | down() | - | 低头 |
| head | center() | - | 归中 |
| util | wait(seconds) | 秒数 | 等待 |

## 示例

### 示例1：简单迎宾
```bash
python3 action_runner.py "forward(0.5); wave(); nod(2)"
```

### 示例2：巡逻路线
```bash
python3 action_runner.py "forward(2); rotate(90); forward(2); rotate(90); forward(2); rotate(90); forward(2); rotate(90)"
```

### 示例3：复杂互动
```bash
python3 action_runner.py "forward(1); parallel(wave(), rotate(360)); nod(3); home()"
```

## Python API

```python
from action_runner import ActionRunner

runner = ActionRunner()

# 执行命令字符串
runner.run_cmd("forward(1); wave(); nod(1)")

# 执行动作列表
runner.run([
    ("", "forward", (1,)),
    ("parallel", [
        ("", "wave", ()),
        ("", "rotate", (360,))
    ]),
    ("", "nod", (1,))
])
```

## 预定义复合动作

### 复合动作：前进挥手旋转返回

```bash
# 直接执行
bash /home/aidlux/run_skill_wave_return.sh

# 或使用 Python
python3 /home/aidlux/skills/action_runner/actions/complex_wave_return.py
```

动作序列：
1. 前进1米 + 挥手
2. 向右旋转360度（挥手同步）
3. 左转 + 前进1米 + 点头
4. 原路返回

依赖 Skills:
- `obstacle_avoidance`: 避障监控
- `chassis_control`: 底盘移动
- `arm_control`: 挥手、点头

## 配置文件

创建 YAML 配置文件：

```yaml
name: 自定义动作
description: 动作描述

actions:
  - ["", "forward", [1]]
  - ["parallel", [
      ["", "wave", []],
      ["", "rotate", [90]]
    ]]
  - ["", "nod", [3]]
```

执行：
```bash
python3 action_runner.py --file my_action.yaml
```
