import os
import platform
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, SetEnvironmentVariable
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    # choose default conda prefix based on CPU architecture
    arch = platform.machine().lower()
    if 'aarch64' in arch or arch.startswith('arm'):
        default_prefix = '/home/aidlux/miniforge3/envs/pinoc'
    else:
        default_prefix = '/home/ros2/miniconda3/envs/pino'

    default_conda_prefix = os.environ.get('CONDA_PREFIX', default_prefix)

    conda_python_bin = os.path.join(default_conda_prefix, 'bin/python3')
    
    conda_site_packages = os.path.join(default_conda_prefix, 'lib/python3.10/site-packages')
    conda_lib = os.path.join(default_conda_prefix, 'lib')

    pkg_share = get_package_share_directory('hair_arm_control')
    config_file = os.path.join(pkg_share, 'config', 'pico_servo_config.yaml')

    node = Node(
        package='hair_arm_control',
        executable='fisheye_arm_node',
        name='fisheye_arm_node',
        output='screen',
        prefix=[conda_python_bin, ' -u'],
        parameters=[
            config_file,
        ],
        emulate_tty=True
    )
    return LaunchDescription([
        SetEnvironmentVariable(
            name='PYTHONPATH',
            value=[conda_site_packages, ':', os.environ.get('PYTHONPATH', '')]
        ),
        SetEnvironmentVariable(
            name='LD_LIBRARY_PATH',
            value=[conda_lib, ':', os.environ.get('LD_LIBRARY_PATH', '')]
        ),
        node,
    ])

