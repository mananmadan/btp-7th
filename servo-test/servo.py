import RPi.GPIO as GPIO
import time

class Servo:
 pin = 0
 def __init__(self,pinnumber):
    GPIO.setmode(GPIO.BOARD)
    self.pin = pinnumber
    # Set GPIO numbering mode
    GPIO.setup(self.pin,GPIO.OUT)
    self.pwm = GPIO.PWM(self.pin,50) # Note 11 is pin, 50 = 50Hz pulse

 def SetAngle(self,angle):
    duty = angle / 18 + 2
    print("Pin",self.pin)
    print("Duty",duty)
    self.pwm.start(0)
    self.pwm.ChangeDutyCycle(duty)
    time.sleep(1)
    self.pwm.ChangeDutyCycle(0)