#!/usr/bin/env python3
"""
YAML 配置动作加载器

功能：从 YAML 配置文件加载并执行动作序列

使用：
    python3 action_loader.py <sequence_name>
    python3 action_loader.py wave_hand
    python3 action_loader.py pick_and_place

依赖：
    pip install pyyaml
"""
import os
import sys
import time
import yaml
import atexit
from pathlib import Path
from PallasSDK import Controller, LocationJ

# ==================== 配置 ====================
CONFIG_PATH = Path(__file__).parent.parent / "templates" / "robot_actions.yaml"


class ConfigLoader:
    """YAML 配置加载器"""
    
    def __init__(self, config_path=CONFIG_PATH):
        self.config = None
        self.load(config_path)
    
    def load(self, path):
        """加载 YAML 配置"""
        with open(path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)
        print(f"[配置] 已加载: {path}")
    
    def get_system(self):
        """获取系统配置"""
        return self.config.get('system', {})
    
    def get_joint_limits(self):
        """获取关节限位"""
        limits = self.config.get('joint_limits', {})
        result = {}
        for name, data in limits.items():
            result[name] = (data['min'], data['max'])
        return result
    
    def get_pose(self, name):
        """获取预设位姿"""
        poses = self.config.get('poses', {})
        if name not in poses:
            raise ValueError(f"未知位姿: {name}")
        return poses[name]['angles']
    
    def get_sequence(self, name):
        """获取动作序列"""
        sequences = self.config.get('sequences', {})
        if name not in sequences:
            available = list(sequences.keys())
            raise ValueError(f"未知序列: {name}. 可用: {available}")
        return sequences[name]


class ArmController:
    """机械臂控制器（支持配置驱动）"""
    
    def __init__(self, config_loader):
        self.cfg = config_loader
        self.sys = config_loader.get_system()
        self.ctrl = Controller()
        self.robot = None
        self.connected = False
        
        # 从配置读取参数
        self.ip = self.sys.get('robot_ip', '192.168.3.100')
        self.init_wait = self.sys.get('init_wait_seconds', 30)
        self.speed = self.sys.get('default_speed_percent', 10)
        self.move_wait = self.sys.get('move_wait_seconds', 1.0)
        self.emergency_pose = self.sys.get('emergency_pose', [0, 10, 0, 30, 0, 0])
        self.joint_limits = config_loader.get_joint_limits()
    
    def connect(self):
        """连接机械臂"""
        print(f"\n[连接] {self.ip}")
        self.ctrl.Connect(self.ip)
        print(f"  → 等待初始化 ({self.init_wait}s)...")
        time.sleep(self.init_wait)
        
        print("  → 伺服上电...")
        self.ctrl.SetPowerEnable(True)
        self.robot = self.ctrl.AddRobot(1)
        self.robot.SetSpeed(self.speed)
        
        self.connected = True
        atexit.register(self.emergency_stop)
        print("  ✓ 已就绪")
    
    def emergency_stop(self, reason="程序退出"):
        """紧急停止"""
        if not self.connected:
            return
        
        print(f"\n[!] 紧急停止: {reason}")
        try:
            print("  → 移动到安全位姿...")
            self.robot.MoveJ(LocationJ(*self.emergency_pose))
            time.sleep(2)
        except:
            pass
        
        try:
            print("  → 伺服下电...")
            self.ctrl.SetPowerEnable(False)
            print("  ✓ 已关闭")
        except:
            pass
        
        self.connected = False
    
    def check_limits(self, angles):
        """检查关节限位"""
        for i, (name, (lo, hi)) in enumerate(self.joint_limits.items()):
            if i >= len(angles):
                break
            if not (lo <= angles[i] <= hi):
                return False, f"{name} 超限: {angles[i]} (范围 [{lo}, {hi}])"
        return True, "OK"
    
    def move_to_pose(self, pose_name, wait=None):
        """移动到预设位姿"""
        if wait is None:
            wait = self.move_wait
        
        angles = self.cfg.get_pose(pose_name)
        return self.move_joints(angles, desc=pose_name, wait=wait)
    
    def move_joints(self, angles, desc="", wait=None):
        """移动到指定关节角度"""
        if wait is None:
            wait = self.move_wait
        
        ok, msg = self.check_limits(angles)
        if not ok:
            print(f"  ✗ [限位] {msg}")
            return False
        
        desc_str = f" ({desc})" if desc else ""
        print(f"  → 移动{desc_str}...")
        self.robot.MoveJ(LocationJ(*angles))
        time.sleep(wait)
        return True
    
    def execute_sequence(self, sequence_name):
        """执行动作序列"""
        sequence = self.cfg.get_sequence(sequence_name)
        
        print(f"\n[执行序列] {sequence.get('name', sequence_name)}")
        print(f"  描述: {sequence.get('description', 'N/A')}")
        
        repeat = sequence.get('repeat', 1)
        poses = sequence.get('poses', [])
        
        for r in range(repeat):
            if repeat > 1:
                print(f"\n  --- 循环 {r+1}/{repeat} ---")
            
            for step in poses:
                self._execute_step(step)
        
        print(f"\n✓ 序列完成: {sequence_name}")
    
    def _execute_step(self, step):
        """执行单步动作"""
        wait = step.get('wait', self.move_wait)
        
        # 位姿移动
        if 'pose' in step:
            pose_name = step['pose']
            angles = self.cfg.get_pose(pose_name)
            
            # 应用偏移
            if 'offset' in step:
                offset = step['offset']
                angles = [a + o for a, o in zip(angles, offset)]
            
            self.move_joints(angles, desc=pose_name, wait=wait)
        
        # 直接关节角度
        elif 'joints' in step:
            angles = step['joints']
            self.move_joints(angles, wait=wait)
        
        # 夹爪动作
        elif 'action' in step:
            action = step['action']
            print(f"  → [夹爪] {action}")
            # 这里可以添加实际的夹爪控制
            time.sleep(wait)


def list_sequences(config):
    """列出可用序列"""
    print("\n可用动作序列:")
    print("-" * 40)
    sequences = config.config.get('sequences', {})
    for name, data in sequences.items():
        print(f"  {name}")
        print(f"    名称: {data.get('name', 'N/A')}")
        print(f"    描述: {data.get('description', 'N/A')}")
        print(f"    步骤: {len(data.get('poses', []))}")
        print()


def main():
    print("=" * 50)
    print("YAML 配置动作加载器")
    print("=" * 50)
    
    # 加载配置
    try:
        config = ConfigLoader()
    except Exception as e:
        print(f"[✗] 配置加载失败: {e}")
        return
    
    # 检查参数
    if len(sys.argv) < 2:
        print("\n用法: python3 action_loader.py <sequence_name>")
        list_sequences(config)
        return
    
    sequence_name = sys.argv[1]
    
    # 列出模式
    if sequence_name in ['-l', '--list', 'list']:
        list_sequences(config)
        return
    
    # 执行序列
    try:
        arm = ArmController(config)
        arm.connect()
        arm.execute_sequence(sequence_name)
        arm.emergency_stop("正常完成")
        
    except ValueError as e:
        print(f"\n[✗] {e}")
        list_sequences(config)
    except KeyboardInterrupt:
        print("\n[!] 用户中断")
    except Exception as e:
        print(f"\n[✗] 错误: {e}")


if __name__ == "__main__":
    main()
