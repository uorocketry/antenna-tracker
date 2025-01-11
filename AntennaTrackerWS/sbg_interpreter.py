# shebang (check)
#!/usr/bin/env python3
# when program is stopped (automatic tracking) keep this runnning
# pitch and yaw speed
# limiting maximum speed in the software si going directly above/kind of
# do an analysis/simulation when testing?

#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import Imu
import math

class GroundAntennaTracker:
    def __init__(self):
        rospy.init_node('ground_antenna_tracker', anonymous=True)
        
        # tracking state variables
        self.current_orientation = None
        self.current_angular_velocity = None
        self.current_linear_acceleration = None
        # if rocket is right above ground station
        self.rocket_above_threshold = 85.0  # zenith path threshold (degrees) 

        # ROS subscriber
        rospy.Subscriber("/sbg/imu_data", Imu, self.imu_callback)
        
        # ROS publisher
        self.control_pub = rospy.Publisher('/antenna/control', Imu, queue_size=10)
        
    def imu_callback(self, data):
    	# callback to IMU data
        self.current_orientation = data.orientation
        self.current_angular_velocity = data.angular_velocity
        self.current_linear_acceleration = data.linear_acceleration

        # convert to roll, pitch, yaw
        pitch_angle, yaw_angle = self.quaternion_to_euler(self.current_orientation)
        
        # log the data
        rospy.loginfo("Orientation (Pitch, Yaw): [%.2f, %.2f]", pitch_angle, yaw_angle)

        # if the rocket is directly above the ground station and still autonomous
        if self.is_rocket_above(pitch_angle):
            rospy.logwarn("rocket surpassed zenith path threshold.")
            self.handle_zenith_pass()
        else:
            rospy.loginfo("normal tracking")
            self.track_rocket(pitch_angle, yaw_angle)

    def is_rocket_above(self, pitch_angle):
        # check rocket position (zenith)
        return pitch_angle >= self.rocket_above_threshold

    def handle_zenith_pass(self):
 		# adjust tracking during direct overhead movement
        rospy.loginfo("adjusting tracking") # assume that the counterweight YAGI antenna option (manual) is going to be employed

    def track_rocket(self, pitch_angle, yaw_angle):
        rospy.loginfo("adjusting antenna to pitch: %.2f, yaw: %.2f", pitch_angle, yaw_angle)
        self.control_pub.publish(Imu())

    def quaternion_to_euler(self, orientation):
        x, y, z, w = orientation.x, orientation.y, orientation.z, orientation.w

        sinp = 2 * (w * y - z * x)
        pitch = math.degrees(math.asin(sinp)) if abs(sinp) <= 1 else 90 * math.copysign(1, sinp)

        siny_cosp = 2 * (w * z + x * y)
        cosy_cosp = 1 - 2 * (y**2 + z**2)
        yaw = math.degrees(math.atan2(siny_cosp, cosy_cosp))

        return pitch, yaw

    def run(self):
        # run ROS node
        rospy.spin()

if __name__ == '__main__':
    try:
        tracker = GroundAntennaTracker()
        tracker.run()
    except rospy.ROSInterruptException:
        rospy.loginfo("ground antenna tracker node terminated.")