import csv
import Rocket
import Antenna
from Phidget22.Phidget import *
from Phidget22.Devices.Stepper import *
import math
import time
from geographiclib.geodesic import Geodesic
import csv
import threading
import SharedStack

def CollectingCoords_thread ():
    # Add coolection code
    return

def AntennaController_thread (Rocket rocket):
    while rocket.state == "IDLE" : 
        if 1 == 1 :# PlaceHolder # Enter Manual input as condition
            rocket.state("SCANNING")
            
    while rocket.state == "SCANNING" : 

        if rocket.is_connected: # file gets populated maybe time == now (within a sec) ?
            rocket.state("TRACKING")
            pitchAngle = 0
            yawAngle = 0
            yawIncrement = 1
            break
            
        rocket.move_traker(pitchAngle, yawAngle)
            
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
                    
    while rocket.state == "TRACKING":
        # if not connected predicting
        if rocket.is_connected == False:
            
            newaltitude = PredictionStack.peak(0)
            rocket.altitude(newaltitude)
        
        else : 
            
            (Rocket_Latitude, Rocket_Longitude, Rocket_Altitude) = get_rocket_coords()
            
            rocket.latitude(Rocket_Latitude)
            rocket.longitude(Rocket_Longitude)
            rocket.altitude(Rocket_Altitude)
        
        lastadjusttime = timesincetakeoff
        
        rocket.move_tracker()
        
        if 1 == 1 :# PlaceHolder # Enter Manual input as condition
            rocket.state("IDLE")

def Prediction_thread ():
    
    return

if __name__ == "__main__":

    CoordStack = SharedStack(500)
    PredictionStack = SharedStack(100)

    antenna = Antenna()
    rocket = Rocket()

    CoodrsThread = threading.Thread(target=CollectingCoords_thread)
    AntennaThread = threading.Thread(target=AntennaController_thread, args=(rocket,))
    PredictionThgread = threading.Thread(target=Prediction_thread)
        
   
    