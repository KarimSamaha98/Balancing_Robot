
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
    if speed != 0:
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
        time.sleep((6.25*10**-5)+T)
        GPIO.output(CLK_M1,GPIO.LOW)
        GPIO.output(CLK_M2,GPIO.LOW)

def move_backward(speed):
    #Find the residual delay
    if speed != 0:
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
        time.sleep(6.25*10**-5+T)
        GPIO.output(CLK_M1,GPIO.LOW)
        GPIO.output(CLK_M2,GPIO.LOW)


if __name__ == "__main__":
    from RpiMotorLib import RpiMotorLib
    Motor1 = RpiMotorLib.TB6612FNGDc()
    for i in range (1000):
        for  j in range(10):
            GPIO.output(CW_M2,GPIO.HIGH)
            GPIO.output(CW_M1,GPIO.LOW)
            time.sleep((6.25*10**-5))
            GPIO.output(CLK_M1,GPIO.HIGH)
            GPIO.output(CLK_M2,GPIO.HIGH)
            time.sleep((6.25*10**-5))
            GPIO.output(CLK_M1,GPIO.LOW)
            GPIO.output(CLK_M2,GPIO.LOW)
        #time.sleep(0.007)