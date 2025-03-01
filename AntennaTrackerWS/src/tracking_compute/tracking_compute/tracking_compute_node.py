#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from std_msgs.msg import Float64, String, Bool
from .yawmotor import yawMotor
from .antenna import Antenna
from .rocket import Rocket
from .switch import Switch
import time
import math

class trackingComputeNode(Node):

    def __init__(self):
        super().__init__("tracker_compute")
        self.get_logger().info("ROS2 Tracking Compute Node Initialized")

        # Initialize Antenna & Rocket object
        self.antenna = Antenna(47.98714, -81.84864, 62.52301, False, "IDLE") #STEM coordinates
        self.rocket = Rocket(self, 47.98714, -81.84864, 362.52301) #STEM coordinates, but higher altitude than antenna

        # TO BE DONE --> Include actual coordinates of antenna using its respective node (SBG Node)

        # Switch Status
        self.switch = Switch(self)

        # Initialize motors
        self.yawMotor = yawMotor(self)
        # self.pitchMotor = pitchMotor() # possible stepper board change means I'm waiting for this

        # This function is just for testing temporarily
        self.testing()

        # self.run()

    def calc_yaw(self):
        x = math.radians(self.antenna.latitude - self.latitude)
        y = math.radians(self.antenna.longitude - self.longitude)

        yawRad = math.atan2(y, x)
        yawDeg = math.degrees(yawRad)

        return yawDeg
    
    # def calc_pitch(self):
    #     altdiff = self.altitude - self.antenna.altitude
    #     dist = Geodesic.WGS84.Inverse(self.antenna.latitude, self.antenna.longitude, self.latitude, self.longitude)
    #     pitchRad = math.atan2(altdiff, dist['s12'])
    #     pitchDeg = math.degrees(pitchRad)
    #     return pitchDeg

    def calibrate(self):
        self.get_logger().info("Calibrating the Antenna")

        # 2 steps
        # Yaw Calibration
        count = self.count_publishers('/Switch/Yaw')
        if count > 0:
            self.get_logger().info(f"Publisher '/Switch/Yaw' is available.")

        while (self.switch.getYawSwitch() == False):
            self.yawMotor.move(-0.1) # move -0.1 degrees

        # Assume we hit switch and set as position 0deg
        # Important to assume that 0deg is pointing to true north. (must be met when setting up antenna tracker)
        # A magnetometer could be nice in the future
        self.yawMotor.position_offset()

        # # Pitch Calibration
        # count = self.count_publishers('/Switch/Pitch')
        # if count > 0:
        #     self.get_logger().info(f"Publisher '/Switch/Pitch' is available.")

        # while (self.switch.getPitchSwitch() == False):
        #     self.pitchMotor.move(-0.1) # move -0.1 degrees

        # # Assume we hit switch and set as position 0deg
        # # Important to assume that 0deg is pointing to the lowest pitch on the antenna. (if the antenna is not on flat ground this wont work)
        # # An IMU could be nice in the future for this
        # self.pitchMotor.position_offset()


    # For testing purposes
    def testing(self):
        self.get_logger().info("Waiting 10 seconds to start test")
        time.sleep(10) # wait 5 seconds to start
        self.get_logger().info("Testing started")
        self.yawMotor.toggle_engagement(True) # set engaged on
        self.yawMotor.position_offset() # set position to 0
        self.yawMotor.move(30.0) # move 30 degrees
        return
    
    # Basic Run loop
    # def run():
    #     while True:

    #     return


def main(args=None):
    rclpy.init(args=args) 
    node = trackingComputeNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        rclpy.shutdown()

if __name__ == '__main__':
    main()