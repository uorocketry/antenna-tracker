from math import pi, sin
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
from sensor_msgs.msg import JointState

class StateProvider(Node):

    def __init__(self):
        super().__init__('state_provider')
        
        # Initialize joint state publisher
        self.joint_pub = self.create_publisher(
            JointState,
            'joint_states',
            QoSProfile(depth=10))
        
        # Motion parameters
        self.base_rotation = 0.0  # Continuous rotation angle
        self.arm_elevation = 0.0  # Vertical pointing angle
        self.update_rate = 30  # Hz
        
        # Configure joint state message
        self.joint_state = JointState()
        self.joint_state.name = ['base_to_arm_plate', 'arm_plate_to_arm']
        
        # Start main loop
        self.start_motion()

    def start_motion(self):
        """Main control loop for antenna movement"""
        timer = self.create_timer(1/self.update_rate, self.update_state)
        
    def update_state(self):
        """Calculate new positions and publish joint states"""
        # Update base rotation (full 360° continuous)
        self.base_rotation = (self.base_rotation + 0.035) % (2 * pi)
        
        # Calculate arm elevation
        self.arm_elevation = 0
        
        # Prepare and publish message
        self.joint_state.header.stamp = self.get_clock().now().to_msg()
        self.joint_state.position = [self.base_rotation, self.arm_elevation]
        self.joint_pub.publish(self.joint_state)

def main():
    rclpy.init()
    provider = StateProvider()
    rclpy.spin(provider)
    rclpy.shutdown()

if __name__ == '__main__':
    main()