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
        self.get_logger().info('Yaw switch triggered')
        self.yawSwitch = msg.data

    def pitch_switch_callback(self, msg: Bool):
        self.get_logger().info('Pitch switch triggered')
        self.pitchSwitch = msg.data
    
    # Getters
    def getYawSwitch(self):
        return self.yawSwitch

    def getPitchSwitch(self):
        return self.pitchSwitch