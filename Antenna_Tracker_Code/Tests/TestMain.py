import csv
from TestRocket import TestRocket
from TestAntenna import TestAntenna
from Phidget22.Phidget import *
from Phidget22.Devices.Stepper import *
import math
import time
from geographiclib.geodesic import Geodesic
import csv
import threading
from TestSharedStack import TestSharedStack

CoordStack = TestSharedStack(500)
PredictionStack = TestSharedStack(100)

antenna = TestAntenna(47.98714, -81.84864, 62.52301) #STEM
print ("antenna built")
rocket = TestRocket(47.986884, -81.848456, 362.52301, antenna)
print ("Rocket built")
rocket.is_connected = True

ReadCoords = True

def CollectingCoords_thread():
    while True:
        with open('gps1.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                CoordStack.push([float(row['alt']), float(row['latitude']), float(row['longitude'])])
                time.sleep(0.1)  # Sleep for half a second
    

def AntennaController_thread ():
    while rocket.state == "IDLE" : 
        
        print ("State: IDLE")
        
        if 1 == 1 :# PlaceHolder # Enter Manual input as condition
            rocket.state = ("SCANNING")
            
    while rocket.state == "SCANNING" : 
        
        print ("State Scanning")

        if rocket.is_connected: # file gets populated maybe time == now (within a sec) ?
            rocket.state = ("TRACKING")
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
                   
    ReadCoords = True 
     
    while rocket.state == "TRACKING":
        
        print ("State : TRACKING")
        # if not connected predicting
        if rocket.is_connected == False:
            
            newaltitude = PredictionStack.peek(0)
            rocket.altitude(newaltitude)
        
        else : 
            
            print (CoordStack.peek(0))
            
            try : 
                rocket.latitude = (CoordStack.peek(0)[1])
                rocket.longitude = (CoordStack.peek(0)[2])
                rocket.altitude = (CoordStack.peek(0)[0])
            except :
                print ("Stack is null")
                
            print ("tracker move")
        
        rocket.move_tracker()
        time.sleep(0.1)  # Sleep for half a second
        
        
        if 1 != 1 :# PlaceHolder # Enter Manual input as condition
            rocket.state = ("IDLE")

def Prediction_thread ():
    
    return

if __name__ == "__main__":

    print ("main")

    

    CoodrsThread = threading.Thread(target=CollectingCoords_thread)
    AntennaThread = threading.Thread(target=AntennaController_thread)
    PredictionThgread = threading.Thread(target=Prediction_thread)
    
    CoodrsThread.start()
    AntennaThread.start()
    
    CoodrsThread.join()
    AntennaThread.join()
        