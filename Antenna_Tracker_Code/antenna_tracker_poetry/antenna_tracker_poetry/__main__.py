import csv
from Rocket import Rocket
from Antenna import Antenna
from PredictionAlg import PredictionAlg
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

# class Antenna:
#     def __init__(self, latitude, longitude, altitude, is_connected_to_rocket = False, state = "IDLE"):
# class Rocket:
#     def __init__(self, latitude, longitude, altitude):
# class PredictionAlg:
#     def __init__(self, latituide, lognitude, altitude, time):

rocket = Rocket(47.986884, -81.848456, 362.52301) 
antenna = Antenna(47.98714, -81.84864, 62.52301, False, "IDLE") #STEM
predict = PredictionAlg()


def AntennaController_thread (): #State checker 
    
    # In Idle the antenna is not moving, waiting for a manual input to start scanning
    
    while rocket.state == "IDLE" : 

        print("Tracker is Idle, do you want to attempt a connection(y/n): ")
        startScan = input()
        if startScan == 'y':
            #start the connection
            antenna.state = "SCANNING"
            find_rocket()

        elif startScan == 'n':
            print("Okay, exiting...")
            break

        else:
            print("Wrong character entered, try again...")
            
    # In Scanning the antenna is moving in a set pattern (still subject to change)
    # IMPORTANT need to determin a way to know if the rocket is connected
        # Possible solution, if data in, in the last X seconds then it is considered connected
    return


def find_rocket():
    
    #establishes connection to rocket, hope ground station has it connected...
    if antenna.is_connected_to_rocket == True:
        antenna.state = "TRACKING"
        collectingCoords_thread()
        #Call the pitch and yaw calc
    
    elif antenna.is_connected_to_rocket == False:
        antenna.state = "PREDICTING"
        #ask prediction 
    
    return


def collectingCoords_thread():
    
    # Add coolection code
    # Populates the CoordStack
    # Expected output format
        # Array [latitude, longitude, altitude, timestamp]
        #populates into rocket
        #sets ant state to tracking
        
    rocket.latitude =...
    rocket.longitude =...
    rocket.altitude =...

    move_one_step()
    
    return


def move_one_step():        #Drivers seem to remember its intial pos and moving is done wrt to pos 0.
    
    antenna.move_tracker(calc_pitch(), calc_yaw())

    find_rocket()

    return

  
def calc_yaw():
        x = math.radians(rocket.latitude - antenna.latitude)
        y = math.radians(rocket.longitude - antenna.longitude) #MAY NOT BE ACCURATE, SINCE TLONG LINE ARE NOT PARALLEL 'LONG TERM'
        
        try :
            yawRad = math.atan(y/x)
            yawDeg = math.degrees(yawRad)
        except : 
            print ("calc_yaw : division by 0")

        return yawDeg


def calc_pitch():
        altdiff = rocket.altitude - antenna.altitude
        dist = Geodesic.WGS84.Inverse(antenna.latitude, antenna.longitude, rocket.latitude, rocket.longitude)
        pitchRad = math.atan(altdiff/dist['s12']) #Meters
        pitchDeg = math.degrees(pitchRad)
        return pitchDeg




if __name__ == "__main__":      #What is this?

    CoordStack = SharedStack(500)

    antenna = Antenna()
    rocket = Rocket()

    CoodrsThread = threading.Thread(target=CollectingCoords_thread)
    AntennaThread = threading.Thread(target=AntennaController_thread)
    
    CoodrsThread.start()
    AntennaThread.start()
    
    CoodrsThread.join()
    AntennaThread.join()
        
   
    