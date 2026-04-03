#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
机器人 WebSocket 接口整合 + 交互式菜单
Author: Delisa

⚠️WS_URL = "ws://192.168.112.86:9090" 根据IP修改 192.168.112.86⚠️
"""

import json
from typing import Any, Dict, Optional
import time
import websocket

# WS_URL = "ws://192.168.111.157:9090"
WS_URL = "ws://127.0.0.1:9090"

_request_counter = 0
ARM_SERVICE = "/arm_control_act"
ARM_PUB_TOPIC = "/arm_transform_pose"

def _next_id() -> str:
    global _request_counter
    _request_counter += 1
    return _request_counter


def _pretty_json(data: Any) -> str:
    try:
        return json.dumps(data, ensure_ascii=False, indent=2)
    except TypeError:
        return str(data)


def _print_json_block(title: str, payload: Any) -> None:
    print(f"\n{title}")
    print(_pretty_json(payload))

def call_arm_service(act: str, data: Any = None) -> Dict[str, Any]:
    """封装机械臂专用的服务调用"""
    ws = websocket.create_connection(WS_URL)
    reqid = int(time.time() * 1000)
    
    # 构造与原 ROS2 消息一致的 JSON 结构
    args = {
        "request": json.dumps({
            "reqid": reqid,
            "act": act,
            "data": json.dumps(data) if data is not None else ""
        })
    }
    
    msg = {
        "op": "call_service",
        "service": ARM_SERVICE,
        "args": args,
        "id": f"arm_{act}_{_next_id()}"
    }
    
    print(f"\n➡️ 发送指令 [{act}]: {args}")
    ws.send(json.dumps(msg))
    resp_raw = ws.recv()
    ws.close()
    
    resp = json.loads(resp_raw)
    print(f"✅ 响应: {resp.get('values', {}).get('response', 'no response')}")
    return resp


def publish(topic: str, msg: Dict[str, Any], msg_type: Optional[str] = None) -> None:
    """向指定 topic 发布一次消息，可选显式声明消息类型。"""
    ws = websocket.create_connection(WS_URL)
    try:
        if msg_type:
            advertise_payload = {
                "op": "advertise",
                "topic": topic,
                "type": msg_type,
                "id": _next_id(),
            }
            _print_json_block("➡️ advertise", advertise_payload)
            ws.send(json.dumps(advertise_payload))
        publish_payload = {"op": "publish", "topic": topic, "msg": msg, "id": _next_id()}
        _print_json_block("➡️ 发布", publish_payload)
        ws.send(json.dumps(publish_payload))
        if msg_type:
            unadvertise_payload = {
                "op": "unadvertise",
                "topic": topic,
                "id": _next_id(),
            }
            _print_json_block("➡️ unadvertise", unadvertise_payload)
            ws.send(json.dumps(unadvertise_payload))
    finally:
        ws.close()
    print(f"✅ 已发布 topic: {topic}")
# ====================== 功能实现 ======================

def left_start_arm_poweron():
    """1. 上电"""
    call_arm_service("left_start")

def left_reset_and_poweroff():
    """2. 复位并下电"""
    call_arm_service("left_stop")
def left_reset_arm():
    """3. 复位 (Init)"""
    call_arm_service("left_init")

def left_open_gripper():
    """4. 打开夹爪 (Open)"""
    call_arm_service("left_open")
def left_close_gripper():
    """5. 关闭夹爪 (Close)"""
    call_arm_service("left_close")

def left_start_remote_ctrl():
    """6. 开始遥操 (Moving: True)"""
    call_arm_service("left_move", {"moving": True})
def left_stop_remote_ctrl():
    """7. 结束遥操 (Moving: False)"""
    call_arm_service("left_move", {"moving": False})
def left_reset_joint():
    call_arm_service("left_reset_joint")



def right_start_arm_poweron():
    """1. 上电"""
    call_arm_service("right_start")

def right_reset_and_poweroff():
    """2. 复位并下电"""
    call_arm_service("right_stop")
def right_reset_arm():
    """3. 复位 (Init)"""
    call_arm_service("right_init")

def right_open_gripper():
    """4. 打开夹爪 (Open)"""
    call_arm_service("right_open")
def right_close_gripper():
    """5. 关闭夹爪 (Close)"""
    call_arm_service("right_close")

def right_start_remote_ctrl():
    """6. 开始遥操 (Moving: True)"""
    call_arm_service("right_move", {"moving": True})
def right_stop_remote_ctrl():
    """7. 结束遥操 (Moving: False)"""
    call_arm_service("right_move", {"moving": False})
def right_reset_joint():
    call_arm_service("right_reset_joint")

def toggle_teleop_pub() -> None:
    pose_data = {
        "left": {
            "position": {"x": 0.0, "y": 0.0, "z": 0.0},
            "quaternion": {"x": 0.0, "y": 0.0, "z": 0.0, "w": 1.0}
        },
        "right": {  
            "position": {"x": 0.0, "y": 0.0, "z": 0.0},
            "quaternion": {"x": 0.0, "y": 0.0, "z": 0.0, "w": 1.0}
        }
    }
    msg = {
        "data": json.dumps(pose_data)
    }
    publish(ARM_PUB_TOPIC, msg, "std_msgs/msg/String")


# ====================== 菜单系统 ======================
def main_menu() -> None:
    sections = [
        (
            "机械臂控制",
            [
                ("1", "左臂上电", left_start_arm_poweron),
                ("2", "左臂复位并下电", left_reset_and_poweroff),
                ("3", "左臂复位", left_reset_arm),
                ("4", "左臂打开夹爪", left_open_gripper),
                ("5", "左臂关闭夹爪", left_close_gripper),
                ("6", "左臂开始遥操", left_start_remote_ctrl),
                ("7", "左臂结束遥操", left_stop_remote_ctrl),
                ("8", "发布遥感数据", toggle_teleop_pub),
                ("9", "左臂复位限位", left_reset_joint),
                ("10", "右臂上电", right_start_arm_poweron),
                ("11", "右臂复位并下电", right_reset_and_poweroff),
                ("12", "右臂复位", right_reset_arm),
                ("13", "右臂打开夹爪", right_open_gripper),
                ("14", "右臂关闭夹爪", right_close_gripper),
                ("15", "右臂开始遥操", right_start_remote_ctrl),
                ("16", "右臂结束遥操", right_stop_remote_ctrl),
                ("17", "左臂复位限位", right_reset_joint),
            ],
        ),
    ]

    menu_lookup = {key: func for _, items in sections for key, _, func in items}

    while True:
        print("\n=== 🤖 机器人 WebSocket 控制菜单 ===")
        for title, items in sections:
            print(f"\n-- {title} --")
            for key, desc, _ in items:
                print(f"{key}. {desc}")
        print("0. 退出程序")

        choice = input("\n请选择功能编号:").strip()

        if choice == "0" or choice == "q":
            print("👋 已退出程序。")
            break
        if choice in menu_lookup:
            try:
                menu_lookup[choice]()
            except Exception as exc:  # pylint: disable=broad-except
                print(f"❌ 执行出错：{exc}")
        else:
            print("⚠️ 无效选择，请重新输入。")


# ====================== 程序入口 ======================
if __name__ == "__main__":
    main_menu()
