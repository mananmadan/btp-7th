import RPi.GPIO as GPIO
import time

class Servo:
        pin = 0
        def __init__(self,pinnumber):
            self.pin = pinnumber
            # Set GPIO numbering mode
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(self.pin,GPIO.OUT)
            self.pwm = GPIO.PWM(self.pin,50) # Note 11 is pin, 50 = 50Hz pulse

        def SetAngle(self,angle):
	        duty = angle / 18 + 2
            print("Duty",duty)
	        GPIO.output(self.pin, True)
	        self.pwm.ChangeDutyCycle(duty)
	        time.sleep(1)
	        GPIO.output(self.pin, False)
