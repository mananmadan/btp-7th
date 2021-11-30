#!/usr/bin/python3
import RPi.GPIO as GPIO
import pigpio
import time
 
#servo = 17 # horizontal
servo = 18 # vertical
# more info at http://abyz.me.uk/rpi/pigpio/python.html#set_servo_pulsewidth
 
pwm = pigpio.pi() 
pwm.set_mode(servo, pigpio.OUTPUT)
 
pwm.set_PWM_frequency(servo, 50 )
i=500
while i <1600:
    pwm.set_servo_pulsewidth( servo, i ) ;
    i+=11
    time.sleep(0.1)
#print( "0 deg" )
#pwm.set_servo_pulsewidth( servo, 500 ) ;
#time.sleep( 3 )
 
# turning off servo
pwm.set_PWM_dutycycle(servo, 0)
pwm.set_PWM_frequency( servo, 0 )