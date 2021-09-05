# Import libraries
import RPi.GPIO as GPIO
import time

# Set GPIO numbering mode
GPIO.setmode(GPIO.BOARD)

# Set pin 11 as an output, and set servo1 as pin 11 as PWM
GPIO.setup(12,GPIO.OUT)
servo1 = GPIO.PWM(12,50) # Note 11 is pin, 50 = 50Hz pulse

#start PWM running, but with value of 0 (pulse off)
servo1.start(0)
print ("Waiting for 2 seconds")
time.sleep(2)

#Let's move the servo!
print ("Rotating 180 degrees in 10 steps")

# Define variable duty
duty = 0

# Loop for duty values from 2 to 12 (0 to 180 degrees)
while True:
 while duty <= 8:
        servo1.ChangeDutyCycle(duty)
        time.sleep(0.1)
        duty = duty + 1

 while duty >= 1:
        servo1.ChangeDutyCycle(duty)
        time.sleep(0.1)
        duty = duty - 1
 
servo1.ChangeDutyCycle(1)
time.sleep(1)
