#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
挥手动作脚本 - 完整版

功能: 执行挥手动作并在完成后回到初始位姿 [0,0,0,0,0,0]

完整流程:
1. 连接机械臂
2. 回到初始位姿 [0,0,0,0,0,0]
3. 移动到准备姿势
4. 执行挥手 (左右摆动3次)
5. 回到初始位姿 [0,0,0,0,0,0] (必须执行)
6. 断开连接
"""

import time
import os
import math
import sys
import signal
import atexit
from typing import List, Tuple


class WaveHandController:
    """挥手动作控制器"""
    
    # 关节限位
    JOINT_LIMITS = {
        "J1": {"min": -70.0,  "max": 200.0},
        "J2": {"min":   0.0,  "max": 120.0},
        "J3": {"min": -55.0,  "max":  55.0},
        "J4": {"min":   0.0,  "max": 120.0},
        "J5": {"min": -85.0,  "max":  85.0},
        "J6": {"min": -20.0,  "max":  20.0},
    }
    
    # ========== 初始位姿 [0,0,0,0,0,0] ==========
    HOME_POSE = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    
    # 挥手准备姿势
    WAVE_PREPARE = [64.3, 0.0, 13.2, 85.9, -84.8, 0.0, 0.0]
    
    # 挥手摆动
    WAVE_LEFT = [64.3, 0.0, 20.0, 85.9, -84.8, 0.0, 0.0]
    WAVE_RIGHT = [64.3, 0.0, -20.0, 85.9, -84.8, 0.0, 0.0]
    
    def __init__(self, ip: str = "192.168.3.100", timeout: int = 10):
        self.ip = ip
        self.timeout = timeout
        self.ctrl = None
        self.robot = None
        self.connected = False
        self.home_reached = False
        
        # SDK
        self.Controller = None
        self.LocationJ = None
        self.HiddenDataType = None
        self.ComPort = None
        
        # 注册退出清理
        atexit.register(self._ensure_home)
    
    def _ensure_home(self):
        """确保回到初始位姿 [0,0,0,0,0,0]"""
        if self.connected and self.ctrl and not self.home_reached:
            print("\n[!] 紧急恢复: 回到初始位姿 [0,0,0,0,0,0]...")
            try:
                self.robot.MoveJ(self.LocationJ(0, 0, 0, 0, 0, 0))
                time.sleep(1.0)
                self.ctrl.SetPowerEnable(False)
                print("[!] 已回到初始位姿并下电")
            except Exception as e:
                print(f"[!] 紧急恢复失败: {e}")
    
    def _import_sdk(self) -> bool:
        """导入 PallasSDK"""
        try:
            from PallasSDK import Controller, HiddenDataType, ComPort
            from PallasSDK import LocationJ
            self.Controller = Controller
            self.LocationJ = LocationJ
            self.HiddenDataType = HiddenDataType
            self.ComPort = ComPort
            return True
        except ImportError as e:
            print(f"[错误] 无法导入 PallasSDK: {e}")
            return False
    
    def _check_limits(self, angles: List[float]) -> Tuple[bool, str]:
        """检查关节限位"""
        for i, (key, limits) in enumerate(self.JOINT_LIMITS.items()):
            if i < len(angles):
                angle = angles[i]
                if not (limits["min"] <= angle <= limits["max"]):
                    return False, f"{key}={angle:.1f}° 超限"
        return True, ""
    
    def _move_to(self, angles: List[float], desc: str = "", delay: float = 1.0) -> bool:
        """移动到指定姿势"""
        if not self.robot:
            return False
        
        ok, msg = self._check_limits(angles)
        if not ok:
            print(f"[限位] {msg}")
            return False
        
        try:
            self.robot.MoveJ(self.LocationJ(*angles[:6]))
            if delay > 0:
                time.sleep(delay)
            return True
        except Exception as e:
            print(f"[移动失败] {e}")
            return False
    
    def connect(self) -> bool:
        """连接机械臂"""
        print(f"\n[1/6] 连接机械臂 {self.ip}...")
        
        if not self._import_sdk():
            return False
        
        def timeout_handler(signum, frame):
            raise TimeoutError("连接超时")
        
        old_handler = signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(self.timeout)
        
        try:
            self.ctrl = self.Controller()
            self.ctrl.Connect(self.ip)
            signal.alarm(0)
            signal.signal(signal.SIGALRM, old_handler)
            
            self.ctrl.SetHiddenOn(self.HiddenDataType.RobotJointPos)
            
            # 灵巧手(可选)
            try:
                self.ctrl.ComOpen("COM2", self.ComPort.Com_485, 115200, 8, 1, 0, True)
            except:
                pass
            
            print("[1/6] 伺服上电...")
            self.ctrl.SetPowerEnable(True)
            time.sleep(0.5)
            
            self.robot = self.ctrl.AddRobot(1)
            self.robot.SetFrameType(1)
            self.robot.SetSpeed(30)
            
            self.connected = True
            print("[1/6] ✓ 连接成功")
            return True
            
        except TimeoutError:
            signal.signal(signal.SIGALRM, old_handler)
            print("[错误] 连接超时")
            return False
        except Exception as e:
            signal.alarm(0)
            signal.signal(signal.SIGALRM, old_handler)
            print(f"[错误] 连接失败: {e}")
            return False
    
    def disconnect(self):
        """断开连接"""
        if self.ctrl:
            print("\n[6/6] 断开连接...")
            try:
                self.ctrl.SetPowerEnable(False)
            except:
                pass
            try:
                self.ctrl.ComClose("COM2")
            except:
                pass
            self.ctrl = None
        self.robot = None
        self.connected = False
        print("[6/6] ✓ 已断开")
    
    def wave_hand(self, times: int = 3) -> bool:
        """
        执行挥手动作
        
        流程:
        1. 回到初始位姿 [0,0,0,0,0,0]
        2. 移动到准备姿势
        3. 挥手 (左右摆动)
        4. 回到初始位姿 [0,0,0,0,0,0] (必须执行)
        """
        if not self.connected:
            print("[错误] 未连接机械臂")
            return False
        
        wave_success = False
        
        try:
            print("\n" + "="*60)
            print("  开始挥手动作")
            print("="*60)
            
            # ========== 步骤2: 回到初始位姿 [0,0,0,0,0,0] ==========
            print("\n[2/6] 回到初始位姿 [0,0,0,0,0,0]...")
            if self._move_to(self.HOME_POSE, "HOME", delay=1.5):
                print("[2/6] ✓ 已到达初始位姿")
            else:
                raise RuntimeError("无法回到初始位姿")
            
            # ========== 步骤3: 移动到准备姿势 ==========
            print("\n[3/6] 移动到准备姿势...")
            if self._move_to(self.WAVE_PREPARE, "准备", delay=1.5):
                print("[3/6] ✓ 已到达准备姿势")
            else:
                raise RuntimeError("无法移动到准备姿势")
            
            # ========== 步骤4: 执行挥手 ==========
            print(f"\n[4/6] 挥手 {times} 次...")
            for i in range(times):
                print(f"       第 {i+1}/{times} 次")
                self._move_to(self.WAVE_LEFT, "左摆", delay=0.3)
                self._move_to(self.WAVE_RIGHT, "右摆", delay=0.3)
            print("[4/6] ✓ 挥手完成")
            wave_success = True
            
            # ========== 步骤5: 回到初始位姿 [0,0,0,0,0,0] ==========
            print("\n[5/6] 回到初始位姿 [0,0,0,0,0,0]...")
            if self._move_to(self.HOME_POSE, "HOME", delay=1.5):
                self.home_reached = True
                print("[5/6] ✓ 已到达初始位姿")
            
        except Exception as e:
            print(f"\n[错误] {e}")
            wave_success = False
        
        finally:
            # 确保回到初始位姿
            if not self.home_reached:
                print("\n[!] 恢复: 回到初始位姿 [0,0,0,0,0,0]...")
                try:
                    self._move_to(self.HOME_POSE, "HOME", delay=1.0)
                    self.home_reached = True
                    print("[!] ✓ 已到达初始位姿")
                except Exception as e:
                    print(f"[!] 恢复失败: {e}")
            
            print("\n" + "="*60)
            if wave_success:
                print("  挥手成功 - 已回到初始位姿 [0,0,0,0,0,0]")
            else:
                print("  挥手失败 - 已回到初始位姿 [0,0,0,0,0,0]")
            print("="*60)
        
        return wave_success


def main():
    """主函数"""
    print("="*60)
    print("  挥手动作 - 完成后回到初始位姿")
    print("="*60)
    
    controller = WaveHandController()
    
    if not controller.connect():
        print("\n[退出] 连接失败")
        return 1
    
    try:
        success = controller.wave_hand(times=3)
        return 0 if success else 1
    except KeyboardInterrupt:
        print("\n[!] 用户中断")
        return 1
    finally:
        controller.disconnect()


if __name__ == "__main__":
    sys.exit(main())
