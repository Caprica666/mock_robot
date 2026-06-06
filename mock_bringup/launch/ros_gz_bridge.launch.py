#!/usr/bin/env python3
import os

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.substitutions import PathJoinSubstitution, Command
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
from launch.substitutions.launch_configuration import LaunchConfiguration

ARGUMENTS = [
    DeclareLaunchArgument('use_sim_time', default_value='true',
                          choices=['true', 'false'],
                          description='Use sim time'),
    DeclareLaunchArgument('robot_name', default_value='create_2',
                          description='Gazebo model name'),
    DeclareLaunchArgument('world', default_value='depot',
                          description='World name')
]

def generate_launch_description():

    pkg_ros_gz_sim = get_package_share_directory('ros_gz_sim')
    use_sim_time = LaunchConfiguration('use_sim_time')
    robot_name = LaunchConfiguration('robot_name')
    world = LaunchConfiguration('world')


    # cmd_vel_bridge
    cmd_vel_bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        name='cmd_vel_bridge',
        output='screen',
        parameters=[{
            'use_sim_time': use_sim_time
        }],
        arguments=[
        #'/cmd_vel@geometry_msgs/msg/TwistStamped]gz.msgs.Twist',
        '/cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist',
        '/odom@nav_msgs/msg/Odometry[gz.msgs.Odometry',
        '/tf@tf2_msgs/msg/TFMessage[gz.msgs.Pose_V'
        ],
     )


    # Pose bridge
    pose_bridge = Node(package='ros_gz_bridge', executable='parameter_bridge',
                       name='pose_bridge',
                       output='screen',
                       parameters=[{
                            'use_sim_time': use_sim_time
                       }],
                       arguments=[
                           ['/model/', robot_name, '/pose' +
                            '@tf2_msgs/msg/TFMessage' +
                            '[gz.msgs.Pose_V'],
                       ],
                       remappings=[
                           (['/model/', robot_name, '/pose'],
                            '_internal/sim_ground_truth_pose'),
                       ])

    # IMU
    imu_bridge = Node(package='ros_gz_bridge', executable='parameter_bridge',
                       name='imu_bridge',
                       output='screen',
                       parameters=[{
                            'use_sim_time': use_sim_time
                       }],
                       arguments=[
                           ['/model/', robot_name,
                            '/link/imu@sensor_msgs/msg/Imu@gz.msgs.IMU' ],
                       ])

    # odom to base_link transform bridge
    odom_base_tf_bridge = Node(package='ros_gz_bridge', executable='parameter_bridge',
                               name='odom_base_tf_bridge',
                               output='screen',
                               parameters=[{
                                   'use_sim_time': use_sim_time
                               }],
                               arguments=[
                                   ['/model/', robot_name, '/tf' +
                                    '@tf2_msgs/msg/TFMessage' +
                                    '[gz.msgs.Pose_V']
                               ],
                               remappings=[
                                   (['/model/', robot_name, '/tf'], 'tf' )
                               ])

    ld = LaunchDescription(ARGUMENTS)
    ld.add_action(cmd_vel_bridge)
    #ld.add_action(pose_bridge)
    #ld.add_action(odom_base_tf_bridge)
    return ld
