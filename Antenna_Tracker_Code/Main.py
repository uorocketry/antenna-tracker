import csv
import Rocket
import Antenna
from Phidget22.Phidget import *
from Phidget22.Devices.Stepper import *
import math
import time
from geographiclib.geodesic import Geodesic
import csv

currentalt = 0
lastalt = 0
    
class Main:
    
    print ("Program Started")

    antenna = Antenna()
    rocket = Rocket()
    
    pitchAngle = 0
    yawAngle = 0
    yawIncrement = 1
    
    accelerationcoefficients = [-0.704039127,57.91038515, 9.4385495, 6.30910149, -7.281367082, 2.869182813, -0.503382474, 0.032046176]
    decelerationcoefficients = [592.9403369, -49.48217932, 2.426806241, -0.065001575, 0.001014778, -0.00000914314, 0.0000000435434, -0.0000000000841452]
    
    timesincetakeoff = 0 # tbd
    
    def get_rocket_coords ():
        
        lastalt = currentalt 

        with open('gps1.csv', newline='') as csvfile:
            
            reader = csv.DictReader(csvfile)
            
            Rocket_Latitude = float(1['latitude'])
            Rocket_Longitude = float(1['longitude'])
            Rocket_Altitude = float(1['alt'])
            
            currentalt = Rocket_Altitude
            
        return (Rocket_Latitude, Rocket_Longitude, Rocket_Altitude)
    
    def is_accending ():
        return True

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
            if is_accending == True :
                predictedvel = (
                    accelerationcoefficients[7] * (timesincetakeoff ** 7) +
                    accelerationcoefficients[6] * (timesincetakeoff ** 6) +
                    accelerationcoefficients[5] * (timesincetakeoff ** 5) +
                    accelerationcoefficients[4] * (timesincetakeoff ** 4) +
                    accelerationcoefficients[3] * (timesincetakeoff ** 3) +
                    accelerationcoefficients[2] * (timesincetakeoff ** 2) +
                    accelerationcoefficients[1] * (timesincetakeoff ** 1) +
                    accelerationcoefficients[0]
                )
            else : 
                predictedvel = (
                    decelerationcoefficients[7] * (timesincetakeoff ** 7) +
                    decelerationcoefficients[6] * (timesincetakeoff ** 6) +
                    decelerationcoefficients[5] * (timesincetakeoff ** 5) +
                    decelerationcoefficients[4] * (timesincetakeoff ** 4) +
                    decelerationcoefficients[3] * (timesincetakeoff ** 3) +
                    decelerationcoefficients[2] * (timesincetakeoff ** 2) +
                    decelerationcoefficients[1] * (timesincetakeoff ** 1) +
                    decelerationcoefficients[0]
                )
            
            newaltitude = rocket.altitude + predictedvel * (timesincetakeoff - lastadjusttime)
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
        
   
    