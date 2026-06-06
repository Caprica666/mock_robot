#!/usr/bin/env python3
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.substitutions import PathJoinSubstitution, LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.conditions import IfCondition


use_rviz_arg = DeclareLaunchArgument('use_rviz', default_value='false',
                choices=['true', 'false'],
                description='Start rviz' )

use_gazebo_arg = DeclareLaunchArgument('use_gazebo', default_value='true',
                choices=['true', 'false'],
                description='Start gazebo' )

#world_arg =  DeclareLaunchArgument('world', default_value='depot', description='Gazebo World' )
world_arg =  DeclareLaunchArgument('world', default_value='empty', description='Gazebo World' )

ARGUMENTS = [ use_gazebo_arg, use_rviz_arg, world_arg ]

for pose_element in ['x', 'y', 'z', 'yaw']:
    ARGUMENTS.append(DeclareLaunchArgument(pose_element, default_value='0.0',
                     description=f'{pose_element} component of the robot pose.'))

def generate_launch_description():
    pkg_bringup = get_package_share_directory('mock_bringup')


    # Paths
    gazebo_launch = PathJoinSubstitution(
        [pkg_bringup, 'launch', 'sim.launch.py'])
    robot_spawn_launch = PathJoinSubstitution(
        [pkg_bringup, 'launch', 'mockbot_spawn.launch.py'])

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([gazebo_launch]),
        condition=IfCondition(LaunchConfiguration('use_gazebo')),
        launch_arguments=[
            ('world', LaunchConfiguration('world'))
        ]
    )

    # Spawn robot
    robot_spawn = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([robot_spawn_launch]),
        launch_arguments=[
            ('use_rviz', LaunchConfiguration('use_rviz')),
            ('use_gazebo', LaunchConfiguration('use_gazebo')),
            ('x', LaunchConfiguration('x')),
            ('y', LaunchConfiguration('y')),
            ('z', LaunchConfiguration('z')),
            ('yaw', LaunchConfiguration('yaw'))])

    # Create launch description and add actions
    ld = LaunchDescription(ARGUMENTS)
    ld.add_action(gazebo)
    ld.add_action(robot_spawn)
    return ld
