#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
挥手动作联动模块

功能:
- 检测到人时触发机械臂挥手动作
- 同步播放音频文件
- 支持触发间隔控制 (防重复触发)
- 支持动态修改配置

重要: 使用完全独立的子进程执行 PallasSDK 操作，避免与 Flask 冲突
"""

import os
import sys
import time
import threading
import subprocess
from typing import Optional, Callable


class WaveActionController:
    """
    挥手动作控制器
    
    管理机械臂挥手动作和音频播放的联动，支持触发间隔控制。
    使用完全独立的子进程执行 PallasSDK 操作，避免与 Flask 的冲突。
    """
    
    def __init__(
        self,
        wave_script: str = "/home/aidlux/human_detection/src/wave_hand_safe.py",
        audio_file: str = "/home/aidlux/auto.mp3",
        min_interval: float = 60.0,
        on_trigger: Optional[Callable[[], None]] = None,
        on_complete: Optional[Callable[[bool], None]] = None
    ):
        """
        初始化挥手动作控制器
        
        Args:
            wave_script: 挥手脚本路径 (必须是完全独立的脚本)
            audio_file: 音频文件路径
            min_interval: 最短触发间隔(秒)，默认60秒
            on_trigger: 触发时的回调函数
            on_complete: 完成时的回调函数(参数: success)
        """
        self.wave_script = wave_script
        self.audio_file = audio_file
        self.min_interval = min_interval
        
        # 回调函数
        self.on_trigger = on_trigger
        self.on_complete = on_complete
        
        # 状态
        self.last_trigger_time = 0.0
        self.is_running = False
        self._lock = threading.Lock()
        
        # 统计
        self.trigger_count = 0
        self.skip_count = 0
        
        # 检测音频播放器
        self.audio_player = self._detect_audio_player()
        
        print(f"[WaveAction] 初始化完成")
        print(f"  挥手脚本: {self.wave_script}")
        print(f"  音频文件: {self.audio_file}")
        print(f"  音频播放器: {self.audio_player or '未检测到'}")
        print(f"  触发间隔: {self.min_interval}秒")
    
    def _detect_audio_player(self) -> str:
        """检测可用的音频播放器"""
        players = ["ffplay", "mpg123"]
        
        for player in players:
            try:
                subprocess.run(
                    ["which", player],
                    check=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                return player
            except:
                continue
        
        return ""
    
    def set_interval(self, interval: float):
        """设置最短触发间隔"""
        if interval < 0:
            interval = 0
        
        with self._lock:
            old_interval = self.min_interval
            self.min_interval = interval
        
        print(f"[WaveAction] 触发间隔已更新: {old_interval}秒 -> {interval}秒")
        return self.min_interval
    
    def get_interval(self) -> float:
        """获取当前触发间隔"""
        return self.min_interval
    
    def get_remaining_cooldown(self) -> float:
        """获取剩余冷却时间"""
        elapsed = time.time() - self.last_trigger_time
        remaining = max(0, self.min_interval - elapsed)
        return remaining
    
    def can_trigger(self) -> bool:
        """检查是否可以触发"""
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
            # 检查是否正在运行
            if self.is_running:
                print("[WaveAction] 动作正在执行中，跳过")
                return False
            
            # 检查间隔
            remaining = self.get_remaining_cooldown()
            if not force and remaining > 0:
                print(f"[WaveAction] 冷却中，还剩 {remaining:.1f} 秒，跳过")
                self.skip_count += 1
                return False
            
            # 标记为运行中
            self.is_running = True
            self.last_trigger_time = time.time()
            self.trigger_count += 1
        
        # 触发回调
        if self.on_trigger:
            try:
                self.on_trigger()
            except Exception as e:
                print(f"[WaveAction] 触发回调出错: {e}")
        
        print(f"[WaveAction] 触发挥手动作 (#{self.trigger_count})")
        
        # 在后台线程执行
        thread = threading.Thread(target=self._execute_wave, daemon=True)
        thread.start()
        
        return True
    
    def _execute_wave(self):
        """执行挥手动作 (在后台线程运行)"""
        wave_success = False
        audio_success = False
        
        try:
            # 使用线程并行执行挥手和音频
            wave_result = [False]
            audio_result = [False]
            
            def run_wave():
                try:
                    wave_result[0] = self._run_wave_script()
                except Exception as e:
                    print(f"[WaveAction] 挥手线程异常: {e}")
                    wave_result[0] = False
            
            def run_audio():
                try:
                    audio_result[0] = self._play_audio()
                except Exception as e:
                    print(f"[WaveAction] 音频线程异常: {e}")
                    audio_result[0] = False
            
            wave_thread = threading.Thread(target=run_wave, daemon=True)
            audio_thread = threading.Thread(target=run_audio, daemon=True)
            
            wave_thread.start()
            audio_thread.start()
            
            # 等待两者完成，最多等待35秒
            wave_thread.join(timeout=35)
            audio_thread.join(timeout=35)
            
            wave_success = wave_result[0]
            audio_success = audio_result[0]
            
        except Exception as e:
            print(f"[WaveAction] 执行出错: {e}")
            import traceback
            traceback.print_exc()
        
        finally:
            with self._lock:
                self.is_running = False
            
            # 完成回调
            success = wave_success or audio_success
            if self.on_complete:
                try:
                    self.on_complete(success)
                except Exception as e:
                    print(f"[WaveAction] 完成回调出错: {e}")
            
            print(f"[WaveAction] 完成: 挥手={'成功' if wave_success else '失败'}, 音频={'成功' if audio_success else '失败'}")
    
    def _run_wave_script(self) -> bool:
        """运行挥手脚本 - 使用 multiprocessing 完全隔离"""
        script_to_run = self.wave_script
        
        if not os.path.exists(script_to_run):
            print(f"[WaveAction] 错误: 挥手脚本不存在: {script_to_run}")
            return False
        
        try:
            print(f"[WaveAction] 执行挥手: {os.path.basename(script_to_run)}")
            
            # 方案1: 使用 wave_hand_wrapper (完全隔离)
            wrapper_path = os.path.join(os.path.dirname(__file__), "wave_hand_wrapper.py")
            if os.path.exists(wrapper_path):
                import subprocess
                result = subprocess.run(
                    ["timeout", "25", "python3", wrapper_path],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                # 处理输出
                if result.stdout:
                    lines = result.stdout.strip().split('\n')
                    for line in lines[-15:]:
                        if line.strip():
                            print(f"  [挥手] {line}")
                
                if result.returncode == 0:
                    print("[WaveAction] 挥手执行成功")
                    return True
                else:
                    print(f"[WaveAction] 挥手执行失败 (返回码: {result.returncode})")
                    return False
            
            # 方案2: 直接执行脚本 (备用)
            else:
                import subprocess
                result = subprocess.run(
                    ["timeout", "30", "python3", script_to_run],
                    capture_output=True,
                    text=True,
                    timeout=35
                )
                
                if result.stdout:
                    lines = result.stdout.strip().split('\n')
                    for line in lines[-15:]:
                        if line.strip():
                            print(f"  [挥手] {line}")
                
                if result.returncode == 0:
                    print("[WaveAction] 挥手执行成功")
                    return True
                else:
                    print(f"[WaveAction] 挥手执行失败 (返回码: {result.returncode})")
                    return False
                
        except subprocess.TimeoutExpired:
            print("[WaveAction] 挥手执行超时")
            return False
        except Exception as e:
            print(f"[WaveAction] 挥手执行异常: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def _play_audio(self) -> bool:
        """播放音频文件"""
        if not os.path.exists(self.audio_file):
            print(f"[WaveAction] 警告: 音频文件不存在: {self.audio_file}")
            return False
        
        if not self.audio_player:
            print("[WaveAction] 警告: 未找到音频播放器")
            return False
        
        try:
            print(f"[WaveAction] 播放音频 ({self.audio_player})...")
            
            if self.audio_player == "ffplay":
                # ffplay -nodisp 不显示窗口 -autoexit 自动退出
                result = subprocess.run(
                    ["ffplay", "-nodisp", "-autoexit", "-loglevel", "quiet", self.audio_file],
                    capture_output=True,
                    timeout=10
                )
                success = result.returncode == 0
                
            elif self.audio_player == "mpg123":
                # 使用 timeout 确保不会挂起
                result = subprocess.run(
                    ["timeout", "8", "mpg123", "-q", self.audio_file],
                    capture_output=True,
                    timeout=10
                )
                success = result.returncode == 0
                if result.returncode == 124:
                    print("[WaveAction] 音频播放超时(音频设备可能不可用)")
                    return False
            
            else:
                print(f"[WaveAction] 未知的音频播放器: {self.audio_player}")
                return False
            
            if success:
                print("[WaveAction] 音频播放完成")
            else:
                print(f"[WaveAction] 音频播放失败 (返回码: {result.returncode})")
            
            return success
            
        except subprocess.TimeoutExpired:
            print("[WaveAction] 音频播放超时(音频设备可能不可用)")
            return False
        except Exception as e:
            print(f"[WaveAction] 音频播放异常: {e}")
            return False
    
    def stop(self):
        """停止当前动作"""
        print("[WaveAction] 停止动作")
        self.is_running = False
    
    def get_stats(self) -> dict:
        """获取统计信息"""
        return {
            "trigger_count": self.trigger_count,
            "skip_count": self.skip_count,
            "is_running": self.is_running,
            "min_interval": self.min_interval,
            "remaining_cooldown": self.get_remaining_cooldown(),
            "can_trigger": self.can_trigger(),
            "audio_player": self.audio_player
        }
    
    def reset_stats(self):
        """重置统计"""
        self.trigger_count = 0
        self.skip_count = 0
        print("[WaveAction] 统计已重置")


class MockWaveActionController(WaveActionController):
    """模拟挥手动作控制器 (用于测试)"""
    
    def _run_wave_script(self) -> bool:
        """模拟挥手动作"""
        print("[WaveAction-Mock] 模拟挥手动作 (3秒)...")
        time.sleep(3)
        print("[WaveAction-Mock] 挥手完成")
        return True
    
    def _play_audio(self) -> bool:
        """模拟音频播放"""
        print("[WaveAction-Mock] 模拟音频播放 (2秒)...")
        time.sleep(2)
        print("[WaveAction-Mock] 音频播放完成")
        return True


# ============ Web GUI 集成功能 ============

class WaveActionWebInterface:
    """WaveAction 的 Web 接口封装"""
    
    def __init__(self, controller: WaveActionController, socketio):
        self.controller = controller
        self.socketio = socketio
        self._register_events()
    
    def _register_events(self):
        """注册 SocketIO 事件"""
        
        @self.socketio.on('wave_trigger')
        def handle_wave_trigger(data):
            """手动触发挥手"""
            try:
                force = data.get('force', False)
                success = self.controller.trigger(force=force)
                self.socketio.emit('wave_result', {
                    'success': success,
                    'forced': force,
                    'stats': self.controller.get_stats()
                })
            except Exception as e:
                print(f"[WaveAction-WS] 触发出错: {e}")
                self.socketio.emit('wave_error', {'message': str(e)})
        
        @self.socketio.on('wave_set_interval')
        def handle_set_interval(data):
            """设置触发间隔"""
            try:
                interval = data.get('interval', 60)
                new_interval = self.controller.set_interval(interval)
                self.socketio.emit('wave_config', {
                    'min_interval': new_interval,
                    'message': f'触发间隔已设置为 {new_interval}秒'
                })
            except Exception as e:
                print(f"[WaveAction-WS] 设置间隔出错: {e}")
        
        @self.socketio.on('wave_get_status')
        def handle_get_status():
            """获取状态"""
            try:
                self.socketio.emit('wave_status', self.controller.get_stats())
            except Exception as e:
                print(f"[WaveAction-WS] 获取状态出错: {e}")
        
        @self.socketio.on('wave_stop')
        def handle_stop():
            """停止动作"""
            try:
                self.controller.stop()
                self.socketio.emit('wave_status', {
                    **self.controller.get_stats(),
                    'message': '动作已停止'
                })
            except Exception as e:
                print(f"[WaveAction-WS] 停止出错: {e}")
        
        @self.socketio.on('wave_reset_stats')
        def handle_reset_stats():
            """重置统计"""
            try:
                self.controller.reset_stats()
                self.socketio.emit('wave_status', self.controller.get_stats())
            except Exception as e:
                print(f"[WaveAction-WS] 重置统计出错: {e}")


if __name__ == "__main__":
    # 测试
    print("=" * 50)
    print("挥手动作控制器测试")
    print("=" * 50)
    
    controller = MockWaveActionController(min_interval=5)
    
    print("\n测试1: 正常触发")
    result = controller.trigger()
    
    # 等待完成
    while controller.is_running:
        time.sleep(0.5)
    
    print("\n测试2: 间隔内重复触发")
    result = controller.trigger()
    print(f"结果: {result}")
    
    print("\n测试完成!")
    print(f"统计: {controller.get_stats()}")
