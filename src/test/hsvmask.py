import numpy as np
import cv2
from time import sleep

#create lower and upper thresh for green in image
lower_green = np.array([20, 10, 10])
upper_green = np.array([40, 240, 240])

lower_red_low = np.array([0, 50, 50])
upper_red_low = np.array([10, 255, 255])
lower_red_high = np.array([170, 50, 50])
upper_red_high = np.array([180, 255, 255])

def bounding_box_for_largest_cnt(frame, mask):
    image, contours, hierarchy  = cv2.findContours(mask.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    biggest_contour = sorted(contours, key=cv2.contourArea, reverse=True)[:1]
    if len(biggest_contour) > 0:
        rect = cv2.minAreaRect(biggest_contour[0])
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        return box
    return False

def main():
    #get cap obj
    cap = cv2.VideoCapture(0)
    while(True):
        ret,frame = cap.read()
        frame = cv2.flip(frame, 1)#horizontal flip

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        #apply threshold
        green_mask = cv2.inRange(hsv, lower_green, upper_green)
        red_mask_low = cv2.inRange(hsv, lower_red_low, upper_red_low)
        red_mask_high = cv2.inRange(hsv, lower_red_high, upper_red_high)
        red_mask = cv2.bitwise_or(red_mask_low, red_mask_high)
        
        red_box = bounding_box_for_largest_cnt(frame, red_mask)
        green_box = bounding_box_for_largest_cnt(frame, green_mask)
       
        if red_box is not False and green_box is not False:
            cv2.drawContours(frame, [red_box], 0, (0, 255, 0), 1)
            cv2.drawContours(frame, [green_box], 0, (0, 0, 255), 1)

        #figure out bounding box and draw on frame
        cv2.imshow('frame', frame)
        cv2.imshow('red_mask', red_mask)
        cv2.imshow('green_mask', green_mask)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
