import numpy as np
import cv2
from cubestate import CubeState
import vision

cap = cv2.VideoCapture(0)
while(True):
    #read and flip frame
    ret,frame = cap.read()
    frame = cv2.flip(frame, 1)#horizontal flip

    green_mask, red_mask = vision.apply_thresholds(frame)
    green_box, red_box = vision.get_boxes(frame, green_mask, red_mask)

    vision.draw_boxes(frame, green_box, red_box)

    cv2.imshow('frame', frame)
    cv2.imshow('red_mask', red_mask)
    cv2.imshow('green_mask', green_mask)
    print(vision.get_x())

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()

