

import time
import sys
import os
sys.path.append(os.getcwd())
import math 
from config.config import *
    
try:
    import RPi.GPIO as GPIO
    from mpu6050 import mpu6050
except:
    print('[INFO] Could not import pi based packages')


def rotateMotorR():
    #Set direction
    GPIO.output(CW_M2,GPIO.HIGH)
    time.sleep(0.001)
    GPIO.output(CLK_M2,GPIO.HIGH)
    time.sleep(0.001)
    GPIO.output(CLK_M2,GPIO.LOW)


def rotateMotorL():
    #Set direction
    GPIO.output(CW_M1,GPIO.HIGH)
    time.sleep(0.001)
    GPIO.output(CLK_M1,GPIO.HIGH)
    time.sleep(0.001)
    GPIO.output(CLK_M1,GPIO.LOW)


def move_forward(speed):
    #Find the residual delay
    T = (degperstep*60)/(360*speed)
    T = T - (6.25*10**-5)
    if T<0: #Faster than maximum
        T = 0

    #Set direction
    GPIO.output(CW_M2,GPIO.HIGH)
    GPIO.output(CW_M1,GPIO.LOW)
    time.sleep((6.25*10**-5))
    GPIO.output(CLK_M1,GPIO.HIGH)
    GPIO.output(CLK_M2,GPIO.HIGH)
    time.sleep((6.25*10**-5))
    GPIO.output(CLK_M1,GPIO.LOW)
    GPIO.output(CLK_M2,GPIO.LOW)
    time.sleep(T)

def move_backward(speed):
    #Find the residual delay
    T = (degperstep*60)/(360*speed)
    T = T - (6.25*10**-5)
    if T<0: #Faster than maximum
        T = 0

    #Set direction
    GPIO.output(CW_M1,GPIO.HIGH)
    GPIO.output(CW_M2,GPIO.LOW)
    time.sleep(6.25*10**-5)
    GPIO.output(CLK_M1,GPIO.HIGH)
    GPIO.output(CLK_M2,GPIO.HIGH)
    time.sleep(6.25*10**-5)
    GPIO.output(CLK_M1,GPIO.LOW)
    GPIO.output(CLK_M2,GPIO.LOW)
    time.sleep(T)


def TestMotors():
    print('Testing Right Motor ...')
    for i in range(1000):
        rotateMotorR()

    print('Testing Left Motor ...')
    for i in range(1000):
        rotateMotorL()

    print('Moving Forward ...')
    for i in range(1000):
        move_forward(200)

    print('Moving Backward ...')
    for i in range(1000):
        move_backward(200)

def get_Tilt():
    data = sensor.get_accel_data()
    tilt = math.atan(data["x"]/(math.sqrt(data["y"]**2+data["z"]**2)))
    tilt=tilt*180/math.pi
    return tilt #Value between -90 and 90degrees

def TestGyro():
    print('Fetching data from gyro')
    for i in range(200):
        print(get_Tilt())
        time.sleep(0.3)

while True:
    TestMotors()

