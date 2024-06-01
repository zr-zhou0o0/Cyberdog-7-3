'''
> keeper
> author: zzr
> ***scan***
> ***if in the range then we can decide the incline!!!!change the order!
> problem: jump of line in side_cam
> revise the intepret of all the classes, and move the readme to root, and highlight the essential algorithm in readme
> logic: the larger number suggest the higher priority
    mode 0 = left, 1 = right, -1 = none
   
        if dog out the range: move opposite, (stand at the boundary)
            no_line = 11 : pass
            back = 12 : move forth
            forth = 13 : move back
            boundary_lr = 14 : size out/ x out/or y out, move right or left, mode0=left boundary, mode1=...
        if dog in the range: decide the state 
            # if dog inclined: 
                # incline = 11, mode0=left_incline, mode1=right_incline
            if not:
                no_ball = 0: stand still

                far_mid = 1: move aim position
                clo_mid = 2: move aim direction

                far_border = 3: move aim position, mode0=left, mode1=...
                clo_border = 4: move aim direction, with xr or xr+width as x, mode0=left, mode1=...
                rush_border = 5: move aim position with high speed, mode0=left, mode1=...

                extclo_mid = 7: stand still or move slightly for 4~5 time
                extclo_corner = 8: rush, mode0=left, mode1=...

                # left = 9: rush
                # right = 10: rush

> modules:
    rgb_cam_suber: front camera 
        return the green ball's x, y, size(contour), sizec(circle), r(radius of cir), sizer(rect), xr, yr, h(height of rect), w(width of rect), ratio(h/w)
        logic: 
            if minenclosed rect's x or x+width nearly equals to (0, 480) or (640, 480): state 7 or 8
            if minenclosed rect's height >> minenclosed circle's diameter: state 2, 4, or 6
            else: dicide according to ball size

    side_cam: left camera and right camera(subscribe in the same class to utilize less resource)
        logic:
            angle and position:
                return (x_left + x_right)/2 as the x_bf(back and forth)
                if x_left >> x_right: left_incline (should rotate right)
                if x_right >> x_left: right_incline (should rotate left)
            ball and boundary:
                if the ball in sight: rush, state 9 or 10
                if not: return the height of the rect as the distance to boundary
> problems:
    what if the ball is hovering in front of the goal? how to push the ball out?

'''


import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Range
from protocol.msg import MotionServoCmd
import socket
import sys
import time
import cv2
from cv_bridge import CvBridge
import numpy as np

from .get_data import Location
from .move_horizontal import move_horizontal_aim_ball

def main():
    move_horizontal_aim_ball()


