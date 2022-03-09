from random import randint
from time import sleep
from buildhat import Motor



control = Motor('A')
# control.run_for_rotations(1,-60)
cmd = ''
while not(cmd =='q'):
    control.run_for_rotations(1,-80)
    control.run_for_rotations(1,80)
    # cmd = input("enter q to quit.")
    