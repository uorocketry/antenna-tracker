from Phidget22.Phidget import *
from Phidget22.Devices.Stepper import *
import math
from geographiclib.geodesic import Geodesic
from TestAntenna import TestAntenna
import time

class TestRocket:
    def __init__(self, latitude, longitude, altitude, antenna, is_connected=False, state="IDLE"):
        self.antenna = antenna
        self.is_connected = is_connected
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude
        self.state = state
        
        try : 
            self.stepperPitch = Stepper() 
            self.stepperYaw = Stepper() 
            
            self.stepperPitch.openWaitForAttachment(5000)
            self.stepperYaw.openWaitForAttachment(5000)
            
            self.stepperPitch.setEngaged(True)
            self.stepperYaw.setEngaged(True)
        except :
            raise Exception("Steppers failed to engaged")
    

    # Specific Setter for State to IDLE
    def setstate_to_idle(self):
        self.state = "IDLE"

    # Specific Setter for State to TRACKING
    def setstate_to_tracking(self):
        self.state = "TRACKING"

    # Specific Setter for State to PREDICTING
    def setstate_to_predicting(self):
        self.state = "PREDICTING"

    # Specific Setter for State to SCANNING
    def setstate_to_scanning(self):
        self.state = "SCANNING"
        
    # Uses the latitude and longitude of the rocket and antenna to the yaw angle of the antenna

    def calc_yaw(self):
        x = math.radians(self.antenna.latitude - self.latitude)
        y = math.radians(self.antenna.longitude - self.longitude)
        

        yawRad = math.atan2(y,x)
        yawDeg = math.degrees(yawRad)

        return yawDeg
    
    # Uses the altitude of the rocket and antenna to the pitch angle of the antenna
    # Geodesic is used to account for the curvature of the earth
    
    def calc_pitch(self):
            altdiff = self.altitude - self.antenna.altitude
           
            dist = Geodesic.WGS84.Inverse(self.antenna.latitude, self.antenna.longitude, self.latitude, self.longitude)
            
            pitchRad = math.atan2(altdiff, dist['s12'])
            # pitchRad = math.asin(altdiff, dist['s12']
            # https://geographiclib.sourceforge.io/html/python/code.html
            pitchDeg = math.degrees(pitchRad)
            return pitchDeg

    
    def kill_tracker(self):
         
        try :
            self.stepperPitch.setTargetPosition(0)
        except : 
            print ("Pitch Stepper Set Target Position Failed during kill")
    
        try: 
            self.stepperYaw.setTargetPosition(0)
        except : 
            print ("Yaw Stepper Set Target Position Failed during kill")

        time.sleep(1)

        #print("Pitch Position: " + str(self.stepperPitch.getPosition()))
        #print("Yaw Position: " + str(self.stepperYaw.getPosition()) )
        try :
            self.stepperPitch.close()
        except :
            print ("Pitch Stepper Close Failed")

        try :
            self.stepperYaw.close()
        except :
            print ("Yaw Stepper Close Failed")

        print("Steepers Killed")
        
    # Translates the angle to the antenna to steps needed by each motor to attain the wanted position
        
    def update_tracker_position(self, pitchAngle = None, yawAngle = None):
        
        if (pitchAngle == None and yawAngle == None):
            pitchSteps = self.calc_pitch()*(6800/360)
            yawSteps = self.calc_yaw()*(6800/360)
        
            # no gearbox and bet 360 deg is 3200 (360/1.8 * 16) # 16 is the micro-step ratio https://www.phidgets.com/?prodid=1029#Open_and_Closed_Loop_Control
            # gearbox ratio 1:4.25 (estimate)
            # bet ratio is 2:1
            # devide or mutiply
            # with gearbox 360 deg is 6800 (3200 * 4.25 / 2)
            # real step angle = 360/6800
        else: 

            pitchSteps = pitchAngle*(6800/360)

            yawSteps = yawAngle*(6800/360)
        return (pitchSteps, yawSteps)
    
    # Calls the update tracker position method and makes the motors move the wanted amount of steps
    
    def move_tracker(self, pitchAngle = None, yawAngle = None):
        (pitchSteps, yawSteps) = self.update_tracker_position(pitchAngle, yawAngle)

        try :
            self.stepperPitch.setTargetPosition((pitchSteps))
        except : 
            print ("Pitch Stepper Set Target Position Failed")

        try: 
            self.stepperYaw.setTargetPosition(yawSteps)
        except : 
            print ("Yaw Stepper Set Target Position Failed")

        # print("Pitch Position: " + str(self.stepperPitch.getPosition()))

        # print("Yaw Position: " + str(yawDeg))
            
        # print("Yaw Position: " + str(self.stepperYaw.getPosition()) )