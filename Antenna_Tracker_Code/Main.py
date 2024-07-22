import Rocket
import Antenna

class Main:
    
    print ("Program Started")

    antenna = Antenna()
    rocket = Rocket()
    
    pitchAngle = 0
    yawAngle = 0
    yawIncrement = 1

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
            
        (Rocket_Latitude, Rocket_Longitude, Rocket_Altitude) = get_rocket_coords()
        
        rocket.latitude(Rocket_Latitude)
        rocket.longitude(Rocket_Longitude)
        rocket.altitude(Rocket_Altitude)
        
        rocket.move_tracker()
        
        if 1 == 1 :# PlaceHolder # Enter Manual input as condition
            rocket.state("IDLE")
        
    def get_rocket_coords ():
        # SQL Query to get Coord
        return (Rocket_Latitude, Rocket_Longitude, Rocket_Altitude)
    