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

# Phidget API info : https://www.phidgets.com/?view=api

# Place Holder Values, need to figure out how they will be entered initially (rocket might not need intial value but TBD)

antenna = Antenna(47.98714, -81.84864, 62.52301) #STEM
rocket = Rocket(47.986884, -81.848456, 362.52301, antenna)

def CollectingCoords_thread ():
    
    
    # Add coolection code
    # Populates the CoordStack
    # Expected output format
        # Array [latitude, longitude, altitude, timestamp]
    
    return

def AntennaController_thread ():
    
    # In Idle the antenna is not moving, waiting for a manual input to start scanning
    
    while rocket.state == "IDLE" : 
        if 1 == 1 :# PlaceHolder # Enter Manual input as condition
            rocket.state = ("SCANNING")
            
    # In Scanning the antenna is moving in a set pattern (still subject to change)
    # IMPORTANT need to determin a way to know if the rocket is connected
        # Possible solution, if data in, in the last X seconds then it is considered connected
            

def calc_yaw(rocket_latitude):
        x = math.radians(self._rocket.latitude - self._latitude)
        y = math.radians(self._rocket.longitude - self._longitude) #MAY NOT BE ACCURATE, SINCE TLONG LINE ARE NOT PARALLEL 'LONG TERM'
        
        try :
            yawRad = math.atan(y/x)
            yawDeg = math.degrees(yawRad)
        except : 
            print ("calc_yaw : division by 0")

        return yawDeg







    while rocket.state == "SCANNING" : 

        if rocket.is_connected: # file gets populated maybe time == now (within a sec) ?
            rocket.state = ("TRACKING")
            pitchAngle = 0
            yawAngle = 0
            yawIncrement = 1
            break
            
        rocket.move_tracker(pitchAngle, yawAngle)
            
        yawAngle = yawAngle + yawIncrement
        
        if yawAngle >= 90 :
            pitchAngle = pitchAngle + 1
            yawIncrement = -1
            
        elif yawAngle <= 0 :
            pitchAngle = pitchAngle + 1
            yawIncrement = 1
            
        if (yawAngle >= 90 or yawAngle <= 0) and pitchAngle >= 90 :
            pitchAngle = 0
            yawAngle = 0
            yawIncrement = 1
    
    # When tracking we peek at the top element of the CoodStack and set the rockets Coods accordinglly. Use the Rocket class from there
    # In the case where the rocket is not connected we will use the predicted coordinated (computed from the ground station TBD) 
                    
    while rocket.state == "TRACKING":
        # if not connected predicting
        if rocket.is_connected == True:
            
            print (CoordStack.peek(0))
            
            try : 
                rocket.latitude = (CoordStack.peek(0)[1])
                rocket.longitude = (CoordStack.peek(0)[2])
                rocket.altitude = (CoordStack.peek(0)[0])
            except :
                print ("Coord Stack is null")
                
        else : 
            
            # use predicted coordinated
            palcehoder = ''
            
        rocket.move_tracker()
        
        # Have an manual input to stop process
        
        if 1 != 1 :# PlaceHolder # Enter Manual input as condition
            rocket.state = ("IDLE")
            rocket.kill_tracker()


if __name__ == "__main__":

    CoordStack = SharedStack(500)

    antenna = Antenna()
    rocket = Rocket()

    CoodrsThread = threading.Thread(target=CollectingCoords_thread)
    AntennaThread = threading.Thread(target=AntennaController_thread)
    
    CoodrsThread.start()
    AntennaThread.start()
    
    CoodrsThread.join()
    AntennaThread.join()
        
   
    