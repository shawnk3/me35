##image processing code iteration 1.

from random import randint
from time import sleep
from buildhat import Motor
import cv2
import sys
from flask import Flask, render_template, Response
from webcamvideostream import WebcamVideoStream
from flask_basicauth import BasicAuth
import time
import threading
from skimage.metrics import structural_similarity as compare_ssim
import imutils

## Import custom Onshape library of functions
from OnshapePlus import *
## Import any necessary libraries for buildhat
print("importing buildhat libraries...")
from buildhat import Motor, DistanceSensor,ForceSensor,ColorSensor, MotorPair

from onshape_client.client import Client
from onshape_client.onshape_url import OnshapeElement
import json

import numpy as np
import matplotlib.pyplot as plt
## Best practice is to add you API keys and base URL to a separate file named "apikeys.py" in the folder
# try:
#     exec(open('/home/pi/fun-stuff/me35/apikeys.py').read())
#     try:
#         print("Base URL defined as " + base)
#     except:
#         print("Base URL not specified, defaulting to https://cad.onshape.com")
#         base = 'https://cad.onshape.com'
#     client = Client(configuration={"base_url": base,
#                                 "access_key": access,
#                                 "secret_key": secret})
#     print('Onshape client configured')

# ## If keys are not in separate file, you can input them directly here, but make sure you never share this file
# except:
#     access = "<access key>"
#     secret = "<secret key>"
#     base = "https://cad.onshape.com" ## Change base url if working in an enterprise
#     client = Client(configuration={"base_url": base,
#                                 "access_key": access,
#                                 "secret_key": secret})
#     print('Onshape client configured')


# print("---------------------TOOTHPASTE------------------------")

# url = 'https://rogers.onshape.com/documents/3c57a9ed71ef9764af978718/w/5071b877874272a8c32e15a6/e/e814809deb99e01b4ac44682' #@param {type:"string"}
# showResponse = False #@param {type:"boolean"}
# listParts = True #@param {type:"boolean"}
# def getPartsInPartStudio(url: str):
#   fixed_url = '/api/parts/d/did/w/wid/e/eid/'

#   element = OnshapeElement(url)
#   fixed_url = fixed_url.replace('did', element.did)
#   fixed_url = fixed_url.replace('wid', element.wvmid)
#   fixed_url = fixed_url.replace('eid', element.eid)

#   method = 'GET'

#   params = {}
#   payload = {}
#   headers = {'Accept': 'application/vnd.onshape.v1+json; charset=UTF-8;qs=0.1',
#             'Content-Type': 'application/json'}

#   response = client.api_client.request(method, url=base + fixed_url, query_params=params, headers=headers, body=payload)

#   parsed = json.loads(response.data)
#   # The command below prints the entire JSON response from Onshape
#   # print(json.dumps(parsed, indent=4, sort_keys=True))
#   return parsed

# partResponse = getPartsInPartStudio(url)
# if showResponse:
#   print(json.dumps(partResponse, indent=4, sort_keys=True))
# if listParts:
#   for i in range(len(partResponse)):
#     print(partResponse[i]["name"] +" has part ID: "+ partResponse[i]["partId"])
# else:
#   pass

# #@title Get Mass Properties of Parts in a Part Studio
# #@markdown Defines function `getMassProp(url: str, partId="", config="")`, which returns JSON of mass properties for all parts in a part studio
# url = 'https://rogers.onshape.com/documents/3c57a9ed71ef9764af978718/w/5071b877874272a8c32e15a6/e/e814809deb99e01b4ac44682' #@param {type:"string"}
# config = 'squeezeDistance%3D0.01%2Bmillimeter' #@param {type:"string"}
# partId = 'JZH' #@param {type:"string"}
# showResponse = True #@param {type:"boolean"}

# def getMassProp(url: str, partId="", config=""):
#   fixed_url = '/api/partstudios/d/did/w/wid/e/eid/massproperties'
#   element = OnshapeElement(url)
#   method = 'GET'

#   params = {}
#   if partId != "":
#     params['partId'] = partId
#   if config != "":
#     params['configuration'] = config
    
