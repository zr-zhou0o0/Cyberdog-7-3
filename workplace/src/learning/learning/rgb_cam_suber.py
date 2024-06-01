#---get rgb image from stereo camera---#
'''
>   author: all
>   rgb_cam_suber.py
>   define a class rgb_cam_suber(Node)
    with attributes:
        - bridge: CvBridge
        - sub: subscription to '/image_rgb'
        - frame_count: int
        - size: int
        - ball_position: tuple (float)
        - contour: list of numpy arrays, each array is a contour of the green area in image
        - size: the area of the biggest green area (when area < 100, assume that there's no green object in view, and ball position is set (0,0))
    note:
        - boundrect return the point in the left top!!!!! and the y coord is upside down!
        - size of front cam: 480 * 640


'''

import cv2
import numpy as np
from cv_bridge import CvBridge
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image

class RGBCamSuber(Node):
    '''subscribe the message of stereo camera'''
    def __init__(self, name) -> None:
        super().__init__(name)
        self.bridge = CvBridge()
        self.declare_parameter("dog_name", "az2")
        self.sub = self.create_subscription(Image, '/image_rgb', self.sub_callback, 10)
        self.frame_count = 0

        self.ball_position = (320, 0)
        
        self.size = 0

        self.sizec = 0
        self.r = 0

        self.sizer = 0
        self.xr = 0
        self.yr = 0
        self.h = 0
        self.w = 0

        self.ratio = 0
        

    def sub_callback(self, msg: Image):
        '''the callback function of subscriber'''
        rgb_msg = msg
        cv_image = self.bridge.imgmsg_to_cv2(rgb_msg, "bgr8")

        hsv = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)

        lower_green = np.array([35, 43, 46])
        upper_green = np.array([77, 255, 255])

        mask = cv2.inRange(hsv, lower_green, upper_green)

        _, contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            largest_contour = max(contours, key=cv2.contourArea)

            ((x, y), radius) = cv2.minEnclosingCircle(largest_contour)
            cv2.circle(cv_image, (int(x), int(y)), int(radius), (0, 255, 255), 2)

            x_r, y_r, width, height = cv2.boundingRect(largest_contour)    
            cv2.rectangle(cv_image, (x_r, y_r), (x_r+width, y_r+height), (255, 0, 0), 3) # in blue, with thickness 3

            self.ball_position = (x, y)
            self.size = cv2.contourArea(largest_contour)
            self.sizec = 3.14 * radius * radius
            self.r = radius
            self.sizer = width * height
            self.xr = x_r
            self.yr = y_r
            self.h = height
            self.w = width
            self.ratio = height/width
            
            
        if self.size <100:
            x,y = 320, 0
            self.ball_position = (x, y)
            self.sizec = 0
            self.r = 0
            self.sizer = 0
            self.xr = 0
            self.yr = 0
            self.h = 0
            self.w = 0
            self.ratio = 0
        
        print("x={},y={},size={},sizec={},siezr={}".format(self.ball_position[0],self.ball_position[1],self.size,self.sizec,self.sizer))
        # print("ratio={},h={},r={}".format(self.ratio,self.h,self.r))
        # print("xr={},yr={}".format(self.xr,self.yr))
        # print("yr+h={}".format(self.yr + self.h))

        # cv2.imshow("rgb_image", cv_image)
        # cv2.waitKey(1) ###########

def main(args=None):
    rclpy.init()
    rgb_cam_suber = RGBCamSuber("rgb_cam_suber")
    rclpy.spin(rgb_cam_suber)
    try:
        while True:
            pass
    except exception:
        print('exception')
    rgb_cam_suber.destroy_node()
    rclpy.shutdown()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
