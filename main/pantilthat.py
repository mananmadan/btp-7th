## change this file according to the algo required

## Thoughts on the algo!
'''
- let's say current angle is 60 (which is for eg val 4-5 in servopwm)
- now if error is -ve .. 4-5 will change to 6,7,8,9 ... 12 depending upon the magnitude of error
- if error is +ve .. 4-5 will change to 3,2,1 .. depending upon the magnitude of error
'''
'''
- Current Implementation
 - if error is neg.. make servopwm less by 0.5
 - if error is pos .. make servopwm more by 0.5
'''

#import RPi.GPIO as GPIO
import time


def servo_enable(pin,val):
    '''
    ## code for servo enable false or true
    # Set GPIO numbering mode
    GPIO.setmode(GPIO.BOARD)

    # Set pin 11 as an output, and set servo1 as pin 11 as PWM
    GPIO.setup(11,GPIO.OUT)
    GPIO.setup(12,GPIO.OUT)
    '''
    print("servo enable",pin,val)

def publish(pin,val):
    '''
    servo=GPIO.PWM(pin,50)
    servo.start(0)
    ## code for publishing max value
    '''
    print("Publish",pin,val)

def pan(arg1,cp):                                              
    print("pan angle",arg1)
    if arg1 < 0:
        print("Neg")
        if cp < 12.0:
            cp = cp + 0.5
    if arg1 > 0:
        if cp > 0.0:
            cp = cp - 0.5
        print("Pos")
    print("cp:",cp)
    publish(11,cp) ## publish val on pan pin
    return cp

def tilt(arg1,ct):
    print("tilt angle",arg1)
    if arg1 < 0:
        print("Neg")
        if ct < 12.0:
            ct = ct + 0.5
    if arg1 > 0:
        if ct > 0.0:
            ct = ct - 0.5
        print("Pos")
    print("ct:",ct)
    publish(12,ct) ## publish val on tilt pin
    return ct