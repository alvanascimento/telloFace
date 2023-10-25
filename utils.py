from djitellopy import Tello
import cv2
# from ultralytics import YOLO
import numpy as np

def iniDrone():
    myDrone = Tello()
    myDrone.connect()
    print("Bateria:", myDrone.get_battery())
    print("Temperatura:", myDrone.get_temperature())
    myDrone.streamoff()
    myDrone.streamon()
    myDrone.takeoff()
    return myDrone

# Tacking face
def trackFace(drone, bbox, W, H):
    speedYaw = 50
    speedUD  = 60
    ruido    = 0.1
    (x, y, w, h) = bbox
    erroW = (x+w//2) - W//2
    erroH = (y+h//2) - H//2
    erroZ = int(((w*h//1000) - 10) * -1)
    yaw = int(np.interp(erroW, [-W//2,W//2], [-speedYaw, speedYaw]))
    if abs(yaw) < speedYaw*ruido: yaw = 0
    ud  = int(np.interp(erroH, [-H//2,H//2], [speedUD, -speedUD]))
    if abs(ud) < speedUD*ruido: ud = 0
    print(bbox)
    # print("L/R:", 0)
    print("F/B:", erroZ)
    print("U/D:", ud)
    print("Yaw:", yaw)
    drone.send_rc_control(0, erroZ, ud, yaw)
    print("Bateria:", drone.get_battery())
    print("Temperatura:", drone.get_temperature())

# Find face by HAAR Cascade
def findFace(img):
    faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(imgGray, 1.2, 4)
    maiorArea = 0
    bbox = None
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x,y), (x+w, y+h), (255, 0, 0), 2)
        area = w * h
        if area > maiorArea:
            maiorArea = area
            bbox = (x, y, w, h)
    return img, bbox

# Find face by Yolo8
# def findFace(img):
#     model = YOLO("best.pt")
#     results = model(img)
#     boxes = results[0].boxes
#     for box in boxes:
#         x  = int(box.xyxy.tolist()[0][0])
#         y  = int(box.xyxy.tolist()[0][1])
#         xw = int(box.xyxy.tolist()[0][2])
#         yh = int(box.xyxy.tolist()[0][3])
#         cv2.rectangle(img, (x,y), (xw, yh), (255, 0, 0), 2)
#     return img
