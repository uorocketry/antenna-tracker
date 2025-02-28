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
from time import sleep
import asyncio
from queue import LifoQueue


#antenna = Antenna() #STEM
rocket = Rocket(47.986884, -81.848456, 362.52301) 
antenna = Antenna(47.98714, -81.84864, 62.52301, False, "IDLE") #STEM


# try : #Attempting to connect the pitch and yaw motors to their drivers
#     stepperPitch = Stepper() 
# #    stepperYaw = Stepper()                                             #INC AN ACCELERATION AND VELOCITY LIMIT. FOR SAFETY
            
#     stepperPitch.openWaitForAttachment(5000) #mili sec
# #    stepperYaw.openWaitForAttachment(5000)
            
#     stepperPitch.setEngaged(True)
# #    stepperYaw.setEngaged(True)
# except :
#         raise Exception("Steppers failed to engaged")



  #rocket.move_tracker(pitchAngle, yawAngle)

if __name__ == "__main__":


  antenna.stepperPitch.setTargetPosition(0)
  antenna.stepperYaw.setTargetPosition(0)

  #queueP = asyncio.Queue()
  #queueP.asyncio.maxsize = 3
  #queueY = asyncio.Queue()
  #queueY.asyncio.maxsize = 3

  #move_task = asyncio.create_task(antenna.movetracker())
  #await queueP.join()
  #queueP.put_nowait(90)


  antenna.move_tracker(90, 0)
  while (antenna.stepperPitch.getIsMoving() == True):
    sleep(0.25)


  antenna.move_tracker(-90,0)
  while (antenna.stepperPitch.getIsMoving() == True):
    sleep(0.25)



  antenna.move_tracker(90, 0)
  while (antenna.stepperPitch.getIsMoving() == True):
    sleep(0.25)


  antenna.move_tracker(-90,0)
  while (antenna.stepperPitch.getIsMoving() == True):
    sleep(0.25)

  # antenna.move_tracker(180,180)
  # while (antenna.stepperPitch.getIsMoving() == True):
  #   sleep(0.25)


  # antenna.move_tracker(-180,-180)
  # while (antenna.stepperPitch.getIsMoving() == True):
  #   sleep(0.25)


  antenna.move_tracker(0,0)
  while (antenna.stepperPitch.getIsMoving() == True):
    sleep(0.25)


  #task.cancel()
  #await asyncio.gather(task, return_exceptions = True)
  
  antenna.kill_tracker()

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









