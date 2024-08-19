#TestAntenna will move both motors 180 degrees CCW, 180 degrees CCW, 90 degrees CCW, and 90 degrees CW
#
#
#


import csv
from Rocket import Rocket
from Antenna import Antenna
from Phidget22.Phidget import *
from Phidget22.Devices.Stepper import *
import math
import time
from geographiclib.geodesic import Geodesic
import csv
import threading
import SharedStack
import socket

class TestAntenna:
    def __init__(self, latitude, longitude, altitude):
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude

         try : #Attempting to connect the pitch and yaw motors to their drivers
            self.stepperPitch = Stepper() 
            self.stepperYaw = Stepper()                                             #INC AN ACCELERATION AND VELOCITY LIMIT. FOR SAFETY
            
            self.stepperPitch.openWaitForAttachment(5000) #mili sec
            self.stepperYaw.openWaitForAttachment(5000)
            
            self.stepperPitch.setEngaged(True)
            self.stepperYaw.setEngaged(True)
        except :
            raise Exception("Steppers failed to engaged")



        #rocket.move_tracker(pitchAngle, yawAngle)
    rocket.move_tracker(90, 90)
    rocket.move_tracker(-90,-90)
    #rocket.move_tracker(180,180)
    #rocket.move_tracker(-180,-180)
        

    rocket.kill_tracker()

    # # Getter for Latitude
    # @property
    # def latitude(self):
    #     return self._latitude

    # # Setter for Latitude
    # @latitude.setter
    # def latitude(self, value):
    #     self._latitude = value

    # # Getter for Longitude
    # @property
    # def longitude(self):
    #     return self._longitude

    # # Setter for Longitude
    # @longitude.setter
    # def longitude(self, value):
    #     self._longitude = value
        
    # # Getter for Altitude
    # @property
    # def altitude(self):
    #     return self._altitude

    # # Setter for Altitude
    # @altitude.setter
    # def altitude(self, value):
    #     self._altitude = value


