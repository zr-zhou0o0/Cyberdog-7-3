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
from .move_x import move_x_aim_ball

def main():
    # move_x_aim_ball(mode=1)
    location = Location()
    location.get_data()
    print(location.ball)

