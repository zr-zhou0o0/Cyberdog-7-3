'''
> move_horizontal
> author: zzr
> date: 2024-05-24
> make the dog move horizontal aiming at the ball
> note:
    - if speed.y > 0 the dog move left,if speed.y < 0 the dog move right
    - if ball_y > 330, the ball is close!

'''

import cv2
from cv_bridge import CvBridge
import numpy as np
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image, Range
from protocol.msg import MotionServoCmd
import threading
import time

from .classifier import Classifier


class move_horizontal(Node):
    def __init__(self, name):
        super().__init__(name)
        self.classifier_node = Classifier("classifier")
        self.speed_x, self.speed_y, self.speed_z = 0.0, 0.0, 0.0
        self.dog_name = "az2"
        self.pub = self.create_publisher(MotionServoCmd, f"/{self.dog_name}/motion_servo_cmd", 10)
        self.timer = self.create_timer(0.1, self.timer_callback)
        # self.x_rec=[320.0,320.0,320.0]  # 优化：none类型
        # self.avx_rec=[320.0,320.0,320.0]
        # self.size_rec=[.0,.0,.0,.0,.0]
        # self.aim = False



        self.state = self.classifier_node.state
        self.mode = self.classifier_node.mode

        self.x = self.classifier_node.x
        self.y = self.classifier_node.y
        self.size = self.classifier_node.size
        self.sizec = self.classifier_node.sizec
        self.r = self.classifier_node.r
        self.sizer = self.classifier_node.sizer
        self.xr = self.classifier_node.xr
        self.yr = self.classifier_node.yr
        self.h = self.classifier_node.h
        self.w = self.classifier_node.w
        self.ratio = self.classifier_node.ratio
        self.size_deduced = self.classifier_node.size_deduced

        self.xr_rec=[.0,.0,.0]
        self.xr_w_rec=[320.0,320.0,320.0]
        self.xr_vel=0
        self.xr_w_vel=[.0,.0,.0]

        self.top_left = self.classifier_node.top_left
        self.x_left = self.classifier_node.x_left
        self.size_left = self.classifier_node.size_left
        self.top_right = self.classifier_node.top_right
        self.x_right = self.classifier_node.x_right
        self.size_right = self.classifier_node.size_right

        self.x_left_swap = self.classifier_node.x_left_swap
        self.x_bf = self.classifier_node.x_bf
        self.x_dif = self.classifier_node.x_dif

        # self.ball_x_left = self.left_node.ball_x
        # self.ball_size_left = self.left_node.ball_size
        # self.ball_x_right = self.right_node.ball_x
        # self.ball_size_right = self.right_node.ball_size

        self.x_rec=self.classifier_node.x_rec
        self.size_rec=self.classifier_node.size_rec
        self.size_deduced_rec=self.classifier_node.size_deduced_rec
        self.avx = self.classifier_node.avx
        self.avs = self.classifier_node.avs
        self.avsd = self.classifier_node.avsd
        self.size_vel = self.classifier_node.size_vel

        self.x_vel = 0
        self.x_vel_rec=[.0,.0,.0]

        self.number = 0




    def timer_callback(self):
        msg = MotionServoCmd()
        rclpy.spin_once(self.classifier_node)

        self.state = self.classifier_node.state
        self.mode = self.classifier_node.mode

        self.x = self.classifier_node.x
        self.y = self.classifier_node.y
        self.size = self.classifier_node.size
        self.sizec = self.classifier_node.sizec
        self.r = self.classifier_node.r
        self.sizer = self.classifier_node.sizer
        self.xr = self.classifier_node.xr
        self.yr = self.classifier_node.yr
        self.h = self.classifier_node.h
        self.w = self.classifier_node.w
        self.ratio = self.classifier_node.ratio
        self.size_deduced = self.classifier_node.size_deduced

        self.xr_rec.pop(0)
        self.xr_rec.append(self.xr)
        self.xr_w_rec.pop(0)
        self.xr_w_rec.append(self.xr + self.w)
   
        self.xr_vel=self.xr_rec[2]-self.xr_rec[1] # >0, ball move right; <0, ball move left
        self.xr_w_vel=self.xr_w_rec[2]-self.xr_w_rec[1]

        self.top_left = self.classifier_node.top_left
        self.x_left = self.classifier_node.x_left
        self.size_left = self.classifier_node.size_left
        self.top_right = self.classifier_node.top_right
        self.x_right = self.classifier_node.x_right
        self.size_right = self.classifier_node.size_right

        self.x_left_swap = self.classifier_node.x_left_swap
        self.x_bf = self.classifier_node.x_bf
        self.x_dif = self.classifier_node.x_dif

        # self.ball_x_left = self.left_node.ball_x
        # self.ball_size_left = self.left_node.ball_size
        # self.ball_x_right = self.right_node.ball_x
        # self.ball_size_right = self.right_node.ball_size

        self.x_rec=self.classifier_node.x_rec
        self.size_rec=self.classifier_node.size_rec
        self.size_deduced_rec=self.classifier_node.size_deduced_rec
        self.avx = self.classifier_node.avx
        self.avs = self.classifier_node.avs
        self.avsd = self.classifier_node.avsd
        self.size_vel = self.classifier_node.size_vel

        self.x_vel=self.x_rec[2]-self.x_rec[1]
        self.x_vel_rec.pop(0)
        self.x_vel_rec.append(self.x_vel)
        
        if self.state == 14: # boundary lr
            msg.motion_id = 308
            if self.mode == 1:
                self.speed_x, self.speed_y, self.speed_z = 0.0, 0.27, 0.0
            elif self.mode == 0: # should go right
                self.speed_x, self.speed_y, self.speed_z = 0.0, -0.27, 0.0
            else:
                msg.motion_id = 308
                pass
        
        elif self.state == 13: #forth, should go back
            msg.motion_id = 308
            self.speed_x, self.speed_y, self.speed_z = -0.27, 0.0, 0.0
        
        elif self.state == 12: # back
            msg.motion_id = 308
            self.speed_x, self.speed_y, self.speed_z = 0.27, 0.0, 0.0

        elif self.state == 11:
            msg.motion_id = 308
            pass

        elif self.state == 10: # right
            msg.motion_id = 308
            pass

        elif self.state == 9: # left
            msg.motion_id = 308
            pass

        elif self.state == 8: # extclo_corner
            msg.motion_id = 305
            if self.mode == 1:
                self.speed_x, self.speed_y, self.speed_z = 0.0, -0.47, 0.0
            elif self.mode == 0:
                self.speed_x, self.speed_y, self.speed_z = 0.0, 0.47, 0.0
            else:
                msg.motion_id = 305
                pass
        
        elif self.state == 7: # extclo_mid
            msg.motion_id = 305
            self.speed_x, self.speed_y, self.speed_z = 0.0, 0.0, 0.0

        elif self.state == 6:
            msg.motion_id = 308
            pass

        elif self.state == 5: # rush_border
            msg.motion_id = 305
           
            if self.mode == 1:
                self.speed_x, self.speed_y, self.speed_z = 0.0, -0.35, 0.0
            elif self.mode == 0:
                self.speed_x, self.speed_y, self.speed_z = 0.0, 0.35, 0.0
            else:
                msg.motion_id = 305
                pass

        elif self.state == 4: # clo_border
            msg.motion_id = 308
            # if self.mode == 1: #right, use xr as x_center
            #     if self.xr_vel > 1: # ball move right
            #         self.speed_x, self.speed_y, self.speed_z = 0.0, -0.33, 0.0
            #     elif self.xr_vel < -1: 
            #         self.speed_x, self.speed_y, self.speed_z = 0.0, 0.33, 0.0
            #     else:
            #         self.speed_x, self.speed_y, self.speed_z = 0.0, -0.20, 0.0
                
            # elif self.mode == 0: #left, use xr+w as x_center
            #     if self.xr_w_vel > 1: # ball move right
            #         self.speed_x, self.speed_y, self.speed_z = 0.0, -0.33, 0.0
            #     elif self.xr_w_vel < -1: 
            #         self.speed_x, self.speed_y, self.speed_z = 0.0, 0.33, 0.0
            #     else:
            #         self.speed_x, self.speed_y, self.speed_z = 0.0, 0.20, 0.0

            # else:
            #     msg.motion_id = 308
            #     pass

            if  self.avx < 280: #球从左侧溜走:向左走  320是像素中心位置
                self.speed_x, self.speed_y, self.speed_z = 0.0, 0.35, 0.0
                if self.avx > 300:
                    self.speed_x, self.speed_y, self.speed_z = 0.0, 0.0, 0.0
            elif self.avx > 360: # 球从右侧溜走：向右走
                self.speed_x, self.speed_y, self.speed_z = 0.0, -0.35, 0.0
                if self.avx < 340:
                    self.speed_x, self.speed_y, self.speed_z = 0.0, 0.0, 0.0
            else:
                self.speed_x, self.speed_y, self.speed_z = 0.0, 0.0, 0.0


        elif self.state == 3: # far_border
            msg.motion_id = 305
            if self.mode == 1:
                self.speed_x, self.speed_y, self.speed_z = 0.0, -0.27, 0.0
            elif self.mode == 0:
                self.speed_x, self.speed_y, self.speed_z = 0.0, 0.27, 0.0
            else:
                msg.motion_id = 308
                pass
        
        elif self.state == 2: #clo_mid #############
            msg.motion_id = 305
            # if (self.x > 280) & (self.x < 360):
            #     self.speed_x, self.speed_y, self.speed_z = 0.0, 0.0, 0.0
            # else:

            # v.1
            # if sum(self.x_vel_rec) < 1: # ball move left ##############会偏右？？？
            #     self.speed_x, self.speed_y, self.speed_z = 0.0, 0.34, 0.0
            # elif sum(self.x_vel_rec) > 1: 
            #     self.speed_x, self.speed_y, self.speed_z = 0.0, -0.34, 0.0
            # else:
            #     self.speed_x, self.speed_y, self.speed_z = 0.0, 0.0, 0.0
            # self.get_logger().info(f"x_vel={self.x_vel}")
            # self.get_logger().info(f"x_rec={self.x_rec}")

            # v.2
            # if self.x_vel < 0: # ball move left
            #     self.speed_x, self.speed_y, self.speed_z = 0.0, 0.37, 0.0
            # elif self.x_vel > 0: 
            #     self.speed_x, self.speed_y, self.speed_z = 0.0, -0.37, 0.0
            # else:
            #     self.speed_x, self.speed_y, self.speed_z = 0.0, 0.0, 0.0
            # self.get_logger().info(f"x_vel={self.x_vel}")
            # self.get_logger().info(f"x_rec={self.x_rec}")

            if  self.avx < 280: #球从左侧溜走:向左走  320是像素中心位置
                self.speed_x, self.speed_y, self.speed_z = 0.0, 0.27, 0.0
                if self.avx > 300:
                    self.speed_x, self.speed_y, self.speed_z = 0.0, 0.0, 0.0
            elif self.avx > 360: # 球从右侧溜走：向右走
                self.speed_x, self.speed_y, self.speed_z = 0.0, -0.27, 0.0
                if self.avx < 340:
                    self.speed_x, self.speed_y, self.speed_z = 0.0, 0.0, 0.0
            else:
                self.speed_x, self.speed_y, self.speed_z = 0.0, 0.0, 0.0


        elif self.state == 1: # far_mid
            msg.motion_id = 305
            self.speed_x, self.speed_y, self.speed_z = 0.0, 0.0, 0.0

        elif self.state == 0: # noball
            msg.motion_id = 305
            self.speed_x, self.speed_y, self.speed_z = 0.0, 0.0, 0.0

        else:
            msg.motion_id = 308
            pass
        
        self.number += 1
        if(self.number%50) > 40:
            self.speed_x, self.speed_y, self.speed_z = 0.1, 0.0, 0.0
        self.get_logger().info(f"number%50={self.number%50}")



        msg.cmd_type = 1
        msg.value = 2
        msg.vel_des = [self.speed_x, self.speed_y, self.speed_z]
        msg.step_height = [0.05, 0.05]
        self.pub.publish(msg)
        # self.get_logger().info(f"avs={avs},avx={avx},velx={ball_x_vel},by={ball_y}")


def move_horizontal_aim_ball(args=None):
    rclpy.init()
    # classifier_node = Classifier("Classifier")
    move_horizontal_node = move_horizontal("move_horizontal_node")
    move_horizontal_thread = threading.Thread(target=rclpy.spin, args=(move_horizontal_node,))
    move_horizontal_thread.start()
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print('KeyBoardInterrupt')
    move_horizontal_node.destroy_node()
    # rgb_node.destroy_node()
    rclpy.shutdown()
    cv2.destroyAllWindows()
    return True


def main(args=None):
    print(move_horizontal_aim_ball())


if __name__ == '__main__':
    main()