#!/usr/bin/env python3
import os

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.substitutions import PathJoinSubstitution, Command, FindExecutable
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
from launch.substitutions.launch_configuration import LaunchConfiguration
from launch_ros.parameter_descriptions import ParameterValue


ARGUMENTS = [
   DeclareLaunchArgument('visualize_rays', default_value='false',
                          choices=['true', 'false']) ]

def generate_launch_description():
    pkg_mock_description = get_package_share_directory('mock_description')
    visualize_rays = LaunchConfiguration('visualize_rays')

    # Correct URDF path

    xacro_file = os.path.join(pkg_mock_description, 'gazebo', 'mockbot_sim.urdf.xacro')

    urdf_file = Command([ PathJoinSubstitution([FindExecutable(name='xacro')]), ' ', xacro_file ])

    # Start robot state publisher
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[
            {'use_sim_time': True },
            {'robot_description': ParameterValue(
             Command( ['xacro', ' ', xacro_file]), value_type=str)
            },
        ],
        remappings=[
            ('/tf', 'tf'),
            ('/tf_static', 'tf_static')
        ]
    )

    joint_state_publisher = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
        output='screen',
        parameters=[{'use_sim_time': True}],
        remappings=[
            ('/tf', 'tf'),
            ('/tf_static', 'tf_static')
        ]
    )

    ld = LaunchDescription(ARGUMENTS)
    ld.add_action(joint_state_publisher)
    ld.add_action(robot_state_publisher)
    return ld
