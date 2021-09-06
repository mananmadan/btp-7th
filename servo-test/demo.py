from servo import Servo
import Rpi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
servo1 = Servo(11)
servo1.SetAngle(45)

servo2 = Servo(12)
servo2.SetAngle(45)