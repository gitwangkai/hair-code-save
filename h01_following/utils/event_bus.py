"""
utils/event_bus.py
轻量级事件总线：模块间完全解耦，通过事件名通信，不持有彼此引用。
"""

import threading
from collections import defaultdict
from typing import Callable, Any
from utils.logger import get_logger


class EventBus:
    """
    发布-订阅事件总线。
    - 发布者：bus.publish("event_name", payload)
    - 订阅者：bus.subscribe("event_name", callback)
    线程安全，回调在发布者线程中同步执行（轻量，适合 ROS callback 场景）。
    """

    def __init__(self):
        self._subscribers: dict[str, list[Callable]] = defaultdict(list)
        self._lock = threading.Lock()
        self._logger = get_logger("EventBus")

    def subscribe(self, event: str, callback: Callable) -> None:
        with self._lock:
            self._subscribers[event].append(callback)
        self._logger.debug(f"订阅: {event} → {callback.__qualname__}")

    def unsubscribe(self, event: str, callback: Callable) -> None:
        with self._lock:
            self._subscribers[event] = [
                cb for cb in self._subscribers[event] if cb != callback
            ]

    def publish(self, event: str, payload: Any = None) -> None:
        with self._lock:
            callbacks = list(self._subscribers.get(event, []))
        for cb in callbacks:
            try:
                cb(payload)
            except Exception as e:
                self._logger.error(f"事件 '{event}' 处理异常 [{cb.__qualname__}]: {e}")
