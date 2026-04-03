import time

print("机械手控制 Demo 脚本")
# 引入 SDK
from PallasSDK import Controller, Robot, HiddenDataType, ComPort
from PallasSDK import Location, LocationJ
# 在这里监控机器人位置
def hidden_callback(type, robot, data):
    print(type, data)


def main():
    ctrl = None
    serial_port_open = False
    try:
        # 创建 实例
        ctrl = Controller()
        print("IsConnected", ctrl.IsConnected())
        # 添加数据监控
        ctrl.SetHiddenCallback(hidden_callback)
        # 连接
        # ctrl.Connect("192.168.1.100")
        ctrl.Connect("192.168.3.100")
        # 开启轴坐标反馈
        ctrl.SetHiddenOn(HiddenDataType.RobotJointPos)
        # 开启世界坐标反馈
        ctrl.SetHiddenOn(HiddenDataType.RobotCartesianPos)
        
        # 尝试打开串口
        try:
            # 创建一个串口 串口名称  串口类型485 波特率115200 数据位8 停止位1 校验位0 发送16进制     
            ctrl.ComOpen("com2", ComPort.Com_485, 115200, 8, 1, 0, True)
            serial_port_open = True
            print("串口 com2 打开成功")
        except Exception as e:
            print(f"警告: 串口打开失败: {e}")
            print("继续执行，跳过串口操作...")
        
        # 伺服上电
        ctrl.SetPowerEnable(True)
        # 获取 Robot 对象
        robot = ctrl.AddRobot(1)
        # 在轴坐标下运动 2 是世界坐标
        robot.SetFrameType(1)
        # 设置速度为 10%
        robot.SetSpeed(10) 
        
        # 在世界坐标运动指令 - 需要等运动学到位
        # 世界坐标
        # robot.SetFrameType(2)
        # 运动到 X = 10 , Y = 20 的位置 - 请根据实际位置修改
        # 对应 X,Y,Z,Yaw,Pitch,Roll
        # robot.MoveL(Location(10, 20, 0, 0, 0, 0))
        
        while True:
            try:
                aa = input("输入指令，输入1-6个整数控制机械臂:").split()
                if not aa:
                    continue
                bb = [int(i) for i in aa]
                ll = len(bb) - 6
                if ll > 0:
                    bb = bb[:6]
                elif ll < 0:
                    for i in range(abs(ll)):
                        bb.append(0)
                robot.MoveJ(LocationJ(bb[0], bb[1], bb[2], bb[3], bb[4], bb[5]))
            except ValueError:
                print("错误: 请输入有效的整数")
            except Exception as e:
                print(f"错误: {e}")
            
            # # 控制手运动
            # if serial_port_open:
            #     try:
            #         ctrl.ComSend("com2","55AA01140901140014001400F4063200320032003200640081")
            #         time.sleep(1)
            #         ctrl.ComSend("com2","55AA011409011400140014008403320032003200320064000E")
            #         time.sleep(1)
            #         ctrl.ComSend("com2","55AA011409014C044C044C04840332003200320032006400C2")
            #         time.sleep(1)
            #         ctrl.ComSend("com2","55AA011409011400140014008403320032003200320064000E")
            #         time.sleep(1)
            #     except Exception as e:
            #         print(f"警告: 串口发送失败: {e}")
            
            # time.sleep(0.1)
    except KeyboardInterrupt:
        print("\n程序被用户中断")
    except Exception as e:
        print(f"错误: {e}")
    finally:
        try:
            # 尝试关闭连接
            if ctrl:
                print("\n清理资源...")
                try:
                    ctrl.SetPowerEnable(False)
                    print("伺服已下电")
                except Exception as e:
                    print(f"警告: 伺服下电失败: {e}")
                
                if serial_port_open:
                    try:
                        ctrl.ComClose("com2")
                        print("串口 com2 已关闭")
                    except Exception as e:
                        print(f"警告: 串口关闭失败: {e}")
                
                print("清理完成")
        except Exception as e:
            print(f"清理错误: {e}")
            
if __name__ == '__main__':
    main()
