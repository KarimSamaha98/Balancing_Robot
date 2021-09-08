import time
import sys
import os
import multiprocessing
from multiprocessing import Value
sys.path.append(os.getcwd())
import math 
from config.config import *
from Gyro.Gyro import Gyro
from Utils.Visualisation.Visual import *
from Control.PID import *
from Control.Commander import *
import csv
try:
    import RPi.GPIO as GPIO
    from mpu6050 import mpu6050
except:
    print('[INFO] Could not import pi based packages')
import glob

def InitializePWM():
    #Using RPi.GPIO
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(CLK_M1,GPIO.OUT)
    GPIO.setup(CW_M1,GPIO.OUT)
    pwm1 = GPIO.PWM(CLK_M1,100)
    GPIO.output(CW_M1,0)
    pwm1.start(0)
    GPIO.setup(CLK_M2,GPIO.OUT)
    GPIO.setup(CW_M2,GPIO.OUT)
    pwm2 = GPIO.PWM(CLK_M2,100)
    GPIO.output(CW_M2,1)
    pwm2.start(0)
    return pwm1, pwm2
    
    

#Clean Log
files = glob.glob('Data/*')
for f in files:
    os.remove(f)

#Reset Clock
reference_time = time.time()

#Controlling Loop
def MainLoop():

    #Instantiate a gyro object
    Gyroscope = Gyro(gyro_addr)

    #Instantiate a controller object
    Kp = 2
    Kd = 0
    Ki = 0
    Controller = Control(Kp, Ki, Kd, 0, 600)

    #Initiate data
    Tilt = []
    Time_t = []
    Time_s = []
    Speed = []
    previous_error = 0
    error_integral = 0
    angle = 0
    init_time = time.time()
    
    
    #Initialize PWM
    pwm1, pwm2 = InitializePWM()

    r1 = time.time()
    while True:
        final_time = time.time()
        delta = final_time-init_time
        #Extract the value continuously
        try:
            angle = Gyroscope.get_Tilt(angle, delta, logging=False, reference_time=reference_time)
        except:
            print('[INFO] Could not fetch angle value')
            break

        
        speed, previous_error, error_integral = Controller.get_Actuation(angle, previous_error, error_integral, delta, logging=False, reference_time=reference_time)
        init_time = time.time()
        
        #Take action
        if abs(speed)>2000:
            speed = 2000
        if speed < 0:
            GPIO.output(CW_M1,1)
            GPIO.output(CW_M2,0)
        else:
            GPIO.output(CW_M1,0)
            GPIO.output(CW_M2,1)
        
        pwm1.ChangeFrequency(speed)
        pwm2.ChangeFrequency(speed)
        
        r1 = time.time()
        print(speed)
        time.sleep(0.1)


MainLoop()

#Launch Multiprocessing
#p1 = multiprocessing.Process(target=MainLoop, args=(speed,))
#p3 = multiprocessing.Process(target=LivePlot, args=['Data/Tilt.csv',0])
#p1.start()
#p2.start()
#p3.start()
#p3.join()
