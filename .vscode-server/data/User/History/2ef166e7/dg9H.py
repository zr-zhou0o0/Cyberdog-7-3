'''
> move_horizontal
> author: zzr
> date: 2024-05-24
> make the dog move horizontal aiming at the ball
> note: if speed.y > 0 the dog move left,if speed.y < 0 the dog move right

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
import socket

from .get_data import Location
from .rgb_cam_suber import RGBCamSuber
# from .data_receive import get_dog_address


class move_horizontal(Node):
    def __init__(self, name, RGBCamSuber):
        super().__init__(name)
        self.rgb_node = RGBCamSuber
        self.speed_x, self.speed_y, self.speed_z = 0.0, 0.0, 0.0
        self.dog_name = "az2"
        self.pub = self.create_publisher(MotionServoCmd, f"/{self.dog_name}/motion_servo_cmd", 10)
        self.timer = self.create_timer(0.1, self.timer_callback)
        self.x_rec=[320.0,320.0,320.0]
        self.size_rec=[.0,.0,.0,.0,.0]
        self.xx=[320.0,320.0,320.0]
        self.aim = False

        self.dog_coords, self.ball_coords = get_dog_address()
        self.ball_y_abs = self.ball_coords[1]
        self.ball_y_rec=[.0,.0,.0]



    def timer_callback(self):
        rclpy.spin_once(self.rgb_node)
        ball_x, ball_y = self.rgb_node.ball_position
        size = self.rgb_node.size

        if ball_x != 0:  # 持续更新x坐标
            self.x_rec.pop(0)
            self.x_rec.append(ball_x)
        self.size_rec.pop(0)
        self.size_rec.append(size)
        self.ball_y_rec.pop(0)
        self.ball_y_rec.append(self.ball_y_abs)

        avx=sum(self.x_rec)/len(self.x_rec)  
        avs=sum(self.size_rec)/len(self.size_rec)

        # self.xx.pop(0) # self.xx记录球的连续三个x值
        # self.xx.append(avx)

        # 如果球不见了或者球在往外走
        if (avs <= 500) | ((self.ball_y_rec[2]+0.1 < self.ball_y_rec[1]) & (self.ball_y_rec[1]+0.1 < self.ball_y_rec[0])): 
            self.speed_x, self.speed_y, self.speed_z = 0.0, 0.0, 0.0
            self.aim = False

        if (avs > 500) & (avs < 1600): # 如果球很远或者走掉了
            if  avx < 280: #球从左侧溜走:向左走  320是像素中心位置
                self.speed_x, self.speed_y, self.speed_z = 0.0, 0.27, 0.0
                if avx > 300:
                    self.speed_x, self.speed_y, self.speed_z = 0.0, 0.0, 0.0
            elif avx > 360: # 球从右侧溜走：向右走
                self.speed_x, self.speed_y, self.speed_z = 0.0, -0.27, 0.0
                if avx < 340:
                    self.speed_x, self.speed_y, self.speed_z = 0.0, 0.0, 0.0
            else:
                self.speed_x, self.speed_y, self.speed_z = 0.0, 0.0, 0.0
        # 可以加一个校准系统：如果多次都在“中心”循环中，但是avoriginx偏差较大，就加一次速度
        
        if (avs >= 1600) & (avs < 1850): # 如果球比较近了
            # if yy[0]<yy[1] & yy[1]<yy[2]: # 如果球离球门越来越近
            if avx > 280 and avx < 360:  #球在视野中心：不再平移
                self.speed_x, self.speed_y, self.speed_z = 0.0, 0.0, 0.0
                self.aim = True
            else:
                if (self.x_rec[0]+2.0 < self.x_rec[1]) & (self.x_rec[1]+2.0 < self.x_rec[2]): # 如果x越来越大，狗往右走
                    self.speed_x, self.speed_y, self.speed_z = 0.0, -0.35, 0.0
                elif (self.x_rec[2]+2.0 < self.x_rec[1]) & (self.x_rec[1]+2.0 < self.x_rec[0]):# 如果x越来越小，狗往左走
                    self.speed_x, self.speed_y, self.speed_z = 0.0, 0.35, 0.0
                else: # 如果球几乎不动，狗不动
                    self.speed_x, self.speed_y, self.speed_z = 0.0, 0.0, 0.0
                    self.aim = True

        if (avs >= 1850) | (self.ball_y_abs > 7.5): # 如果球几乎在眼前
            if avx > 320:
                self.speed_x, self.speed_y, self.speed_z = 0.0, -0.45, 0.0
            else:
                self.speed_x, self.speed_y, self.speed_z = 0.0, 0.45, 0.0

            
        # 下一步：利用左右相机，如果球在左边就疯狂往左走，反之亦然，除非size很小
        # 问题：如果球离狗很近，但是球在视野边缘，size也会很小，这时候就要用到上位机判断了

        msg = MotionServoCmd()
        if avs < 1600: 
            msg.motion_id = 308
        else: 
            msg.motion_id = 305 
        msg.cmd_type = 1
        msg.value = 2
        msg.vel_des = [self.speed_x, self.speed_y, self.speed_z]
        msg.step_height = [0.05, 0.05]
        self.pub.publish(msg)
        self.get_logger().info(f"ballyabs={self.ball_y_abs},avs={avs},size={size},avx={avx},origin_x={self.x_rec}")

   



def move_horizontal_aim_ball(mode=0):
    rclpy.init()
    rgb_node = RGBCamSuber("RGBCamSuber")
    move_horizontal_node = move_horizontal("move_horizontal_node", rgb_node)
    move_horizontal_thread = threading.Thread(target=rclpy.spin, args=(move_horizontal_node,))
    move_horizontal_thread.start()
    if mode == 0:
        while(move_horizontal_node.aim == False):
            pass
    elif mode == 1:
        try:
            while True:
                pass
        except KeyboardInterrupt:
            print('KeyBoardInterrupt')
    move_horizontal_node.destroy_node()
    rgb_node.destroy_node()
    rclpy.shutdown()
    cv2.destroyAllWindows()
    return True
def main(args=None):
    print(move_horizontal_aim_ball())
if __name__ == '__main__':
    main()