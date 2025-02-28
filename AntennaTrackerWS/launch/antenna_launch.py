from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess

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
            name='Compute',
        ),

        # Node(
        #     package='mavros',
        #     namespace='mavros',
        #     executable='mavros_node',
        #     name='MyMavROS',
        #     parameters=[{
        #         "fcu_url": "tcp://127.0.0.1:5656",
        #         "gcs_url": "",
        #         "uas_prefix": "/uas1",
        #         "target_system": 1,
        #         "target_component": 1
        #     }]
        # )
        # Not sure why, but Node doesn't seem to work...
        # Here is a workaround

        ExecuteProcess(
            cmd=["ros2", "run", "mavros", "mavros_node", "--ros-args", "-p", "fcu_url:=tcp://127.0.0.1:5656"],
            output="screen"
        ),
       
    ])