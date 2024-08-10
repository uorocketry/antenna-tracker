from Phidget22.Phidget import *
from Phidget22.Devices.Stepper import *
import math
from geographiclib.geodesic import Geodesic
from TestAntenna import TestAntenna
import time

class TestRocket:
    def __init__(self, latitude, longitude, altitude, antenna, is_connected=False, state="IDLE"):
        self._antenna = antenna
        self._is_connected = is_connected
        self._latitude = latitude
        self._longitude = longitude
        self._altitude = altitude
        self._state = state
         
        
        
        self.stepperPitch = Stepper() 
        print ("Stepper init")
        self.stepperPitch.openWaitForAttachment(5000)
        print("waited for attach")
        # exception handle

        self.stepperPitch.setEngaged(True)
        print("Motor engagedS")
        
        
    
        # exception handle
        #kill in case of exception
        
    # Getter for IsConnected
    @property
    def is_connected(self):
        return self._is_connected

    # Setter for IsConnected
    @is_connected.setter
    def is_connected(self, value):
        self._is_connected = value

    # Getter for Latitude
    @property
    def latitude(self):
        return self._latitude

    # Setter for Latitude
    @latitude.setter
    def latitude(self, value):
        self._latitude = value

    # Getter for Longitude
    @property
    def longitude(self):
        return self._longitude
    
    # Getter for Altitude
    @property
    def altitude(self):
        return self._altitude

    # Setter for Altitude
    @altitude.setter
    def altitude(self, value):
        self._altitude = value

    # Setter for Longitude
    @longitude.setter
    def longitude(self, value):
        self._longitude = value

    # Getter for State
    @property
    def state(self):
        return self._state

    # Setter for State
    @state.setter
    def state(self, value):
        if value in ["IDLE", "TRACKING", "PREDICTING", "SCANNING"]:
            self._state = value
        else:
            raise ValueError("Invalid state. State must be 'IDLE', 'TRACKING', 'PREDICTING', or 'SCANNING'.")

    # Specific Setter for State to IDLE
    def set_state_to_idle(self):
        self._state = "IDLE"

    # Specific Setter for State to TRACKING
    def set_state_to_tracking(self):
        self._state = "TRACKING"

    # Specific Setter for State to PREDICTING
    def set_state_to_predicting(self):
        self._state = "PREDICTING"

    # Specific Setter for State to SCANNING
    def set_state_to_scanning(self):
        self._state = "SCANNING"
    
    def calc_pitch(self):
            altdiff = self._altitude - self._antenna.altitude
            dist = Geodesic.WGS84.Inverse(self._antenna.latitude, self._antenna.longitude, self._latitude, self._longitude)
            pitchRad = math.atan(altdiff/dist['s12'])
            pitchDeg = math.degrees(pitchRad)
            return pitchDeg
        
    def update_tracker_position(self):
    
        pitchSteps = (self.calc_pitch())*(27200/360)
        
        # no gearbox and bet 360 deg is 3200 (360/1.8 * 16)
        # gearbox ratio 4.25 (estimate)
        # bet ratio is 2
        # devide or mutiply
        # with gearbox 360 deg is 27200 (3200 * 4.25 *2)
        # real step angle = 360/27200

        return (pitchSteps)
    
    def move_tracker(self):
        
        (pitchSteps) = self.update_tracker_position()

        try :
            self.stepperPitch.setTargetPosition((pitchSteps))
        except : 
            print ("Pitch Stepper Set Target Position Failed")
            
        
        # exception

        print("Pitch Position: " + str(self.stepperPitch.getPosition()))


    
    def kill_tracker(self):
         
        try :
            self.stepperPitch.setTargetPosition(0)
        except : 
            print ("Pitch Stepper Set Target Position Failed during kill")

        time.sleep(1)

        #print("Pitch Position: " + str(self.stepperPitch.getPosition()))
        try :
            self.stepperPitch.close()
        except :
            print ("Pitch Stepper Close Failed")


        print("Steepers Killed")

   