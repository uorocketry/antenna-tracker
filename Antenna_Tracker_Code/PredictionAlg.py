# This prediction alg should not be ran on the ras pi and needs to be reviewed 


import numpy as np

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
