import csv
import socket
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
import json



CoordStack = TestSharedStack(500)
PredictionStack = TestSharedStack(100)

lastcoord = None

antenna = TestAntenna(45.420456125900316, -75.68087806949006, 62.52301) #STEM
# antenna = TestAntenna(0,0 ,0) #STEM
print ("antenna built")
rocket = TestRocket(47.986884, -81.848456, 362.52301, antenna)
print ("Rocket built")
rocket.is_connected = True

ReadCoords = True

def CollectingCoords_thread():
    global lastcoord
    # while True:
    #     with open('gps1.csv', newline='') as csvfile:
    #         reader = csv.DictReader(csvfile)
    #         for row in reader:
    #             CoordStack.push([float(row['alt']), float(row['latitude']), float(row['longitude'])])
    #             time.sleep(0.01)  # Sleep for half a second
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(("172.20.10.2", 5757))
        print("Connected")
        
        
        while True:
            data = s.recv(1024)
            if not data:
                print("no data!!!")
                continue
            # print("received: ", data.decode('utf-8'))
            try:
                datum = data.decode("utf-8").splitlines()
                for line in datum:
                    dat = json.loads(line)
                    
                    # print(dat)
                    alt = dat["alt"]
                    lon = dat['lon']
                    lat = dat['lat']
                    t = dat['t']
                    coords = [alt, lat,lon, t]
                    
                    lastcoord = coords
            except Exception as e:
                print(e)
                # exit(1)
            # time.sleep(0.1)
            
            

    

def AntennaController_thread ():
    global lastcoord
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
        time.sleep(0.01)  # Sleep for half a second
        
        print ("State : TRACKING")
        # if not connected predicting
        if rocket.is_connected == False:
            raise "aaa"
            newaltitude = PredictionStack.peek(0)
            rocket.altitude(newaltitude)
        
        else : 
            if lastcoord is not None:
                print(lastcoord)
                rocket.altitude=(lastcoord[0])
                rocket.latitude=(lastcoord[1])
                rocket.longitude=(lastcoord[2])
            else:
                print("empty last coord, skipping")
                continue
                
        print ("tracker move")
        rocket.move_tracker()
        
        
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
        