from Phidget22.Phidget import *
from Phidget22.Devices.Stepper import *
import math
from geographiclib.geodesic import Geodesic
import Antenna
import time

class Rocket:
    def __init__(self, is_connected=False, latitude=0.0, longitude=0.0, altitude=0.0, state="IDLE"):
        if not isinstance(Antenna):
            raise ValueError("antenna must be an instance of the Antenna class")
        self._antenna = Antenna
        self._is_connected = is_connected
        self._latitude = latitude
        self._longitude = longitude
        self._altitude = altitude
        self._state = state
        
        self.stepperPitch = Stepper() 
        self.stepperYaw = Stepper() 
        
        self.stepperPitch.openWaitForAttachment(5000)
        self.stepperYaw.openWaitForAttachment(5000)
        
        self.stepperPitch.setEngaged(True)
        self.stepperYaw.setEngaged(True)
    
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

    def calc_yaw(self):
        x = math.radians(self._antenna.latitude - self._latitude)
        y = math.radians(self._antenna.longitude - self._longitude)
        yawRad = math.atan(y/x)
        yawDeg = math.degrees(yawRad)

        return yawDeg
    
    def calc_pitch(self):
            altdiff = self._altitude - self._antenna.altitude
            dist = Geodesic.WGS84.Inverse(self._antenna.latitude, self._antenna.longitude, self._latitude, self._longitude)
            pitchRad = math.atan(altdiff/dist['s12'])
            pitchDeg = math.degrees(pitchRad)
            return pitchDeg
        
    def update_tracker_position(self):

        pitchSteps = self.calc_pitch*(13600/360)

        yawSteps = self.calc_yaw*(13600/360)
        return (pitchSteps, yawSteps)
    
    def move_tracker(self):
        
        (pitchSteps, yawSteps) = self.update_tracker_position()

        self.stepperPitch.setTargetPosition((pitchSteps))
        self.stepperYaw.setTargetPosition(yawSteps)

        # print("Pitch Position: " + str(self.stepperPitch.getPosition()))

        # print("Yaw Position: " + str(yawDeg))
            
        # print("Yaw Position: " + str(self.stepperYaw.getPosition()) )

    
    def kill_tracker(self):
        self.stepperPitch.setTargetPosition(0)
        self.stepperYaw.setTargetPosition(0)
        time.sleep(1)

        #print("Pitch Position: " + str(self.stepperPitch.getPosition()))
        #print("Yaw Position: " + str(self.stepperYaw.getPosition()) )
        
        self.stepperPitch.close()
        self.stepperYaw.close()
        print("Steepers Killed")
        
        
    def update_tracker_position(self, pitchAngle, yawAngle):

        pitchSteps = pitchAngle*(13600/360)

        yawSteps = yawAngle*(13600/360)
        return (pitchSteps, yawSteps)
    
    def move_tracker(self, pitchAngle, yawAngle):
        
        (pitchSteps, yawSteps) = self.update_tracker_position(pitchAngle, yawAngle)

        self.stepperPitch.setTargetPosition((pitchSteps))
        self.stepperYaw.setTargetPosition(yawSteps)

        # print("Pitch Position: " + str(self.stepperPitch.getPosition()))

        # print("Yaw Position: " + str(yawDeg))
            
        # print("Yaw Position: " + str(self.stepperYaw.getPosition()) )

    