import numpy as np
import cv2
from time import sleep

#create lower and upper thresh for green in image
lower_green = np.array([60, 100, 100])
upper_green = np.array([100, 255, 255])

lower_red_low = np.array([0, 50, 50])
upper_red_low = np.array([10, 255, 255])
lower_red_high = np.array([170, 50, 50])
upper_red_high = np.array([180, 255, 255])

pointer_angles = np.zeros(10) #keep track of ten most recent angles of pointer object
pointer_angle_index = 0 #current place in above arr
current_pointer_angle = -90

def bounding_box_for_largest_cnt(frame, mask, isPointer=False):
    """Returns the bounding box (minAreaRect) for largest contour in given mask. If isPointer is True, also sets current_pointer_angle to the angle of the bounding box."""
    global current_pointer_angle

    image, contours, hierarchy  = cv2.findContours(mask.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    biggest_contour = sorted(contours, key=cv2.contourArea, reverse=True)[:1]
    if len(biggest_contour) > 0:
        rect = cv2.minAreaRect(biggest_contour[0])
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        if isPointer:
            current_pointer_angle = rect[2]#rect[2] is angle
        return box 
    if isPointer:
        current_pointer_angle = -90
    return False


def apply_thresholds(frame):
    """Applies HSV masks to frame and returns a tuple (green_mask, red_mask). Expects frame to be in BGR colorspace"""

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    green_mask = cv2.inRange(hsv, lower_green, upper_green)
    red_mask_low = cv2.inRange(hsv, lower_red_low, upper_red_low)
    red_mask_high = cv2.inRange(hsv, lower_red_high, upper_red_high)
    red_mask = cv2.bitwise_or(red_mask_low, red_mask_high)

    return (green_mask, red_mask)

def get_boxes(frame, green_mask, red_mask):
    """green_mask, red_mask: values returned from apply_thresholds
       Returns a tuple (green_box, red_box) with the bounding box for largest
       contours in green_mask and red_mask, respectively. Assumes green_mask is mask for pointer object."""
    red_box = bounding_box_for_largest_cnt(frame, red_mask)
    green_box = bounding_box_for_largest_cnt(frame, green_mask, isPointer=True)
    
    return (green_box, red_box)

def draw_boxes(frame, green_box, red_box):
    """Draws green_box and red_box onto frame. red_box is drawn in green and green_box is drawn in red. This is because red_box should be surrounding somehting red, and green_box should be surrounding something green."""
    if red_box is not False:
        cv2.drawContours(frame, [red_box], 0, (0, 255, 0), 1)
    if green_box is not False:
        cv2.drawContours(frame, [green_box], 0, (0, 0, 255), 1)


def get_x():
    """Calculates cube x-coord based on current pointer angle."""
    angle = smooth_angle(current_pointer_angle)
    if angle >= -20 and angle <= 0:
        x = 0
    elif angle >= -40 and angle < -20:
        x = 1
    elif angle >= -50 and angle < -40:
        x = 2
    elif angle >= -80:
        x = 3
    else:
        x = -1
    return x

def smooth_angle(angle):
    """Returns the smoothed version of angle by moving average"""
    global pointer_angles
    global pointer_angle_index

    pointer_angles.itemset(pointer_angle_index % pointer_angles.size, angle)
        
    angle = np.average(pointer_angles)
    pointer_angle_index += 1

    return angle
    
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