#   payload = {}
#   headers = {'Accept': 'application/vnd.onshape.v2+json; charset=UTF-8;qs=0.1',
#             'Content-Type': 'application/json'}

#   fixed_url = fixed_url.replace('did', element.did)
#   fixed_url = fixed_url.replace('wid', element.wvmid)
#   fixed_url = fixed_url.replace('eid', element.eid)

#   response = client.api_client.request(method, url=base + fixed_url, query_params=params, headers=headers, body=payload)

#   parsed = json.loads(response.data)
#   return parsed
# if showResponse:
#   massProp = getMassProp(url,partId,config)
#   print(json.dumps(massProp, indent=4, sort_keys=True))
# else:
#   pass

# #REMAINING TOOTHPASTE.


# plt.style.use('seaborn-whitegrid')

# url = "https://rogers.onshape.com/documents/3c57a9ed71ef9764af978718/w/5071b877874272a8c32e15a6/e/e814809deb99e01b4ac44682"

# squeezeDistances = np.linspace(0.01,0.055,5)
# configDef = 'squeezeDistance%3D{}%2Bmillimeter'
# volumes = []
# for x in squeezeDistances:
#   try:
#     configuration = configDef.format(str(x))
#     massProp = getMassProp(url,"JZH",configuration)
#     volumes.append(massProp['bodies']['-all-']['volume'][0])
#   except:
#     print(x)
#     print('error')


# print("VOLUMES: ", volumes)
# print("squeeze:", squeezeDistances)

# plt.plot(squeezeDistances, volumes, 'o', color='black');

# x = np.array(squeezeDistances)
# y = np.array(volumes)
# X = x - x.mean()
# Y = y - y.mean()

# slope = (X.dot(Y)) / (X.dot(X))
# print("slope = "+str(slope)+" squeeze distance / volume")

# TOTAL_VOLUME =  15909 #in mm^3
# SQUEEZE =  9.4 #in mm

# VOLUME_OUT =  SQUEEZE/abs(slope) # volume of toothpaste coming out.

# numOfSqueezes = TOTAL_VOLUME/VOLUME_OUT #number of times can squeeze toothpaste out of tube

# print("NUM OF SQUEEZES:" , numOfSqueezes)

# print("-------------------------------ROBOT ASSEMBLY------------------------")

# ## Change URL to be your Assemelby
# url = "https://rogers.onshape.com/documents/3c57a9ed71ef9764af978718/w/5071b877874272a8c32e15a6/e/3d18c092ee13d63b876188d3"

# ## What is the name of the mate you want to use to control a motor?
# controlMate = 'CONTROL'

# mates = getMates(client,url,base)
# for names in mates['mateValues']:
#     print(names['mateName'])


##VIDEO CAMERA CODE    
# app = Flask(__name__)

# haar_face = cv2.CascadeClassifier('facecascade.xml')
# smile = cv2.CascadeClassifier('smile.xml')


# @app.route('/')
# def index():
#     return render_template('index.html')

# def gen(camera):
#     while True:
#         if camera.stopped:
#             break
#         frame = camera.read()
#         gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
#         faces = haar_face.detectMultiScale(gray, scaleFactor = 1.3, minNeighbors = 7)
#         for (x,y,w,h) in faces:
#             cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)
#             roi_gray = gray[y:y+h,x:x+w]
#             roi_color = frame[y:y+h,x:x+w]
#             smiles = smile.detectMultiScale(roi_gray,scaleFactor = 1.1, minNeighbors = 30)
#             if len(smiles) > 0: 
#                 for (ex,ey,ew,eh) in smiles:
#                     cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
#                     cv2.rectangle(roi_color,(ex,ey),(ex + ew, ey+eh), (0,255,0),2)
#                     cv2.putText(frame, "HAPPY", (x,y-10),cv2.FONT_HERSHEY_SIMPLEX,0.9,(35,255,12),3)
#             else:
#                 cv2.putText(frame, "SAD", (x,y-10),cv2.FONT_HERSHEY_SIMPLEX,0.9,(35,12,255),3)
#         ret, jpeg = cv2.imencode('.jpg',frame)
        

