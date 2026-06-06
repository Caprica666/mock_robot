from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():
    pkg_share = get_package_share_directory('mock_bringup')
    teleop_config = os.path.join(pkg_share, 'config', 'teleop.yaml')


    return LaunchDescription([
        Node(
            package='joy',
            executable='joy_node',
            name='game_controller_node',
        ),

        Node(
            package='teleop_twist_joy',
            executable='teleop_node',
            name='teleop_twist_joy_node',
            parameters=[teleop_config]
        )
    ])

