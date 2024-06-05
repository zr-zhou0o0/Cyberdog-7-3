'''
>   author: zzr
>   side_cam
    with attributes:
        - sub: subscription to '?'
        - size: int  # size of the largest black area
        - tele_position: tuple (float)  # the center of the television
        - contours: list of numpy arrays, each array is a contour of the black area in image     
>   note:
        - **robustness**
        - UnboundLocalError: local variable 'i' referenced before assignment
        - IndexError: list index out of range
        - 0 is top and 480 is bottom
        - under the thresh is black, above is white
'''

import cv2
import numpy as np
import rclpy
from cv_bridge import CvBridge
from rclpy.node import Node
from sensor_msgs.msg import Image

class SideCamLeft(Node):
    def __init__(self, name) -> None:
        super().__init__(name)
        self.bridge = CvBridge()
        self.declare_parameter("dog_name", "az2")
        self.sub = self.create_subscription(Image, '/image_left', self.sub_callback, 10)
        self.size = 0
        self.size_all = 0
        self.size_all_rec = [.0,.0,.0]
        self.tele_position = (0.0, 0.0)

    def sub_callback(self, msg: Image):
        '''the callback function of subscriber'''
        depth_msg = msg
        # cv_image_org = self.bridge.imgmsg_to_cv2(depth_msg, "bgr8")
        cv_image = self.bridge.imgmsg_to_cv2(depth_msg, "bgr8")

        # divide the image
        # cv_image = cv_image_org[60:130, : ]

        # gaussian blur
        cv_image = cv2.GaussianBlur(cv_image, (5, 5), 10)  

        # process the image format with inverse color (only the white items could be find!)
        imgray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
        _, thresholded = cv2.threshold(src=imgray, thresh=100, maxval=255, type=cv2.THRESH_BINARY_INV) # thresholded: This is the thresholded image.
        cv2.imshow("thresholded", thresholded)

        # draw contours
        _, contours, _ = cv2.findContours(thresholded, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) # image, contours, hierarchy
        cv2.drawContours(cv_image, contours, -1, (0, 255, 0), 3) # in green, with thickness 3

        # find the largest contour and calculate all contours' size
        # contours: list of contour, without idx
        # areas: list of tuple, idx of contour and size of contour. the idx equals to the areas'list's idx
        # a2: list of tuple, idx and size, sorted, descented
        areas = list() 
        self.size_all = 0
        for i, cnt in enumerate(contours):
            areas.append((i, cv2.contourArea(cnt)))  # size 
            self.size_all += cv2.contourArea(cnt)
        a2 = sorted(areas, key=lambda d: d[1], reverse=True)  

        # draw the first five contours and choose the one with largest size of rectangle
        # a3: list of tuple, idx and size of the rectangle, descented
        a3 = list()
        for j, (i, a) in enumerate(a2):
            if j<5:
                x, y, w, h = cv2.boundingRect(contours[i])
                cv2.rectangle(cv_image, (x, y), (x+w, y+h), (255, 0, 0), 7) # in blue, with thickness 7
                a3.append((j, i, w*h))
        a3 = sorted(a3, key=lambda d: d[2], reverse=True)

        # get bbox of the largest countour
        largest_contour = contours[a3[0][1]]
        cv2.drawContours(cv_image, contours, a3[0][1], (0, 0, 255), 5) # in red, with thickness 5

        x, y, w, h = cv2.boundingRect(largest_contour)
        cv2.rectangle(cv_image, (x, y), (x+w, y+h), (0, 0, 255), 7) # in red, with thickness 7

        # get average of the size in a period of time


        # get other figures
        self.size = cv2.contourArea(largest_contour)
        self.tele_position = (x+w/2, y+h/2)

        # debug log
        print("sizeall={}, size={}, tele_position={}".format(self.size_all, self.size, self.tele_position))

        cv2.imshow("depth_msg", cv_image)
        cv2.waitKey(1)



class SideCamRight(Node):
    def __init__(self, name) -> None:
        super().__init__(name)
        self.bridge = CvBridge()
        self.declare_parameter("dog_name", "az2")
        self.sub = self.create_subscription(Image, '/image_left', self.sub_callback, 10)
        self.size = 0
        self.size_all = 0
        self.size_all_rec = [.0,.0,.0]
        self.tele_position = (0.0, 0.0)

    def sub_callback(self, msg: Image):
        '''the callback function of subscriber'''
        depth_msg = msg
        # cv_image_org = self.bridge.imgmsg_to_cv2(depth_msg, "bgr8")
        cv_image = self.bridge.imgmsg_to_cv2(depth_msg, "bgr8")

        # divide the image
        # cv_image = cv_image_org[60:130, : ]

        # gaussian blur
        cv_image = cv2.GaussianBlur(cv_image, (5, 5), 10)  

        # process the image format with inverse color (only the white items could be find!)
        imgray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
        _, thresholded = cv2.threshold(src=imgray, thresh=100, maxval=255, type=cv2.THRESH_BINARY_INV) # thresholded: This is the thresholded image.
        cv2.imshow("thresholded", thresholded)

        # draw contours
        _, contours, _ = cv2.findContours(thresholded, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) # image, contours, hierarchy
        cv2.drawContours(cv_image, contours, -1, (0, 255, 0), 3) # in green, with thickness 3

        # find the largest contour and calculate all contours' size
        # contours: list of contour, without idx
        # areas: list of tuple, idx of contour and size of contour. the idx equals to the areas'list's idx
        # a2: list of tuple, idx and size, sorted, descented
        areas = list() 
        self.size_all = 0
        for i, cnt in enumerate(contours):
            areas.append((i, cv2.contourArea(cnt)))  # size 
            self.size_all += cv2.contourArea(cnt)
        a2 = sorted(areas, key=lambda d: d[1], reverse=True)  

        # draw the first five contours and choose the one with largest size of rectangle
        # a3: list of tuple, idx and size of the rectangle, descented
        a3 = list()
        for j, (i, a) in enumerate(a2):
            if j<5:
                x, y, w, h = cv2.boundingRect(contours[i])
                cv2.rectangle(cv_image, (x, y), (x+w, y+h), (255, 0, 0), 7) # in blue, with thickness 7
                a3.append((j, i, w*h))
        a3 = sorted(a3, key=lambda d: d[2], reverse=True)

        # get bbox of the largest countour
        largest_contour = contours[a3[0][1]]
        cv2.drawContours(cv_image, contours, a3[0][1], (0, 0, 255), 5) # in red, with thickness 5

        x, y, w, h = cv2.boundingRect(largest_contour)
        cv2.rectangle(cv_image, (x, y), (x+w, y+h), (0, 0, 255), 7) # in red, with thickness 7

        # get average of the size in a period of time


        # get other figures
        self.size = cv2.contourArea(largest_contour)
        self.tele_position = (x+w/2, y+h/2)

        # debug log
        print("sizeall={}, size={}, tele_position={}".format(self.size_all, self.size, self.tele_position))

        cv2.imshow("depth_msg", cv_image)
        cv2.waitKey(1)



def main(args=None):
    rclpy.init()
    side_cam_left = SideCamLeft("side_cam_left")
    side_cam_right = SideCamRight("side_cam_right")
    rclpy.spin(side_cam_left)
    rclpy.spin(side_cam_right)
    try:
        while True:
            pass
    except exception:
        print('exception')
    side_cam_left.destroy_node()
    side_cam_right.destroy_node()
    rclpy.shutdown()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
