import numpy as np
import cv2
from time import sleep
import cubestate

#create lower and upper thresh for green in image
lower_green = np.array([40, 0, 0])
upper_green = np.array([120, 255, 255])

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


def get_z():
    """Calculates cube x-coord based on current pointer angle."""
    angle = smooth_angle(current_pointer_angle)
    if angle >= -20 and angle <= 0:
        z = 0
    elif angle >= -40 and angle < -20:
        z = 1
    elif angle >= -50 and angle < -40:
        z = 2
    elif angle >= -80:
        z = 3
    else:
        z = -1
    return z

def smooth_angle(angle):
    """Returns the smoothed version of angle by moving average"""
    global pointer_angles
    global pointer_angle_index

    pointer_angles.itemset(pointer_angle_index % pointer_angles.size, angle)
        
    angle = np.average(pointer_angles)
    pointer_angle_index += 1

    return angle

def z(z_coord):
    """returns the coords for entire z plane specified by z_coord"""
    coords = []
    for x in range(0,4):
        for y in range(0,4):
            coords.append((x,y,z_coord))
    return coords
    
def run(cs,delay):
    #get cap obj
    cap = cv2.VideoCapture(0)
    try:
        while True:
            ret,frame = cap.read()
            frame = cv2.flip(frame, 1)#horizontal flip

            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            #apply threshold
            green_mask = cv2.inRange(hsv, lower_green, upper_green)
            
            green_box = bounding_box_for_largest_cnt(frame, green_mask, True)
           
            if green_box is not False:
                cv2.drawContours(frame, [green_box], 0, (0, 0, 255), 1)
                cs.update(coords=z(get_z()))
                cs.send()
    
            #figure out bounding box and draw on frame
            cv2.imshow('frame', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            sleep(delay)
    except KeyboardInterrupt:
        pass
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    cs = cubestate.CubeState("/dev/ttyUSB0", exp_time=-1)
    run(cs, .033)
