import rospy
from std_msgs.msg import String
import RPi.GPIO as GPIO
import time

# GPIO pins 22 and 27 on the Pi
GPIO.setmode(GPIO.BCM)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # GPIO 22 as input with pull-down resistor
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # GPIO 27 as input with pull-down resistor

# initialize publisher
rospy.init_node('limit_switch_publisher', anonymous=True)
pub = rospy.Publisher('limit_switch_status', String, queue_size=10, tcp_nodelay=True)

# def channel as pin #
def limit_switch_callback(channel):
    if GPIO.input(channel):
        rospy.loginfo("GPIO {} triggered".format(channel))
        pub.publish("GPIO {} triggered".format(channel))
    else:
        rospy.loginfo("GPIO {} released".format(channel))
        pub.publish("GPIO {} released".format(channel))

# bouncetime set to 300 ms... change?
GPIO.add_event_detect(22, GPIO.BOTH, callback=limit_switch_callback, bouncetime=300)
GPIO.add_event_detect(27, GPIO.BOTH, callback=limit_switch_callback, bouncetime=300)


try:
    rospy.spin()
except KeyboardInterrupt:
    pass

GPIO.cleanup()
