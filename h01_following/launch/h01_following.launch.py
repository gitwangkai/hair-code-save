#!/usr/bin/env python3
"""
launch/h01_following.launch.py
ROS 2 一键启动文件
启动相机、雷达、人体跟随主节点
"""

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, ExecuteProcess
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.conditions import IfCondition


def generate_launch_description():
    """生成启动描述"""
    
    # 声明启动参数
    declare_use_sim_time = DeclareLaunchArgument(
        "use_sim_time",
        default_value="false",
        description="使用仿真时间"
    )
    
    declare_use_rviz = DeclareLaunchArgument(
        "use_rviz",
        default_value="false",
        description="启动 RViz"
    )
    
    declare_use_camera = DeclareLaunchArgument(
        "use_camera",
        default_value="true",
        description="启动 RGBD 相机"
    )
    
    declare_use_lidar = DeclareLaunchArgument(
        "use_lidar",
        default_value="true",
        description="启动激光雷达"
    )
    
    # 配置参数
    use_sim_time = LaunchConfiguration("use_sim_time")
    use_rviz = LaunchConfiguration("use_rviz")
    use_camera = LaunchConfiguration("use_camera")
    use_lidar = LaunchConfiguration("use_lidar")
    
    # 节点列表
    nodes = []
    
    # 1. Realsense 相机驱动
    # 注意: 需要安装 ros-humble-realsense2-camera
    # camera_launch = IncludeLaunchDescription(
    #     PythonLaunchDescriptionSource([
    #         PathJoinSubstitution([
    #             FindPackageShare("realsense2_camera"),
    #             "launch",
    #             "rs_launch.py"
    #         ])
    #     ]),
    #     launch_arguments={
    #         "depth_module.profile": "640x480x30",
    #         "rgb_camera.profile": "640x480x30",
    #         "align_depth.enable": "true",
    #     }.items(),
    #     condition=IfCondition(use_camera)
    # )
    # nodes.append(camera_launch)
    
    # 2. YDLIDAR 驱动
    # 注意: 需要安装 ydlidar_ros2_driver
    # lidar_launch = IncludeLaunchDescription(
    #     PythonLaunchDescriptionSource([
    #         PathJoinSubstitution([
    #             FindPackageShare("ydlidar_ros2_driver"),
    #             "launch",
    #             "ydlidar_launch.py"
    #         ])
    #     ]),
    #     condition=IfCondition(use_lidar)
    # )
    # nodes.append(lidar_launch)
    
    # 3. 人体跟随主节点（Python 进程）
    # 由于主程序使用 asyncio，通过 ExecuteProcess 启动
    following_node = ExecuteProcess(
        cmd=["python3", "-m", "h01_following.main"],
        cwd="/home/aidlux/h01_following",
        output="screen"
    )
    nodes.append(following_node)
    
    # 4. RViz2（可选）
    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        arguments=["-d", PathJoinSubstitution([
            FindPackageShare("h01_following"),
            "rviz",
            "following.rviz"
        ])],
        condition=IfCondition(use_rviz),
        parameters=[{"use_sim_time": use_sim_time}]
    )
    nodes.append(rviz_node)
    
    # 5. 静态 TF 发布（相机到基座）
    static_tf_camera = Node(
        package="tf2_ros",
        executable="static_transform_publisher",
        name="camera_tf",
        arguments=[
            "0.2",    # x
            "0.0",    # y
            "0.5",    # z
            "0.0",    # roll
            "0.0",    # pitch
            "0.0",    # yaw
            "base_link",
            "camera_color_optical_frame"
        ]
    )
    nodes.append(static_tf_camera)
    
    # 6. 静态 TF 发布（雷达到基座）
    static_tf_lidar = Node(
        package="tf2_ros",
        executable="static_transform_publisher",
        name="lidar_tf",
        arguments=[
            "0.1",    # x
            "0.0",    # y
            "0.3",    # z
            "0.0",    # roll
            "0.0",    # pitch
            "0.0",    # yaw
            "base_link",
            "laser_frame"
        ]
    )
    nodes.append(static_tf_lidar)
    
    return LaunchDescription([
        declare_use_sim_time,
        declare_use_rviz,
        declare_use_camera,
        declare_use_lidar,
        *nodes
    ])


# 独立运行测试
if __name__ == "__main__":
    from launch import LaunchService
    import sys
    
    ls = LaunchService(argv=sys.argv)
    ls.include_launch_description(generate_launch_description())
    sys.exit(ls.run())
