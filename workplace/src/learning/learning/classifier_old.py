import cv2
from cv_bridge import CvBridge
import numpy as np
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image, Range
from protocol.msg import MotionServoCmd
import threading
import time

from .rgb_cam_suber import RGBCamSuber
from .side_cam import SideCamLeft
from .side_cam import SideCamRight

class Classifier(Node):
    def __init__(self, name, RGBCamSuber, SideCamLeft, SideCamRight):
        super().__init__(name)
        self.rgb_node = RGBCamSuber
        self.left_node = SideCamLeft
        self.right_node = SideCamRight
        self.dog_name = "az2"
        self.timer = self.create_timer(0.1, self.timer_callback)

        self.state = 0
        self.mode = -1

        self.x = self.rgb_node.ball_position[0]
        self.y = self.rgb_nod.ball_position[1]
        self.size = self.rgb_nod.size
        self.sizec = self.rgb_nod.sizec
        self.r = self.rgb_nod.r
        self.sizer = self.rgb_nod.sizer
        self.xr = self.rgb_nod.xr
        self.yr = self.rgb_nod.yr
        self.h = self.rgb_nod.h
        self.w = self.rgb_nod.w
        self.ratio = self.rgb_nod.ratio
        self.size_deduced = self.size * self.ratio

        self.top_left = self.left_node.top
        self.x_left = self.left_node.x
        self.top_right = self.right_node.top
        self.x_right = self.right_node.x
        self.x_bf = (self.x_left + self.x_right)/2
        self.x_dif = self.x_left - self.x_right

        self.ball_x_left = self.left_node.ball_x
        self.ball_size_left = self.left_node.ball_size
        self.ball_x_right = self.right_node.ball_x
        self.ball_size_right = self.right_node.ball_size

        self.x_rec=[320.0,320.0,320.0]
        self.size_rec=[.0,.0,.0,.0,.0]
        self.size_deduced_rec=[.0,.0,.0,.0,.0]
        self.avx = 320
        self.avs = 0
        self.avsd = 0
        self.size_vel = 0

    def timer_callback(self):
        rclpy.spin_once(self.rgb_node)
        rclpy.spin_once(self.left_node)
        rclpy.spin_once(self.right_node)

        self.x = self.rgb_node.ball_position[0]
        self.y = self.rgb_nod.ball_position[1]
        self.size = self.rgb_nod.size
        self.sizec = self.rgb_nod.sizec
        self.r = self.rgb_nod.r
        self.sizer = self.rgb_nod.sizer
        self.xr = self.rgb_nod.xr
        self.yr = self.rgb_nod.yr
        self.h = self.rgb_nod.h
        self.w = self.rgb_nod.w
        self.ratio = self.rgb_nod.ratio
        self.size_deduced = self.size * self.ratio

        self.top_left = self.left_node.top
        self.x_left = self.left_node.x
        self.top_right = self.right_node.top
        self.x_right = self.right_node.x
        self.x_bf = (self.x_left + self.x_right)/2
        self.x_dif = self.x_left - self.x_right

        self.ball_x_left = self.left_node.ball_x
        self.ball_size_left = self.left_node.ball_size
        self.ball_x_right = self.right_node.ball_x
        self.ball_size_right = self.right_node.ball_size

        self.x_rec.pop(0)
        self.x_rec.append(self.x)
        self.size_rec.pop(0)
        self.size_rec.append(self.size)
        self.size_deduced_rec.pop(0)
        self.size_deduced_rec.append(self.size_deduced)
        self.avx=sum(self.x_rec)/len(self.x_rec)  
        self.avs=sum(self.size_rec)/len(self.size_rec)
        self.avsd=sum(self.size_deduced_rec)/len(self.size_deduced_rec)
        self.size_vel = self.size_deduced_rec[4]-self.size_deduced_rec[3]

        state_dict = {0:'no_ball', 1:'far_mid', 2:'clo_mid', 3:'far_border', 4:'clo_border', 5:'rush_border', 6:'?',
                      7:'extclo_mid', 8:'extclo_corner', 9:'left', 10:'right', 11:'back', 12:'forth',
                      13:'boundary_lr', 14:'incline'}
        mode_dict = {-1:'none', 0:'left', 1:'right'}

        # angle incline, state 14, with mode
        if self.x_dif > 30 :
            self.state = 14
            self.mode = 0
        elif self.x_dif < 30:
            self.state = 14
            self.mode = 1
        else :


            # boundary left or right, state 13, with mode
            if self.top_left > 440 :
                self.state = 13
                self.mode = 0
            elif self.top_right > 440:
                self.state = 13
                self.mode = 1

            # forth, state 12
            elif self.x_bf < 200:
                self.state = 12
                self.mode = -1
            
            # back, state 11
            elif self.x_bf > 440:
                self.state = 11
                self.mode = -1
            else: 


                # right, state 10
                if self.ball_size_right > 500:
                    self.state = 10
                    self.mode = -1
                
                # left, state 9
                elif self.ball_size_left > 500:
                    self.state = 9
                    self.mode = -1
                
                # extclo_corner, state 8
                # extclo_mid, state 7
                elif self.yr > 460:
                    if self.xr < 20:
                        self.state = 8
                        self.mode = 0
                    elif (self.xr + self.w) > 620:
                        self.state = 8
                        self.mode = 1
                    else:
                        self.state = 7
                        self.mode = -1
                

                # rush_border, state 5
                # clo_border, state 4
                # far_border, state 3
                elif self.xr < 30:
                    self.mode = 0
                    if self.size_vel > 100:
                        self.state = 5
                    elif self.size_deduced > 2000:
                        self.state = 4
                    else:
                        self.state = 3

                elif self.xr + self.w > 610:
                    self.mode = 1
                    if self.size_vel > 100:
                        self.state = 5
                    elif self.size_deduced > 2000:
                        self.state = 4
                    else:
                        self.state = 3

                # clo_mid, state 2
                elif self.size > 2000:
                    self.state = 2
                    self.mode = -1
                
                # far_mid, state 1
                elif (self.size < 2000) & (self.size >100):
                    self.state = 1
                    self.mode = -1
                
                # no_ball, state 0
                else:
                    self.state = 0
                    self. mode = -1
        
        print("state={},mode={}".format(state_dict[self.state], mode_dict[self.mode]))


def main(args=None):
    rclpy.init()
    classifier = Classifier("classifier")
    rclpy.spin(classifier)
    try:
        while True:
            pass
    except exception:
        print('exception')
    classifier.destroy_node()
    rclpy.shutdown()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
                

                    



