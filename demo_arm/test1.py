import time
import os
from PallasSDK import Controller, HiddenDataType, ComPort
from PallasSDK import LocationJ

# 保存当前关节
joint_pos = [0,0,0,0,0,0]

def hidden_callback(type, robot, data):
    global joint_pos

    if type == HiddenDataType.RobotJointPos:
        joint_pos = [float(i) for i in data[:6]]


def clear():
    os.system("clear")


def draw_ui():
    clear()

    print("====== Pallas Robot Controller ======")
    print("")
    print("当前关节角度:")
    print("")
    print(f"J1: {joint_pos[0]:.2f}")
    print(f"J2: {joint_pos[1]:.2f}")
    print(f"J3: {joint_pos[2]:.2f}")
    print(f"J4: {joint_pos[3]:.2f}")
    print(f"J5: {joint_pos[4]:.2f}")
    print(f"J6: {joint_pos[5]:.2f}")
    print("")
    print("控制:")
    print("输入6个角度 -> 运动")
    print("g -> 抓取")
    print("o -> 张开")
    print("q -> 退出")
    print("====================================")


def main():

    ctrl = Controller()

    ctrl.SetHiddenCallback(hidden_callback)

    print("连接机械臂...")

    ctrl.Connect("192.168.3.100")

    print("连接成功")

    ctrl.SetHiddenOn(HiddenDataType.RobotJointPos)

    serial_name = "COM2"

    try:
        ctrl.ComOpen(serial_name,ComPort.Com_485,115200,8,1,0,True)
    except:
        print("机械手未连接")

    ctrl.SetPowerEnable(True)

    robot = ctrl.AddRobot(1)

    robot.SetFrameType(1)
    robot.SetSpeed(10)

    while True:

        draw_ui()

        cmd = input("输入指令: ")

        if cmd == "q":
            break

        if cmd == "g":
            try:
                ctrl.ComSend(serial_name,"55AA011409014C044C044C04840332003200320032006400C2")
            except:
                pass
            continue

        if cmd == "o":
            try:
                ctrl.ComSend(serial_name,"55AA011409011400140014008403320032003200320064000E")
            except:
                pass
            continue

        try:

            arr = cmd.split()
            angles = [float(i) for i in arr]

            while len(angles) < 6:
                angles.append(0)

            angles = angles[:6]

            robot.MoveJ(LocationJ(*angles))

        except:
            pass

        time.sleep(0.5)

    ctrl.SetPowerEnable(False)

    try:
        ctrl.ComClose(serial_name)
    except:
        pass


if __name__ == "__main__":
    main()