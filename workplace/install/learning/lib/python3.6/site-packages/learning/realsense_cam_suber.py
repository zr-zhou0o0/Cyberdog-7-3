'''
>   author: zzr
>   date: 2024-5-26
>   realsense_cam_suber.py
    with attributes:
        - sub: subscription to '/az2/camera/infra1/image_rect_raw'
        - size: int  # size of the largest black area
        - tele_position: tuple (float)  # the center of the television
        - contours: list of numpy arrays, each array is a contour of the green area in image     
'''

import cv2
import numpy as np
import rclpy
from cv_bridge import CvBridge
from rclpy.node import Node
from sensor_msgs.msg import Image

class RealsenseCamSuber(Node):
    def __init__(self, name) -> None:
        super().__init__(name)
        self.bridge = CvBridge()
        self.declare_parameter("dog_name", "az2")
        self.sub = self.create_subscription(Image, '/image_rgb', self.sub_callback, 10)
        # self.frame_count = 0
        self.size = 0
        self.tele_position = (0.0, 0.0)

    def sub_callback(self, msg: Image):
        '''the callback function of subscriber'''
        depth_msg = msg
        cv_image = self.bridge.imgmsg_to_cv2(depth_msg, "bgr8")

        _, thresholded = cv2.threshold(cv_image, 127, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(cv_image, contours, -1, (0, 0, 255), 3)

        largest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)
        cv2.rectangle(cv_image, (x, y), (x+w, y+h), (255, 0, 0), 2)

        self.size = cv2.contourArea(largest_contour)
        self.tele_position = (x+w/2, y+h/2)

        print("size={}, tele_position={}".format(self.size, self.tele_position))

        cv2.imshow("depth_msg", cv_image)

        cv2.waitKey(1)


def main(args=None):
    rclpy.init()
    realsense_cam_suber = RealsenseCamSuber("realsense_cam_suber")
    rclpy.spin(realsense_cam_suber)
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print('KeyBoardInterrupt')
    realsense_cam_suber.destroy_node()
    rclpy.shutdown()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
