#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
挥手动作包装器

使用 multiprocessing 在完全隔离的进程中执行挥手动作，
避免段错误影响主进程。
"""

import os
import sys
import time
import signal
import multiprocessing
from typing import Optional, Tuple


def _wave_process_main(result_queue, ip: str, timeout: int):
    """
    子进程执行的挥手动作
    
    在一个完全独立的进程中执行，与主进程完全隔离
    """
    # 重置信号处理
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    signal.signal(signal.SIGTERM, signal.SIG_DFL)
    
    try:
        # 导入并执行
        from wave_hand_safe import WaveHandController
        
        controller = WaveHandController(ip=ip, timeout=timeout)
        
        if not controller.connect():
            result_queue.put((False, "连接失败"))
            return
        
        try:
            success = controller.wave_hand(times=3, go_home_after=True)
            result_queue.put((success, "成功" if success else "执行失败但已恢复"))
        except Exception as e:
            result_queue.put((False, f"执行异常: {e}"))
        finally:
            controller.disconnect()
            
    except Exception as e:
        result_queue.put((False, f"进程异常: {e}"))


class WaveHandWrapper:
    """
    挥手动作包装器
    
    使用 multiprocessing 完全隔离执行环境
    """
    
    def __init__(self, ip: str = "192.168.3.100", timeout: int = 15):
        self.ip = ip
        self.timeout = timeout
    
    def execute(self) -> Tuple[bool, str]:
        """
        执行挥手动作
        
        Returns:
            (是否成功, 消息)
        """
        # 使用 multiprocessing 创建完全独立的进程
        ctx = multiprocessing.get_context('spawn')  # spawn 模式完全隔离
        result_queue = ctx.Queue()
        
        process = ctx.Process(
            target=_wave_process_main,
            args=(result_queue, self.ip, self.timeout)
        )
        
        print(f"[WaveWrapper] 启动挥手进程...")
        process.start()
        
        # 等待结果
        process.join(timeout=self.timeout + 5)
        
        if process.is_alive():
            print("[WaveWrapper] 进程超时，强制终止...")
            process.terminate()
            process.join(timeout=2)
            if process.is_alive():
                process.kill()
            return False, "执行超时"
        
        # 获取结果
        exit_code = process.exitcode
        
        if exit_code is None:
            return False, "进程异常结束"
        elif exit_code < 0:
            # 负数表示被信号终止
            if exit_code == -signal.SIGSEGV:
                return False, "段错误 (SIGSEGV)"
            elif exit_code == -signal.SIGABRT:
                return False, "异常终止 (SIGABRT)"
            else:
                return False, f"被信号终止 ({exit_code})"
        elif exit_code != 0:
            return False, f"返回非零码 ({exit_code})"
        
        # 获取队列中的结果
        try:
            success, msg = result_queue.get(timeout=1)
            return success, msg
        except:
            return exit_code == 0, "执行完成"


def test_wrapper():
    """测试包装器"""
    print("="*60)
    print("挥手动作包装器测试")
    print("="*60)
    
    wrapper = WaveHandWrapper(timeout=15)
    
    print("\n执行挥手...")
    start = time.time()
    
    success, msg = wrapper.execute()
    
    elapsed = time.time() - start
    
    print(f"\n结果: {'成功' if success else '失败'}")
    print(f"消息: {msg}")
    print(f"耗时: {elapsed:.1f}秒")


if __name__ == "__main__":
    test_wrapper()
