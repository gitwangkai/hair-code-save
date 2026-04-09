"""
interaction/voice_manager.py
语音交互模块：根据状态变化播报语音提示。
完全被动：只监听事件，不主动查询其他模块。
"""

from __future__ import annotations
import threading
from config.settings import VoiceConfig
from utils.event_bus import EventBus
from utils.logger import get_logger
from control.state_machine import State


# 状态转移对应的语音文本
_STATE_VOICES: dict[tuple[State, State], str] = {
    (State.IDLE,      State.SEARCHING):     "开始寻找跟随目标",
    (State.SEARCHING, State.FOLLOWING):     "已锁定目标，开始跟随",
    (State.FOLLOWING, State.LOST):          "目标丢失，等待重新出现",
    (State.FOLLOWING, State.OBSTACLE_STOP): "前方有障碍物，暂停移动",
    (State.OBSTACLE_STOP, State.FOLLOWING): "障碍物已清除，继续跟随",
    (State.LOST,      State.SEARCHING):     "正在重新搜索目标",
    (State.FOLLOWING, State.IDLE):          "已停止跟随",
    (State.FOLLOWING, State.CHARGING):      "电量不足，返回充电",
}


class VoiceManager:
    def __init__(self, config: VoiceConfig, bus: EventBus):
        self._config = config
        self._bus = bus
        self._logger = get_logger("VoiceManager")
        self._running = False

    async def start(self):
        """启动语音管理器"""
        self._running = True
        self._bus.subscribe("state_changed", self.on_state_changed)
        self._bus.subscribe("system/alert", self.speak_alert)

    async def stop(self):
        """停止语音管理器"""
        self._running = False

    async def announce_state(self, data):
        """播报状态变化（兼容接口）"""
        self.on_state_changed(data)

    async def speak_alert(self, data):
        """播报告警"""
        text = data.get("message", "注意")
        self._speak(text)

    def on_state_changed(self, payload: dict) -> None:
        if not self._config.enabled:
            return
        key = (payload["from"], payload["to"])
        text = _STATE_VOICES.get(key)
        if text:
            threading.Thread(target=self._speak, args=(text,), daemon=True).start()

    def _speak(self, text: str) -> None:
        self._logger.info(f"语音播报: {text}")
        try:
            import subprocess
            subprocess.run(
                ["espeak-ng", "-v", self._config.language,
                 "-a", str(int(self._config.volume * 100)), text],
                check=False, capture_output=True
            )
        except Exception as e:
            self._logger.warning(f"TTS 播报失败: {e}")
