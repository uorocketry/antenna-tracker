from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='stepper_controller',
            namespace='stepper_controller',
            executable='stepper_controller',
            name='StepperController',
        ),
        Node(
            package='tracking_compute',
            namespace='tracking_compute',
            executable='tracking_compute',
            name='Compute'
        ),
    ])