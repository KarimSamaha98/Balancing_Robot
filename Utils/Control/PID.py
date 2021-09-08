from Motors.Motors import *
import sys
import os
sys.path.append(os.getcwd())
from Utils.Logging.Logging import *
class Control:
    def __init__(self, Kp, Ki, Kd, reference, treshhold):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.reference = reference
        self.treshhold = treshhold

    def get_Actuation(self, reading, previous_error, error_integral, delta, reference_time, logging=False):
        #params are the Kp, Ki, Kd parameters
        #output: actuation signals
        error = self.reference - reading
        if abs(error) < 2:
            error = 0

        #calculate the derivative
        error_derivative = (error - previous_error)/delta

        #calculate the integral
        error_integral = ((error + previous_error)/2)*delta + error_integral

        #compute actuation signal
        actuation = self.Kp*error + self.Kd*error_derivative + self.Ki*error_integral
        #need to saturate the input
        #print(actuation)
        if abs(actuation)>self.treshhold:
            if actuation>0:
                actuation = self.treshhold
            else:
                actuation = -self.treshhold
        timestamp = time.time() - reference_time

        #Logging
        if logging:
            WriteData('Data/Controller.csv', [timestamp, error, actuation], ['Time', 'Error', 'Speed'])

        #return the actuation signal
        return actuation,error,error_integral


