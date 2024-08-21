#This program initializes the rocket class, will be used to store "current time" properties that will be updated
#Also in charge of connecting the motors together and actuating them
#Rocket is conerned with its own alt, lat, long, state, and connection to the antenna class
#the state determines which mode will be used to update the actuation of the motors


#               **THINGS TO ADD**
#   homing operation at startup, use the limit switches



from Phidget22.Phidget import *
from Phidget22.Devices.Stepper import *
import math
from geographiclib.geodesic import Geodesic
from Rocket import Rocket
import time

class Antenna:
    async def __init__(self, latitude, longitude, altitude, is_connected_to_rocket = False, state = "IDLE"):
    
        self._is_connected_to_rocket = is_connected_to_rocket
        self._latitude = latitude
        self._longitude = longitude
        self._altitude = altitude
        self._state = state
        
        try : #Attempting to connect the pitch and yaw motors to their drivers
            self.stepperPitch = Stepper() 
            #self.stepperYaw = Stepper()                                             #INC AN ACCELERATION AND VELOCITY LIMIT. FOR SAFETY
                
            self.stepperPitch.openWaitForAttachment(5000) #mili sec
            #self.stepperYaw.openWaitForAttachment(5000)
                
            self.stepperPitch.setEngaged(True)
            #self.stepperYaw.setEngaged(True)
        except :
            raise Exception("Steppers failed to engaged")
        
    # Getter for IsConnected
    @property
    async def is_connected_to_rocket(self):
        return self._is_connected_to_rocket

    # Setter for IsConnected
    @is_connected_to_rocket.setter
    async def is_connected_to_rocket(self, value):
        self._is_connected_to_rocket = value

    # Getter for Latitude
    @property
    async def latitude(self):
        return self._latitude

    # Setter for Latitude
    @latitude.setter
    async def latitude(self, value):
        self._latitude = value

    # Getter for Longitude
    @property
    async def longitude(self):
        return self._longitude
    
    # Getter for Altitude
    @property
    async def altitude(self):
        return self._altitude

    # Setter for Altitude
    @altitude.setter
    async def altitude(self, value):
        self._altitude = value

    # Setter for Longitude
    @longitude.setter
    async def longitude(self, value):
        self._longitude = value

    # Getter for State
    @property
    async def state(self):
        return self._state

    # Setter for State
    @state.setter
    async def state(self, value):
        if value in ["IDLE", "TRACKING", "PREDICTING", "SCANNING"]:
            self._state = value
        else:
            raise ValueError("Invalid state. State must be 'IDLE', 'TRACKING', 'PREDICTING', or 'SCANNING'.")

    # Specific Setter for State to IDLE
    async def set_state_to_idle(self):
        self._state = "IDLE"

    # Specific Setter for State to TRACKING
    async def set_state_to_tracking(self):
        self._state = "TRACKING"

    # Specific Setter for State to PREDICTING
    async def set_state_to_predicting(self):
        self._state = "PREDICTING"

    # Specific Setter for State to SCANNING
    async def set_state_to_scanning(self):
        self._state = "SCANNING"
        
    
    #METHODS

    # Uses the latitude and longitude of the rocket and antenna to the yaw angle of the antenna

    # def calc_yaw(self):
    #     x = math.radians(self._rocket.latitude - self._latitude)
    #     y = math.radians(self._rocket.longitude - self._longitude) #MAY NOT BE ACCURATE, SINCE TLONG LINE ARE NOT PARALLEL 'LONG TERM'
        
    #     try :
    #         yawRad = math.atan(y/x)
    #         yawDeg = math.degrees(yawRad)
    #     except : 
    #         print ("calc_yaw : division by 0")

    #     return yawDeg
    
    # Uses the altitude of the rocket and antenna to the pitch angle of the antenna
    # Geodesic is used to account for the curvature of the earth
    #The output of 'Geodesic.WGS84.Inverse' can be found at: https://geographiclib.sourceforge.io/html/python/interface.html#dict
    
    # def calc_pitch(self):
    #         altdiff = self._rocket_altitude - self._antenna.altitude
    #         dist = Geodesic.WGS84.Inverse(self._antenna.latitude, self._antenna.longitude, self._latitude, self._longitude)
    #         pitchRad = math.atan(altdiff/dist['s12']) #Meters
    #         pitchDeg = math.degrees(pitchRad)
    #         return pitchDeg


    # Translates the angle to the antenna to steps needed by each motor to attain the wanted position
    async def update_tracker_position(self, pitchAngle = None, yawAngle = None):
        
            # no gearbox and bet 360 deg is 3200 (360/1.8 * 16)
            # gearbox ratio 4.25 (estimate)
            # bet ratio is 2
            # devide or mutiply
            # with gearbox 360 deg is 27200 (3200 * 4.25 *2)
            # real step angle = 360/27200
       
        pitchSteps = pitchAngle*(27200/360)
        yawSteps = yawAngle*(27200/360)

        return (pitchSteps, yawSteps)    


# Calls the update tracker position method and makes the motors move the wanted amount of steps
    async def move_tracker(self, pitchAngle = None, yawAngle = None):
                
        (pitchSteps, yawSteps) = self.update_tracker_position(pitchAngle, yawAngle)

        try :
            self.stepperPitch.setTargetPosition((pitchSteps))
        except : 
            print ("Pitch Stepper Set Target Position Failed")

        # try: 
        #     self.stepperYaw.setTargetPosition(yawSteps)
        # except : 
        #     print ("Yaw Stepper Set Target Position Failed")

    #print("Pitch Position: " + str(self.stepperPitch.getPosition()))

        # print("Yaw Position: " + str(yawDeg))
            
    #print("Yaw Position: " + str(self.stepperYaw.getPosition()) )

    
    async def kill_tracker(self):
         
        # try :                                         #maybe remove this comment
        #     self.stepperPitch.setTargetPosition(0)
        # except Exception as e: 
        #     print ("Pitch Stepper Set Target Position Failed during kill")
        #     raise e
    
        # try: 
        #     self.stepperYaw.setTargetPosition(0)
        # except Exception as e: 
        #     print ("Yaw Stepper Set Target Position Failed during kill")
        #     raise e

        time.sleep(1)

        #print("Pitch Position: " + str(self.stepperPitch.getPosition()))
        #print("Yaw Position: " + str(self.stepperYaw.getPosition()) )
        try :
            self.stepperPitch.close()
        except Exception as e:
            print ("Pitch Stepper Close Failed")
            raise e

        # try :
        #     self.stepperYaw.close()
        # except Exception as e:
        #     print ("Yaw Stepper Close Failed")
        #     raise e

        print("Steepers Killed")
        

        

    
    