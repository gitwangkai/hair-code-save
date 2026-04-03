from PallasSDK import Controller
from PallasSDK import Location, LocationJ
import time

# 脚本程序入口
if __name__ == "__main__":
    ctrl_ip = "192.168.3.100"
   
    ctrl = Controller()
    try:
        # 输出 SDK 版本号表示 SDK 调用成功
        print(f"SDK Version: {ctrl.GetSDKVersion()}")
        
        # 连接控制器并配置参数
        ctrl.Connect(ctrl_ip)
        print(f"已连接到控制器 {ctrl_ip},开始上电")
        ctrl.SetPowerEnable(True)
        time.sleep(1)
        print("控制器已上电,准备开始下电")
        ctrl.SetPowerEnable(False)
        # 添加控制的机器人（机器人编号1）
        robot = ctrl.AddRobot(1)
        print("机器人已添加,开始读取编码器值并写入控制器IDN参数")
        #===================主要代码=======================#
        for ii in range(1,8):
            if ii == 1:
                value = 0
            else:
                # 读编码器的值
                value = robot.GetEncoder(ii)
                # 校验：确保 value 在 [-32767, 32767] 范围内
                while value > 32767:
                    value -= 65535
                while value < -32767:
                    value += 65535
            print(f"轴{ii} 编码器值: {value}")
            # 写入 IDN
            ctrl.IDNWrite("1127.13","1.0.0",f"{ii},{value}")
        
        # 应用
        ctrl.IDNWrite("1127.14","1.0.0","2")
        # 保存 - 确保下次重启生效
        ctrl.IDNWrite("21.23","1.0.0","save")
        
        
    except Exception as e:
        print(f"程序执行出错：{str(e)}")
    finally:
        # 确保断开连接，释放资源
        if 'ctrl' in locals() and ctrl.IsConnected():
            ctrl.Disconnect()
            print("已断开控制器连接")