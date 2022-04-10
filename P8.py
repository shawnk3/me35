import RPi.GPIO as GPIO     
import time

in1 = 8 

GPIO.setmode(GPIO.BOARD)
GPIO.setup(in1,GPIO.OUT)


while True:
    GPIO.output(in1,GPIO.HIGH)
    time.sleep(.5)
    GPIO.output(in1, GPIO.LOW)
    time.sleep(.5)

