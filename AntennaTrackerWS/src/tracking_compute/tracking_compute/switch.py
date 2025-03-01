from rclpy.node import Node
from std_msgs.msg import Bool

class Switch:
    def __init__(self, node: Node):
        self.node = node
        self.node.get_logger().info("Switch initialized within TrackingComputeNode")

        self.yawSwitch = False
        self.pitchSwitch = False

        # Create 2 subscriptions for yaw & pitch switches
        self.node.create_subscription(Bool, '/switch/yaw', self.yaw_switch_callback, 10)
        self.node.create_subscription(Bool, '/switch/pitch', self.pitch_switch_callback, 10)

    # Switch Callback
    def yaw_switch_callback(self, msg: Bool):
        self.yawSwitch = msg.data
        self.node.get_logger().info(f'Yaw switch {self.yawSwitch}')

    def pitch_switch_callback(self, msg: Bool):
        self.pitchSwitch = msg.data
        self.node.get_logger().info(f'Pitch switch {self.pitchSwitch}')
    
    # Getters
    def getYawSwitch(self):
        return self.yawSwitch

    def getPitchSwitch(self):
        return self.pitchSwitch