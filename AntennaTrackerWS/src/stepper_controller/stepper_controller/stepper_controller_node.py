#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64, String, Bool

from .stepper_services import setup_services
from .stepper_actions import setup_actions, mttpa_execute_callback, mttpa_goal_callback, mttpa_cancel_callback

import time
from Phidget22.Phidget import *
from Phidget22.Devices.Stepper import *


class stepperControllerNode(Node):

    def __init__(self):
        super().__init__("stepper_controller")
        self.get_logger().info("ROS2 Stepper Controller Node Initialized")

        # Publishers
        self.error_pub = self.create_publisher(String, '/stepper_controller/error', 10)
        self.position_pub = self.create_publisher(Float64, '/stepper_controller/position', 10)
        self.is_moving_pub = self.create_publisher(Bool, '/stepper_controller/is_moving', 10)
        self.is_attached_pub = self.create_publisher(Bool, '/stepper_controller/is_attached', 10)
        self.get_logger().info("Created publishers")
        
        setup_services(self) # runs all services
        self.get_logger().info("Created services")
        self.mttpa_execute_callback = mttpa_execute_callback
        self.mttpa_goal_callback = mttpa_goal_callback
        self.mttpa_cancel_callback = mttpa_cancel_callback
        self.get_logger().info("Linked action callbacks")
        setup_actions(self) # runs all actions
        self.get_logger().info("Created actions")

        self.get_logger().info("Creating stepper controller, if it takes a while, check the connection")
        self.stepper = stepperController(logger=self.get_logger(), serialNumber=1, stepAngle=1.8, acceleration=100, velocityLimit=1000, currentLimit=1)
        self.get_logger().info("Created stepper controller")

    # Called when the node is shutting down
    def on_shutdown(self):
        self.stepper.close()

        
class stepperController(Stepper):

    def __init__(self, logger, serialNumber, stepAngle, acceleration, velocityLimit, currentLimit):
        super().__init__()

        # ROS logger
        self.logger = logger

        # We lose some torque with microstepping, but it's locked in by phidget. @ 1/16
        self.stepAngle = stepAngle
        self.stepsPerRevolution = (360 / self.stepAngle) * 16  # Microsteps per revolution
        self.stepsPerDegree = 16 / self.stepAngle # Microsteps per Degree

        self.serialNumber = serialNumber
        #self.setDeviceSerialNumber() # This is one way to chose the correct board. (Phidget makes a hub as another option) 
        
        while True:
            try:
                self.openWaitForAttachment(5000)
                break
            except PhidgetException as e:
                # failed but it will try again
                time.sleep(1)
                continue

        self.StepperControlMode(0x0) #CONTROL_MODE_STEP, should be set by default though
        self.setRescaleFactor(self.stepsPerDegree) # This should allow us to use normal degree's for our functions

        # Attach event handlers
        self.setOnAttachHandler(self.onAttach)
        self.setOnDetachHandler(self.onDetach)
        self.setOnPositionChangeHandler(self.onPositionChange)
        self.setOnStoppedHandler(self.onStopped)

        # Set Phidget-specific parameters (these must be set)
        self.setAcceleration(acceleration)
        self.setVelocityLimit(velocityLimit)
        self.setCurrentLimit(currentLimit)
        

    # Event handler for when the stepper is attached
    def onAttach(self, self_instance):
        msg = Bool()
        msg.data = True
        self.is_attached_pub(msg)

    # Event handler for when the stepper is detached
    def onDetach(self, self_instance):
        msg = Bool()
        msg.data = True
        self.is_attached_pub(msg)

    def onPositionChange(self, position):
        msg = Bool()
        msg.data = True
        self.is_moving_pub(msg)

        msg2 = Float64()
        msg2.data = position
        self.is_moving_pub(msg2)
    
    def onStopped(self):
        msg = Bool()
        msg.data = False
        self.is_moving_pub(msg)

    # Close the connection when done
    def close(self):
        self.stepper.close()


def main(args=None):
    rclpy.init(args=args) 
    node = stepperControllerNode()
    rclpy.spin(node)

    # Should theoretically never make it here
    node.stepper.close()
    rclpy.shutdown()

if __name__ == '__main__':
    main()