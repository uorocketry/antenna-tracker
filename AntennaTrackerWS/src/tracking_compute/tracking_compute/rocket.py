class Rocket:
    def __init__(self, latitude, longitude, altitude):
        self._latitude = latitude
        self._longitude = longitude
        self._altitude = altitude 

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