from rclpy.node import Node
from sensor_msgs.msg import NavSatFix

 # MAVROS Node for Rocket location
# /mavros/global_position/global
# Provided as a sensor_msgs/NavSatFix.msg
# http://docs.ros.org/en/noetic/api/sensor_msgs/html/msg/NavSatFix.html
# fix value
# float64 latitude
# float64 longitude
# float64 altitude

class Rocket:
    def __init__(self, node: Node, latitude, longitude, altitude):
        self.node = node
        self.node.get_logger().info("Rocket initialized within TrackingComputeNode")

        # Should I include a time variable?
        self._latitude = latitude
        self._longitude = longitude
        self._altitude = altitude

        self.node.create_subscription(NavSatFix, '/mavros/global_position/global', self.rocket_location_callback, 10)

    # Rocket Location Callback
    def rocket_location_callback(self, msg: NavSatFix):
        self._latitude = msg.latitude
        self._longitude = msg.longitude
        self._altitude = msg.altitude

        self.get_logger().info(f'Rocket Location: Latitude: {self._latitude}, Longitude: {self._longitude}, Altitude: {self._altitude} meters')

        if self._latitude == 0.0 and self._longitude == 0.0:
            self.get_logger().warn('Invalid location data received (latitude and longitude are zero).')


    # Get all values
    def getValues(self):
        return self._latitude, self._longitude, self._altitude
    
    # Getter and Setter for latitude
    def getLatitude(self):
        return self._latitude

    def setLatitude(self, latitude):
        self._latitude = latitude

    # Getter and Setter for longitude
    def getLongitude(self):
        return self._longitude

    def setLongitude(self, longitude):
        self._longitude = longitude

    # Getter and Setter for altitude
    def getAltitude(self):
        return self._altitude

    def setAltitude(self, altitude):
        self._altitude = altitude