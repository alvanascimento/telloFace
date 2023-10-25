from utils import *
import cv2
from time import time

W       = 640
H       = 360
drone   = iniDrone()
relogio = time()

while True:
    # Camera do Drone
    camera = drone.get_frame_read()
    frame = camera.frame
    
    # Camera do notebook
    # camera = cv2.VideoCapture(0)
    # _, frame = camera.read()
    
    img = cv2.resize(frame, (W,H))
    img, bbox = findFace(img)
    cv2.imshow("Drone", img)
    if bbox:
        relogio = time()
        trackFace(drone, bbox, W, H)
    else:
        if relogio and (time()-relogio) > 2:
            relogio = None 
            drone.send_rc_control(0, 0, 0, 0)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        drone.land()
        break
