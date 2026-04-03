import os
import platform  # 修复：缺失的导入
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory, PackageNotFoundError


def generate_launch_description():
    # 1. 判断架构，设置conda环境路径
    arch = platform.machine().lower()
    if 'aarch64' in arch or arch.startswith('arm'):
        default_prefix = '/home/aidlux/miniforge3/envs/pinoc'
    else:
        default_prefix = '/home/ros2/miniconda3/envs/pino'

    # 获取conda环境路径（优先环境变量，否则用默认）
    default_conda_prefix = os.environ.get('CONDA_PREFIX', default_prefix)

    # conda 路径
    conda_python_bin = os.path.join(default_conda_prefix, 'bin/python3')
    conda_site_packages = os.path.join(default_conda_prefix, 'lib/python3.10/site-packages')
    conda_lib = os.path.join(default_conda_prefix, 'lib')

    # 2. 获取包路径与配置文件
    try:
        pkg_share = get_package_share_directory('hair_arm_control')
    except PackageNotFoundError:
        raise RuntimeError("Package 'hair_arm_control' not found")

    config_file = os.path.join(pkg_share, 'config', 'servo_control.yaml')

    # 3. 启动 servo 控制节点（修复prefix语法）
    servo_node = Node(
        package='hair_arm_control',
        executable='servo_control_node',
        name='servo_control_node',
        output='screen',
        prefix=f'{conda_python_bin} -u',  # 修复：必须是字符串，不是列表
        parameters=[config_file],
        emulate_tty=True
    )

    # 4. 尝试加载 rosbridge launch
    rosbridge_launch = None
    try:
        rosbridge_launch_path = os.path.join(
            pkg_share, 'launch', 'rosbridge_websocket_launch.py'
        )
        if os.path.exists(rosbridge_launch_path):
            rosbridge_launch = IncludeLaunchDescription(
                PythonLaunchDescriptionSource(rosbridge_launch_path)
            )
    except Exception as e:
        print(f"Warning: Failed to load rosbridge launch: {str(e)}")

    # 5. 构建环境变量（修复：必须用字符串拼接）
    python_path = f"{conda_site_packages}:{os.environ.get('PYTHONPATH', '')}"
    ld_library_path = f"{conda_lib}:{os.environ.get('LD_LIBRARY_PATH', '')}"

    # 6. 组装启动项
    launch_items = [
        SetEnvironmentVariable(name='PYTHONPATH', value=python_path),
        SetEnvironmentVariable(name='LD_LIBRARY_PATH', value=ld_library_path),
        servo_node,
    ]

    # 如果有rosbridge则加入
    if rosbridge_launch:
        launch_items.append(rosbridge_launch)

    return LaunchDescription(launch_items)