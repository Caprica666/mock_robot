# Copyright 2021 Clearpath Robotics, Inc.
# @author Roni Kreinin (rkreinin@clearpathrobotics.com)

from ament_index_python.packages import get_package_share_directory


from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, GroupAction
from launch.actions import IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node, PushRosNamespace


ARGUMENTS = [
    DeclareLaunchArgument('bridge', default_value='true',
                          choices=['true', 'false'],
                          description='Use ros_gz_bridge'),
    DeclareLaunchArgument('world', default_value='depot',
                          description='Ignition World'),
    DeclareLaunchArgument('use_rviz', default_value='true',
                          choices=['true', 'false'], description='Start rviz.'),
]

for pose_element in ['x', 'y', 'z', 'yaw']:
    ARGUMENTS.append(DeclareLaunchArgument(pose_element, default_value='0.0',
                     description=f'{pose_element} component of the robot pose.'))


def generate_launch_description():

    # Directories
    pkg_bringup = get_package_share_directory('mock_bringup')
    pkg_description = get_package_share_directory('mock_description')

    # Paths
    ros_gz_bridge_launch = PathJoinSubstitution( [pkg_bringup, 'launch', 'mock_gz_bridge.launch.py'])
    rviz2_launch = PathJoinSubstitution([pkg_bringup, 'launch', 'rviz2.launch.py'])
    robot_description_launch = PathJoinSubstitution(
        [pkg_description, 'launch', 'mock_gz.launch.py'])

    # Launch configurations
    x, y, z = LaunchConfiguration('x'), LaunchConfiguration('y'), LaunchConfiguration('z')
    yaw = LaunchConfiguration('yaw')

    robot_name = 'mockbot'

    spawn_robot_group_action = GroupAction([
        # Robot description
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([robot_description_launch]),
        ),

        # Spawn Create 3
        Node(
            package='ros_gz_sim',
            executable='create',
            arguments=['-name', robot_name,
                       '-x', x,
                       '-y', y,
                       '-z', z,
                       '-Y', yaw,
                       '-topic', 'robot_description'],
            output='screen',
        ),

        # ROS GZ Bridge
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([ros_gz_bridge_launch]),
            launch_arguments=[
                ('world', LaunchConfiguration('world')),
                ('robot_name', robot_name),
            ]
        ),

        # Rviz
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([rviz2_launch]),
            condition=IfCondition(LaunchConfiguration('use_rviz')),
        )
    ])

    # Create launch description and add actions
    ld = LaunchDescription(ARGUMENTS)
    ld.add_action(spawn_robot_group_action)
    return ld
