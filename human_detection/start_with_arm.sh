#!/bin/bash
# 智能迎宾机器人 - 带机械臂启动脚本

echo "========================================"
echo "智能迎宾机器人 - 机械臂控制版"
echo "========================================"

# 检查 Python 环境
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到 python3"
    exit 1
fi

# 显示菜单
echo ""
echo "请选择运行模式:"
echo "  1) 主程序 (GUI模式)"
echo "  2) Web GUI (浏览器控制)"
echo "  3) 机械臂测试"
echo "  4) 模拟模式 (无需机械臂)"
echo "  5) 挥手联动测试"
echo "  6) 退出"
echo ""

read -p "选择 [1-5]: " choice

case $choice in
    1)
        echo ""
        echo "启动主程序..."
        echo "按 Ctrl+C 退出"
        echo ""
        python3 main.py
        ;;
    2)
        echo ""
        echo "启动 Web GUI 服务器..."
        echo "请在浏览器中打开显示的地址"
        echo ""
        python3 web_gui.py
        ;;
    3)
        echo ""
        echo "机械臂测试菜单:"
        echo "  1) 完整测试"
        echo "  2) 连接测试"
        echo "  3) 关节运动测试"
        echo "  4) 夹爪测试"
        echo "  5) 动作测试"
        echo ""
        read -p "选择测试项目 [1-5]: " test_choice
        
        case $test_choice in
            1) python3 test_arm.py ;;
            2) python3 test_arm.py --test connection ;;
            3) python3 test_arm.py --test movement ;;
            4) python3 test_arm.py --test gripper ;;
            5) python3 test_arm.py --test action ;;
            *) python3 test_arm.py ;;
        esac
        ;;
    4)
        echo ""
        echo "启动模拟模式 (无需真实机械臂)..."
        echo ""
        read -p "选择运行方式 [1=主程序, 2=Web GUI]: " mock_choice
        
        if [ "$mock_choice" = "1" ]; then
            python3 main.py --mock-arm
        else
            # Web GUI 需要在配置中设置 mock_arm
            echo "请在 web_gui.py 的 config 中设置 'mock_arm': True"
            echo "或者手动修改配置"
        fi
        ;;
    5)
        echo ""
        echo "挥手联动测试菜单:"
        echo "  1) 间隔控制测试"
        echo "  2) 模拟联动测试"
        echo "  3) Web GUI 测试模式"
        echo ""
        read -p "选择测试项目 [1-3]: " wave_choice
        
        case $wave_choice in
            1) python3 test_wave_integration.py ;;
            2) python3 test_wave_integration.py ;;  # 集成测试包含联动测试
            3) 
                echo "启动 Web GUI 模拟模式..."
                # 修改配置使用模拟模式
                python3 -c "
import sys
sys.path.insert(0, 'src')
from wave_action import MockWaveActionController
ctrl = MockWaveActionController(min_interval=10)
print('挥手动作控制器测试:')
print(f'  间隔: {ctrl.get_interval()}秒')
ctrl.trigger()
"
                ;;
            *) python3 test_wave_integration.py ;;
        esac
        ;;
    6)
        echo "退出"
        exit 0
        ;;
    *)
        echo "无效选择"
        exit 1
        ;;
esac
