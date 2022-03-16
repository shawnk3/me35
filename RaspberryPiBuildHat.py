## Import custom Onshape library of functions
from OnshapePlus import *
## Import any necessary libraries for buildhat
print("importing buildhat libraries...")
from buildhat import Motor, DistanceSensor,ForceSensor








##
## Config API Client
##

## Best practice is to add you API keys and base URL to a separate file named "apikeys.py" in the folder
try:
    exec(open('/home/pi/fun-stuff/me35/apikeys.py').read())
    try:
        print("Base URL defined as " + base)
    except:
        print("Base URL not specified, defaulting to https://cad.onshape.com")
        base = 'https://cad.onshape.com'
    client = Client(configuration={"base_url": base,
                                "access_key": access,
                                "secret_key": secret})
    print('Onshape client configured')

## If keys are not in separate file, you can input them directly here, but make sure you never share this file
except:
    access = "<access key>"
    secret = "<secret key>"
    base = "https://cad.onshape.com" ## Change base url if working in an enterprise
    client = Client(configuration={"base_url": base,
                                "access_key": access,
                                "secret_key": secret})
    print('Onshape client configured')

##
## define buildhat functions and params
##
def handle_motor(speed, pos, apos):
    print("Motor", speed, pos, apos)

def posControl(pos):
    motor.run_to_position(pos)

def speedControl(speed):
    motor.set_default_speed(speed)
    motor.start()

## Chage motor port if different or comment out if not using a motor
motor = Motor('A')
motor.set_default_speed(50)
btn = ForceSensor('B')
# motor.when_rotated = handle_motor ## unocomment to get read out whenever the motor moves

# ## Chage sensor port if different and make sure you are using the correct sensor code for buildhat
dist = DistanceSensor('C')


##
## Specify Onshape funcitons and parameters
##

## Change URL to be your Assemelby
url = "https://rogers.onshape.com/documents/3c57a9ed71ef9764af978718/w/5071b877874272a8c32e15a6/e/3d18c092ee13d63b876188d3"

## What is the name of the mate you want to use to control a motor?
controlMate = 'CONTROL'

mates = getMates(client,url,base)
for names in mates['mateValues']:
    print(names['mateName'])

pos = 0
posprev = 0
try:
    while True:
        ##
        ## The part where you control a motor with an Onshape Assembly Mate
        ##
        ## First get the mate value and map it to the value you really want
        mates = getMates(client,url,base)
        for names in mates['mateValues']:
            if names['mateName'] == controlMate:
                ## Modify the translate to map range of Onshape mate values to motor control value
                print("mate value = "+str(names['rotationZ']))
                if names['jsonType'] == "Revolute":
                    print("names['jsonType'] == 'Revolute'")
                    # pos = math.floor(translate(names['rotationZ'],0,math.pi,0,180))
                    pos = names['rotationZ']
                # if names['jsonType'] == "Slider":
                #     pos = math.floor(translate(names['translationZ'],0,math.pi,180,0))
                # elif names['jsonType'] == "Slider":
                #     pos = math.floor(translate(names['translationZ'],0,2,180,0))
        
        print("getMateValue = "+str(pos))

        print( "SD = : ", pos*0.0028)
        ## Send the value to the motor
        #posControl(pos%180) ## Bug - buildhat only supports values from -180 to 180 for send to position
        motor.run_for_rotations( pos*0.0028 ,-20)
        motor.run_for_rotations(pos*0.0028 ,20)
        # if(btn.is_pressed()):
        #     speedControl(speed=50)
        #     btn.wait_until_released()
        
        
        # # ##
        # # ## The part where you control an Onshape Assembly Mate with a sensor value
        # # ##
        # # ## Get sensor value from buildhat
        # # monitorValue = dist.get_distance()

        # # ## Look for mate name you want to control and set body of API request
        # for names in mates['mateValues']:
        #     if names['mateName'] == monitorMate:
        #         setMateJSON = names
        #         ## Modify the translate to map sensor values to Onshape mate values
        #         if names['jsonType'] == "Cylindrical":
        #             setMateJSON['rotationZ'] = translate(monitorValue,0,200,0,2*math.pi)
        #             print("setMateValue = "+str(translate(monitorValue,0,200,0,2*math.pi)))
        #         # elif names['jsonType'] == "Slider":
        #         #     setMateJSON['translationZ'] = translate(monitorValue,0,200,0,0.1)
        #         #     print("setMateValue = "+str(translate(monitorValue,0,200,0,0.1)))
        
        # ## Send to Onshape
        # setMates(client,url,base,{'mateValues':[setMateJSON]})

        time.sleep(1)
except KeyboardInterrupt:
    motor.stop()
    print('done')



