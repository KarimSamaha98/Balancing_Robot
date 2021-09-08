import time
import sys
import os
sys.path.append(os.getcwd())
import math 
from config.config import *
from Utils.Logging.Logging import *
    
try:
    import RPi.GPIO as GPIO
    from mpu6050 import mpu6050
except:
    print('[INFO] Could not import pi based packages')


class Gyro:
    def __init__ (self, addr):
        self.address = addr

    def get_Tilt(self, tilt, dt, reference_time, logging=False):
        #Returns tilt value betwee -90 and 90
        
        Complementary = True
        data = sensor.get_accel_data()
        gyro = sensor.get_gyro_data()
        if Complementary:
            acc = math.atan(data["x"]/(math.sqrt(data["y"]**2+data["z"]**2)))
            gyros = gyro["y"]
            tilt = 0.98*(tilt + (gyros-0.87)*dt) + 0.02*acc*180/math.pi
        else:
            tilt = math.atan(data["x"]/(math.sqrt(data["y"]**2+data["z"]**2)))
            tilt=tilt*180/math.pi
        timestamp = time.time() - reference_time
        
        #Logging
        if logging:
            WriteData('Data/Gyroscope.csv', [timestamp, gyro["x"], gyro["y"], gyro["z"]], ['Time', 'Gyro_x', 'Gyro_y', 'Gyro_z'])
            WriteData('Data/Accelerometer.csv', [timestamp, data["x"], data["y"], data["z"]], ['Time', 'Acc_x', 'Acc_y', 'Acc_z'])
            WriteData('Data/Tilt.csv', [timestamp, tilt], ['Time', 'Tilt_angle'])
        return tilt 

    def get_tilt(self, tilt, dt):
        gyro = sensor.get_gyro_data()
        tilt = tilt + (gyro["y"]-0.87)*dt
        print(tilt)
        return tilt

if __name__ == "__main__":
    Gyro = Gyro(gyro_addr)
    tilt = 0
    init = time.time()
    reference_time = time.time()
    while(True):
        init = time.time()
        dt = init - reference_time
        #tilt = Gyro.get_tilt(tilt, dt)
        tilt = Gyro.get_Tilt(tilt, dt, reference_time, logging=False)
        print(tilt)
        reference_time = time.time()
        time.sleep(0.2)