# @app.route('/video_feed')
# def video_feed():
#     return Response(gen(WebcamVideoStream().start()),
#                     mimetype='multipart/x-mixed-replace; boundary=frame')

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', debug=True, threaded=True)


# # ## Chage sensor port if different and make sure you are using the correct sensor code for buildhat
motor = Motor('A')
# motor = MotorPair('A','C')
btn = ForceSensor('B')
# dist = DistanceSensor('C')
motor2 = Motor('D')


cam = cv2.VideoCapture(0)
ret,frame = cam.read()

# cascade = cv2.CascadeClassifier('toothbrush.xml')
# cv2.imwrite("/home/pi/fun-stuff/me35/test3.jpg", frame)
# img = cv2.imread("/home/pi/fun-stuff/me35/test3.jpg")

# resized = cv2.resize(img,(400,200))
# gray=cv2.cvtColor(resized,cv2.COLOR_BGR2GRAY)
# faces=cascade.detectMultiScale(gray,1.3,4)
# for(x,y,w,h) in faces:
#     resized=cv2.rectangle(resized,(x,y),(x+w,y+h),(0,255,0),2)

# cv2.imwrite("/home/pi/fun-stuff/me35/test3.jpg", resized)


count = 0
while True:
        count +=1
        cv2.imwrite("/home/pi/fun-stuff/me35/dataset/n/User-"+ str(count) + ".jpg", frame)
        cv2.imwrite("/home/pi/fun-stuff/me35/test3.jpg", frame)
        ch = cv2.waitKey(100)
        if ch& 0xFF == ord('q'):
          break
        elif count >=100:
          break

# og = cv2.imread("/home/pi/fun-stuff/me35/test.jpg")
# og2 = cv2.cv2.imread("/home/pi/fun-stuff/me35/test2.jpg")
# base = cv2.imread("/home/pi/fun-stuff/me35/test3.jpg", frame)


# hsv_base = cv.cvtColor(base, cv2.COLOR_BGR2HSV)
# hsv_test1 = cv.cvtColor(og, cv2.COLOR_BGR2HSV)
# hsv_test2 = cv.cvtColor(og2, cv2.COLOR_BGR2HSV)

  

# # def get_mates(mates,search):
# #     for names in mates['mateValues']:
# #             if names['mateName'] == controlMate:
# #                 ## Modify the translate to map range of Onshape mate values to motor control value
# #                 print("mate value = "+str(names['rotationZ']))
# #                 if names['jsonType'] == "Revolute":
# #                     print("names['jsonType'] == 'Revolute'")
# #                     pos = math.floor(translate(names['rotationZ'],0,math.pi,0,180))


# while True:
#     if btn.is_pressed():
#         motor2.run_for_degrees(-90)
    # mea = dist.get_distance()
    # print("toothbrush distance:", dist.get_distance())

    # mates = getMates(client,url,base)
    # for names in mates['mateValues']:
    #         if names['mateName'] == controlMate:
    #             ## Modify the translate to map range of Onshape mate values to motor control value
    #             print("mate value = "+str(names['rotationZ']))
    #             if names['jsonType'] == "Revolute":
    #                 print("names['jsonType'] == 'Revolute'")
    #                 pos = math.floor(translate(names['rotationZ'],0,math.pi,0,180))

    
    # if(mea < 50 and mea > 0):
    #     print("BRUSH DETECTED!")
    #     # for i in range(10):
    #     # motor.run_for_rotations(2,80)
    #     #   # motor.run_for_rotations(1,-80)
    #     #   # motor.run_for_rotations(1,80)
    #     time.sleep(5)
    #     # ret,frame = cam.read()

    #     # cv2.imwrite("/home/pi/fun-stuff/me35/test.jpg", frame)
        
    #     motor2.run_for_degrees(180)
        
    # motor.run_for_rotations( pos*0.0028 ,-20)
    # motor.run_for_rotations(pos*0.0028 ,20)

    
# # print("color is: ", sen.get_color())
