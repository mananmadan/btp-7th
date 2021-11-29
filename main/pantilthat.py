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
import RPi.GPIO as GPIO
import pigpio
import config
servoh = 17
servov = 18
pwm = pigpio.pi() 



def movehservopositiveh(servo,servoto):
    print("-->>",config.servocurh,servoto)
    while config.servocurh<servoto and config.servocurh<2480:
        pwm.set_servo_pulsewidth( servo, config.servocurh )
        config.servocurh=config.servocurh+11
        time.sleep(0.1)

def movehservonegativeh(servo,servoto):
    print("--<<",config.servocurh,servoto)
    while config.servocurh>servoto and config.servocurh>515:
        pwm.set_servo_pulsewidth( servo, config.servocurh )
        config.servocurh=config.servocurh-11
        time.sleep(0.1)
        
        
def movehservopositivev(servo,servoto):
    print("--<<",config.servocurv,servoto)
    while config.servocurv<servoto and config.servocurv <2480:
        pwm.set_servo_pulsewidth( servo, config.servocurv )
        config.servocurv=config.servocurv+15
        time.sleep(1)

    
def movehservonegativev(servo,servoto):
    print("--<<",config.servocurv,servoto)
    while config.servocurv>servoto and config.servocurv>1200:
        pwm.set_servo_pulsewidth( servo, config.servocurv )
        config.servocurv=config.servocurv-15
        time.sleep(1)

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
    pwm.set_mode(servoh, pigpio.OUTPUT) 
    pwm.set_mode(servov, pigpio.OUTPUT) 
    
    pwm.set_PWM_frequency(servoh, 50 )
    pwm.set_PWM_frequency(servov, 50 )
    pwm.set_servo_pulsewidth( servoh, config.servocurh)
    pwm.set_servo_pulsewidth( servov, config.servocurv )
    
def publish(pin,val):
    '''
    servo=GPIO.PWM(pin,50)
    servo.start(0)
    ## code for publishing max value
    '''
    #print("Publish",pin,val)
    temp=val*104.16 +500
    if pin == servoh:
        if temp> config.servocurh:
            movehservopositiveh(pin,temp)
        else:
            movehservonegativeh(pin,temp)
    
    else:
        if temp> config.servocurv:
            movehservopositivev(pin,temp)
        
        else:
            movehservonegativev(pin,temp)
         
def pan(arg1,cp,x):                                              
    #print("pan angle",arg1,cp)
    
    if arg1 > 0:
        #print("Neg")
        if cp < 12.0:
            cp = cp + 0.5
    if arg1 < 0:
        if cp > 0.0:
            cp = cp - 0.5
        #print("Pos")
    #print("cp:",cp)
    #print(config.top)
    #if x:
    publish(servoh,cp) ## publish val on pan pin
    return cp

def tilt(arg1,ct,x):
    #print("tilt angle",arg1,ct)
    if arg1 < 0:
        #print("Neg")
        if ct < 12.0:
            ct = ct + 0.5
    if arg1 > 0:
        if ct > 0.0:
            ct = ct - 0.5
        #print("Pos")
    #print("ct:",ct)
    
    #print("Toooooooop",top)
    publish(servov,ct) ## publish val on tilt pin
    return ct