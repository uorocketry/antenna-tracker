class Antenna():
    def __init__(self, latitude, longitude, altitude, isConnectedToRocket = False, state = "IDLE"):
    
        self.isConnectedToRocket = isConnectedToRocket
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude
        self.state = state

    # Getter and Setter for isConnectedToRocket
    def getIsConnectedToRocket(self):
        return self.isConnectedToRocket

    def setIsConnectedToRocket(self, isConnectedToRocket):
        self.isConnectedToRocket = isConnectedToRocket

    # Getter and Setter for latitude
    def getLatitude(self):
        return self.latitude

    def setLatitude(self, latitude):
        self.latitude = latitude

    # Getter and Setter for longitude
    def getLongitude(self):
        return self.longitude

    def setLongitude(self, longitude):
        self.longitude = longitude

    # Getter and Setter for altitude
    def getAltitude(self):
        return self.altitude

    def setAltitude(self, altitude):
        self.altitude = altitude

    # Getter and Setter for state
    def getState(self):
        return self.state

    def setState(self, state):
        if state in ["IDLE", "TRACKING", "PREDICTING", "SCANNING"]:
            self._state = state
        else:
            raise ValueError("Invalid state. State must be 'IDLE', 'TRACKING', 'PREDICTING', or 'SCANNING'.")