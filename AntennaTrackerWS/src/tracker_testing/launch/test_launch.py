import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():

    use_sim_time = LaunchConfiguration('use_sim_time', default='false')

    urdf_file_name = 'test.urdf.xml'
    urdf = os.path.join(
        get_package_share_directory('tracker_testing'),
        urdf_file_name)
    with open(urdf, 'r') as infp:
        robot_desc = infp.read()

    rviz_config_file = os.path.join(
        get_package_share_directory('tracker_testing'), 'rviz', 'test.rviz')

    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='Use simulation (Gazebo) clock if true'),
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{'use_sim_time': use_sim_time, 'robot_description': robot_desc}],
            arguments=[urdf]),
        Node(
            package='tracker_testing',
            executable='state_publisher',
            name='state_publisher',
            output='screen'),
        # Start RViz2 with the given config file
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            output='screen',
            arguments=['-d', rviz_config_file],
            ),
    ])