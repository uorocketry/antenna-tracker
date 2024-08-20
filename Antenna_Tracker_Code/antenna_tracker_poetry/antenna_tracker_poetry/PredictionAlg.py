# This prediction alg should not be ran on the ras pi and needs to be reviewed 


import numpy as np
from numpy import polynomial
from Rocket import Rocket
from Antenna import Antenna


class PredictionAlg:
    def __init__(self, velocity, time):
        # Ensure the input arrays are of length 500
        if len(velocity) != 500 or len(time) != 500:
            raise ValueError("Both Velocity and Time arrays must be of length 500.")
        
        self.velocity = np.array(velocity)
        self.time = np.array(time)
        self.coefficients = None

    def fit_polynomial(self, degree=7):
        """
        Fits a polynomial of the specified degree to the data.
        The default degree is 7, which gives us 8 coefficients.
        """
        # Fit the polynomial
        self.coefficients = np.polyfit(self.time, self.velocity, degree)
        return self.coefficients

    def get_coefficients(self):
        """
        Returns the coefficients of the fitted polynomial.
        """
        if self.coefficients is None:
            raise ValueError("Polynomial has not been fitted yet. Call fit_polynomial() first.")
        return self.coefficients

    def predict_velocity(self, x):
        """
        Predicts the velocity at a given time x using the fitted polynomial.
        Returns the polynomial in the form of y = a7*x^7 + a6*x^6 + ... + a0
        """
        if self.coefficients is None:
            raise ValueError("Polynomial has not been fitted yet. Call fit_polynomial() first.")
        
        # Calculate the polynomial value at time x
        y = np.polyval(self.coefficients, x)
        
        # Create the polynomial equation as a string
        terms = [f"{self.coefficients[i]:.4f}*x^{len(self.coefficients) - i - 1}" for i in range(len(self.coefficients))]
        equation = " + ".join(terms)
        
        return f"y = {equation}", y

# Example usage:
velocity = np.random.rand(500) * 100  # Example data
time = np.linspace(0, 10, 500)        # Example time data

prediction_alg = PredictionAlg(velocity, time)
prediction_alg.fit_polynomial()  # Fit and get the coefficients

# Predict velocity at a specific time x
equation, predicted_velocity = prediction_alg.predict_velocity(5)
print("Polynomial equation:", equation)
print("Predicted velocity at x=5:", predicted_velocity)



# while antenna.state == "SCANNING" : #Seeking a new signal, should be done in parallel with prediction

#     if rocket.is_connected: # file gets populated maybe time == now (within a sec) ?
#         rocket.state = ("TRACKING")
#         pitchAngle = 0
#         yawAngle = 0
#         yawIncrement = 1
#         break
            
#     rocket.move_tracker(pitchAngle, yawAngle)
            
#     yawAngle = yawAngle + yawIncrement
        
#     if yawAngle >= 90 :
#         pitchAngle = pitchAngle + 1
#         yawIncrement = -1
            
#     elif yawAngle <= 0 :
#         pitchAngle = pitchAngle + 1
#         yawIncrement = 1
            
#     if (yawAngle >= 90 or yawAngle <= 0) and pitchAngle >= 90 :
#         pitchAngle = 0
#         yawAngle = 0
#         yawIncrement = 1
    
#     # When tracking we peek at the top element of the CoodStack and set the rockets Coods accordinglly. Use the Rocket class from there
#     # In the case where the rocket is not connected we will use the predicted coordinated (computed from the ground station TBD) 
                    
# while rocket.state == "TRACKING":
#         # if not connected predicting
#     if rocket.is_connected == True:
            
#         print (CoordStack.peek(0))
            
#         try : 
#             rocket.latitude = (CoordStack.peek(0)[1])
#             rocket.longitude = (CoordStack.peek(0)[2])
#             rocket.altitude = (CoordStack.peek(0)[0])
#         except :
#             print ("Coord Stack is null")
                
#     else : 
            
#         # use predicted coordinated
#         palcehoder = ''
            
#         rocket.move_tracker()
        
#         # Have an manual input to stop process
        
#     if 1 != 1 :# PlaceHolder # Enter Manual input as condition
#         rocket.state = ("IDLE")
#         rocket.kill_tracker()


if __name__ == "__main__":
    rocket = Rocket()
    antnenna = Antenna()


    #Somehow a talbe is filled with info
    #info we need:
        #x axis = time
        #y axis = lat, long, alt
    #CoeffArray[6] = Poly.fit(x[],y[],deg = 7)  
    #   