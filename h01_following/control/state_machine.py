"""
control/state_machine.py
跟随状态机：管理机器人行为状态，驱动模式切换。
状态：IDLE → SEARCHING → FOLLOWING → OBSTACLE_STOP → LOST → IDLE
"""

from __future__ import annotations
import time
from enum import Enum, auto

try:
    from rclpy.node import Node
    from rclpy.clock import Clock
    ROS_AVAILABLE = True
except ImportError:
    ROS_AVAILABLE = False
    Node = object

from config.settings import StateConfig
from utils.event_bus import EventBus
from utils.logger import get_logger


class State(Enum):
    IDLE          = auto()   # 待机
    SEARCHING     = auto()   # 搜索目标
    FOLLOWING     = auto()   # 正在跟随
    OBSTACLE_STOP = auto()   # 障碍物停止
    LOST          = auto()   # 目标丢失，等待重现
    CHARGING      = auto()   # 低电量返回充电


# 合法状态转移表
_TRANSITIONS: dict[State, set[State]] = {
    State.IDLE:          {State.SEARCHING},
    State.SEARCHING:     {State.FOLLOWING, State.IDLE},
    State.FOLLOWING:     {State.OBSTACLE_STOP, State.LOST, State.IDLE, State.CHARGING},
    State.OBSTACLE_STOP: {State.FOLLOWING, State.LOST},
    State.LOST:          {State.FOLLOWING, State.SEARCHING, State.IDLE},
    State.CHARGING:      {State.IDLE},
}


class StateMachine:
    """StateMachine 别名，兼容 main.py 接口（非 ROS 节点版本）"""
    
    def __init__(self, config, event_bus):
        self._config = config
        self._bus = event_bus
        self._sm = None
        self._running = False
        self._logger = get_logger("StateMachine")
    
    async def start(self):
        """启动状态机"""
        self._running = True
        try:
            # 尝试创建 ROS 节点版本
            self._sm = FollowingStateMachine(self._config, self._bus)
        except Exception as e:
            self._logger.warning(f"无法创建 ROS 状态机: {e}，使用简化版本")
            self._sm = SimpleStateMachine(self._config, self._bus)
    
    async def stop(self):
        """停止状态机"""
        self._running = False
        if self._sm:
            await self._sm.stop()
    
    async def update_position(self, data):
        """更新位置（兼容接口）"""
        if self._sm:
            self._bus.publish("target_pose", data)


class SimpleStateMachine:
    """简化版状态机（无 ROS 依赖）"""
    
    def __init__(self, config, bus):
        self._config = config
        self._bus = bus
        self._logger = get_logger("SimpleStateMachine")
        self._state = State.IDLE
        self._last_seen = 0.0
        
        bus.subscribe("target_pose", self._on_target_pose)
    
    def _on_target_pose(self, data):
        self._last_seen = time.time()
        if self._state in (State.SEARCHING, State.LOST):
            self._transition(State.FOLLOWING)
    
    def _transition(self, new_state):
        if new_state != self._state:
            old = self._state
            self._state = new_state
            self._logger.info(f"状态: {old.name} → {new_state.name}")
            self._bus.publish("state_changed", {"from": old, "to": new_state})
            self._bus.publish("follow_command", {"active": new_state == State.FOLLOWING})
    
    async def stop(self):
        pass


class FollowingStateMachine(Node):
    """
    输入事件: target_pose, target_lost, obstacle_detected, cmd_start, cmd_stop
    输出事件: state_changed -> {"from": State, "to": State}
              follow_command -> {"active": bool}
    """

    def __init__(self, config: StateConfig, bus: EventBus):
        super().__init__("state_machine_node")
        self._config = config
        self._bus = bus
        self._logger = get_logger("StateMachine")
        self._state = State.IDLE
        self._last_seen: float = 0.0
        self._search_start: float = 0.0

        # 订阅外部事件
        bus.subscribe("target_pose",       self.on_target_pose)
        bus.subscribe("target_lost",       self._on_target_lost)
        bus.subscribe("obstacle_detected", self._on_obstacle)
        bus.subscribe("obstacle_cleared",  self._on_obstacle_cleared)
        bus.subscribe("cmd_start",         self._on_cmd_start)
        bus.subscribe("cmd_stop",          self._on_cmd_stop)
        bus.subscribe("low_battery",       self._on_low_battery)

        # 定时器：超时检查（1Hz）
        self.create_timer(1.0, self._tick)
        self._logger.info(f"状态机初始化，初始状态: {self._state.name}")

    # ── 公开回调 ───────────────────────────────────────────────
    def on_target_pose(self, payload) -> None:
        self._last_seen = time.time()
        if self._state in (State.SEARCHING, State.LOST):
            self._transition(State.FOLLOWING)

    def _on_target_lost(self, track_id: int) -> None:
        if self._state == State.FOLLOWING:
            self._transition(State.LOST)

    def _on_obstacle(self, _) -> None:
        if self._state == State.FOLLOWING:
            self._transition(State.OBSTACLE_STOP)

    def _on_obstacle_cleared(self, _) -> None:
        if self._state == State.OBSTACLE_STOP:
            self._transition(State.FOLLOWING)

    def _on_cmd_start(self, _) -> None:
        if self._state == State.IDLE:
            self._search_start = time.time()
            self._transition(State.SEARCHING)

    def _on_cmd_stop(self, _) -> None:
        self._transition(State.IDLE)

    def _on_low_battery(self, _) -> None:
        self._transition(State.CHARGING)

    # ── 定时超时检查 ────────────────────────────────────────────
    def _tick(self) -> None:
        now = time.time()
        if self._state == State.SEARCHING:
            if now - self._search_start > self._config.search_timeout:
                self._logger.warning("搜索超时，返回 IDLE")
                self._transition(State.IDLE)
        elif self._state == State.LOST:
            if now - self._last_seen > self._config.lost_timeout:
                self._logger.warning("目标长时间未出现，返回 SEARCHING")
                self._transition(State.SEARCHING)
                self._search_start = now

    # ── 状态转移 ────────────────────────────────────────────────
    def _transition(self, new_state: State) -> None:
        if new_state not in _TRANSITIONS.get(self._state, set()):
            self._logger.warning(
                f"非法转移: {self._state.name} → {new_state.name}，忽略"
            )
            return
        old = self._state
        self._state = new_state
        self._logger.info(f"状态: {old.name} → {new_state.name}")
        self._bus.publish("state_changed", {"from": old, "to": new_state})
        self._bus.publish(
            "follow_command",
            {"active": new_state == State.FOLLOWING}
        )

    @property
    def current_state(self) -> State:
        return self._state
