from random import randint
from time import sleep
from buildhat import Motor

new_angle = randint(-180,180)
print(new_angle)

motor_y = Motor('A')
motor_y.run_to_position(90, 100)