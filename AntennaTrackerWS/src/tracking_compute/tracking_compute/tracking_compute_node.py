#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from std_msgs.msg import Float64, String, Bool
from .yawmotor import yawMotor
from .antenna import Antenna
from .rocket import Rocket
import time

class trackingComputeNode(Node):

    def __init__(self):
        super().__init__("tracker_compute")
        self.get_logger().info("ROS2 Tracking Compute Node Initialized")

        # Initialize Antenna & Rocket object
        self.antenna = Antenna(47.98714, -81.84864, 62.52301, False, "IDLE") #STEM coordinates
        self.rocket = Rocket(47.98714, -81.84864, 362.52301) #STEM coordinates, but higher altitude than antenna

        # TO BE DONE --> Include actual coordinates of antenna and rocket using their respective nodes
        # SBG NODE for Antenna location
        # RFD 900 Node for Rocket location

        # Initialize motors
        self.yawmotor = yawMotor(self)
        # self.pitchmotor = pitchMotor() # possible stepper board change means I'm waiting for this

        # Future connection to ground station for coordinate prediction

        self.testing()

    # For testing purposes
    # Just noticed that we must send FLOAT VALUES (even though its Integer... whoops)
    def testing(self):
        self.get_logger().info("Waiting 10 seconds to start test")
        time.sleep(10) # wait 5 seconds to start
        self.get_logger().info("Testing started")
        self.yawmotor.toggle_engagement(True) # set engaged on
        self.yawmotor.position_offset() # set position to 0
        self.yawmotor.move(30.0) # move 30 degrees
        return


        
    # Called when the node is shutting down
    def on_shutdown(self):
        self.stepper.close()


def main(args=None):
    rclpy.init(args=args) 
    node = trackingComputeNode()
    rclpy.spin(node)

    # Should theoretically never make it here
    rclpy.shutdown()

if __name__ == '__main__':
    main()