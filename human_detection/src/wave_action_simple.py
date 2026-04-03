#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
挥手动作联动模块 - 简化版 (每次检测都触发)

功能:
- 检测到人时触发挥手动作
- 每次检测都播放音频 (无间隔限制)
- 调用独立脚本执行: 连接→挥手→断开
"""

import os
import sys
import time
import threading
import subprocess
from typing import Optional, Callable


class SimpleWaveActionController:
    """简化版挥手动作控制器 - 每次检测都触发"""
    
    def __init__(
        self,
        audio_file: str = "/home/aidlux/auto.mp3",
        min_interval: float = 0,  # 默认0，每次检测都触发
        on_trigger: Optional[Callable[[], None]] = None,
        on_complete: Optional[Callable[[bool], None]] = None
    ):
        self.audio_file = audio_file
        self.min_interval = min_interval  # 触发间隔，0表示每次检测都触发
        self.on_trigger = on_trigger
        self.on_complete = on_complete
        
        self.last_trigger_time = 0.0
        self.is_running = False
        self._lock = threading.Lock()
        
        self.trigger_count = 0
        self.skip_count = 0
        
        # 挥手脚本路径
        self.wave_script = "/home/aidlux/human_detection/src/wave_hand_fast.py"
        
        print(f"[SimpleWave] 初始化完成")
        print(f"  挥手脚本: {self.wave_script}")
        print(f"  触发间隔: {self.min_interval}秒 (0=每次检测都触发)")
    
    def set_interval(self, interval: float):
        """设置触发间隔"""
        if interval < 0:
            interval = 0
        with self._lock:
            old = self.min_interval
            self.min_interval = interval
        print(f"[SimpleWave] 触发间隔: {old}秒 → {interval}秒")
        return self.min_interval
    
    def get_interval(self) -> float:
        return self.min_interval
    
    def get_remaining_cooldown(self) -> float:
        """获取剩余冷却时间"""
        if self.min_interval <= 0:
            return 0  # 无冷却
        elapsed = time.time() - self.last_trigger_time
        return max(0, self.min_interval - elapsed)
    
    def can_trigger(self) -> bool:
        """检查是否可以触发"""
        # 如果没有间隔限制，只要不在运行中就可以触发
        if self.min_interval <= 0:
            return not self.is_running
        # 有间隔限制时检查冷却时间
        return self.get_remaining_cooldown() <= 0 and not self.is_running
    
    def trigger(self, force: bool = False) -> bool:
        """
        触发挥手动作
        
        Args:
            force: 是否强制触发(忽略间隔限制)
            
        Returns:
            是否成功触发
        """
        with self._lock:
            if self.is_running:
                print("[SimpleWave] 动作执行中，跳过")
                return False
            
            # 检查间隔 (如果没有设置force且设置了间隔)
            if not force and self.min_interval > 0:
                remaining = self.get_remaining_cooldown()
                if remaining > 0:
                    print(f"[SimpleWave] 冷却中 ({remaining:.0f}秒)，跳过")
                    self.skip_count += 1
                    return False
            
            self.is_running = True
            self.last_trigger_time = time.time()
            self.trigger_count += 1
        
        if self.on_trigger:
            try:
                self.on_trigger()
            except:
                pass
        
        print(f"\n[SimpleWave] === 触发 #{self.trigger_count} ===")
        
        thread = threading.Thread(target=self._execute_action, daemon=True)
        thread.start()
        return True
    
    def _execute_action(self):
        """执行挥手动作"""
        wave_ok = False
        
        try:
            print("[SimpleWave] 启动挥手动作...")
            
            # 执行挥手脚本
            wave_ok = self._run_wave_script()
            
        except Exception as e:
            print(f"[SimpleWave] 执行异常: {e}")
        finally:
            with self._lock:
                self.is_running = False
            
            if self.on_complete:
                try:
                    self.on_complete(wave_ok)
                except:
                    pass
            
            status = "成功" if wave_ok else "失败"
            print(f"[SimpleWave] === 完成: {status} ===")
    
    def _run_wave_script(self) -> bool:
        """执行挥手脚本"""
        if not os.path.exists(self.wave_script):
            print(f"[SimpleWave] 错误: 脚本不存在 {self.wave_script}")
            return False
        
        try:
            print("[SimpleWave] 执行挥手...")
            
            # 执行脚本 (15秒超时)
            result = subprocess.run(
                ["timeout", "15", "python3", self.wave_script],
                capture_output=True,
                text=True,
                timeout=18
            )
            
            # 输出关键信息
            if result.stdout:
                lines = result.stdout.strip().split('\n')
                for line in lines[-8:]:
                    if any(k in line for k in ['完成', '原点', '✓', '错误']):
                        print(f"  {line}")
            
            # 判断结果
            if result.returncode == 0:
                print("[SimpleWave] ✓ 挥手成功")
                return True
            else:
                print(f"[SimpleWave] 返回码: {result.returncode}")
                return False
                
        except subprocess.TimeoutExpired:
            print("[SimpleWave] 超时")
            return False
        except Exception as e:
            print(f"[SimpleWave] 异常: {e}")
            return False
    
    def stop(self):
        """停止动作"""
        print("[SimpleWave] 停止")
        self.is_running = False
    
    def reset_stats(self):
        """重置统计"""
        self.trigger_count = 0
        self.skip_count = 0
        print("[SimpleWave] 统计已重置")
    
    def get_stats(self) -> dict:
        """获取统计"""
        return {
            "trigger_count": self.trigger_count,
            "skip_count": self.skip_count,
            "is_running": self.is_running,
            "min_interval": self.min_interval,
            "can_trigger": self.can_trigger()
        }


if __name__ == "__main__":
    print("=" * 60)
    print("挥手控制器测试 - 每次检测都触发")
    print("=" * 60)
    
    ctrl = SimpleWaveActionController(min_interval=0)  # 每次检测都触发
    
    print("\n测试: 触发3次...")
    for i in range(3):
        print(f"\n--- 触发 {i+1} ---")
        ctrl.trigger()
        
        import time
        while ctrl.is_running:
            time.sleep(0.5)
        
        time.sleep(1)  # 短暂间隔
    
    print(f"\n完成! 统计: {ctrl.get_stats()}")
