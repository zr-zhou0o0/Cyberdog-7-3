# Cyberdog-7-3
The keeper (white dog)  
清华大学第三届机器狗大赛 特等奖

# 路径
workplace/src/learning/learning

# 说明
+ 是一只常常守不住门的守门狗
```
> keeper
> author: zzr
> ***scan***
> ***if in the range then we can decide the incline!!!!change the order!
> problem: jump of line in side_cam
> revise the intepret of all the classes, and move the readme to root, and highlight the essential algorithm in readme
> logic: the larger number suggest the higher priority
    mode 0 = left, 1 = right, -1 = none
    move_horizontal: control the movement of the dog
    classifier: decide the state of the dog
    state_dict = {0:'no_ball', 1:'far_mid', 2:'clo_mid', 3:'far_border', 4:'clo_border', 5:'rush_border', 6:'?',
                      7:'extclo_mid', 8:'extclo_corner', 9:'left', 10:'right', 11:'no_line', 12:'back',
                      13:'forth', 14:'boundary_lr'}
    mode_dict = {-1:'none', 0:'left', 1:'right'}

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

```


# Config
+ name：az2
+ ip：10.0.0.254
+ bluetooth name:035
+ camera: 400 * 500
+ stereo_camera:  
  ros__parameters:  
    stereo_only: false  
    #0-bgr 1-rgb 2-gray  
    format_left: 2  
    format_rgb: 2   
    format_right: 2  
    h_left: 400  
    h_rgb: 480  
    h_right: 400  
    w_left: 500  
    w_rgb: 640  
    w_right: 500
+ opencv的相机坐标系，y轴从上到下，x轴从左到右！！！
+ 左右相机要算平均x需要反转一个
+ rectangle得到的点是左上角而不是左下角！！！
+ 这里写的清清楚楚，sidecam是400x500而前置rgb是480x640，怎么没注意到。。。

# TODO
* keeper整合所有模块和逻辑
* 提高系统鲁棒性 意外状况应对措施 初始化细则
* 优化守门精准度
* 防出前后界  

* 各种小模块：自定位系统的若干尝试
    * 激光雷达：范围在前半部分的3m内 x
    * TOF：范围在1.5mm到0.66m内 x
    * 深度相机+opencv x
        * 动态定位：通过球的两次坐标信息+距离球的两次距离信息计算白狗坐标
    * 左右眼相机 x
    * 左右rgb相机 判断前后位置 判断旋转角度
    * 前置rgb相机
        * 电视位置 判断左右位置
* 自定位系统的应用：
    * 保证比赛过程中不会因为误差而不断出界：校准狗的位置和角度
    * 射门之后（球不在视野范围内）白狗应回到原点
    * 辅助守门判断
* 其他任务：
    * 去掉上位机 不让用。。。 √
    * 在movex中添加一个display相机的功能用来调试 √
    * 判断射门意图（？
    * 预测球的路径（？
    * 横过来 x


### 提醒
+ build之前要先在终端输入`cd workplace`,否则无法更新所做的修改!
+ 单独编译某一个包 colcon build --packages-select learning


### 参考资料
#### 二代机器狗的开源信息：
1. [文档博客](https://miroboticslab.github.io/blogs/#/)
2. [源码地址](https://github.com/MiRoboticsLab/cyberdog_ws)

#### ROS学习参考
1. [发布订阅节点](https://blog.csdn.net/qq_38649880/article/details/104423203)

#### 其它资料
1. [第二次培训的PPT和录屏](https://cloud.tsinghua.edu.cn/d/9aefef66ac9542a6944d/)
2. [代码托管](https://git.tsinghua.edu.cn/cyberdog_competition/2024)

### 常用命令行
 1. 打开深度相机： 
    + ros2 launch realsense2_camera on_dog.py
    + ros2 lifecycle set /az2/camera/camera configure
    + ros2 lifecycle set /az2/camera/camera activate  

    + ros2 lifecycle set /az2/camera/camera deactivate
    + ros2 lifecycle set /az2/camera/camera cleanup 

    + /az2/camera/depth/image_rect_raw 深度图 480*640 16UC1
    + /az2/camera/infra1/image_rect_raw 左目 480*640 mono8
    + /az2/camera/infra2/image_rect_raw 右目

 <!--   + ros2 launch realsense2_camera realsense_align_node.launch.py
    + ros2 lifecycle set /az2/camera/camera_align configure
    + ros2 lifecycle set /az2/camera/camera_align activate-->

2. 运行
    + cd workplace
    + colcon build
    + ros2 run learning XXX
3. 启动rgb相机
    + 窗口1:ros2 launch camera_test stereo_camera.py
    + 窗口2:# 启动lifecycle的接口
    + ros2 lifecycle set /az2/camera/camera configure 
    + ros2 lifecycle set /az2/camera/camera activate 
    + ros2 service call /stereo_camera/change_state lifecycle_msgs/srv/ChangeState "{transition: {id: 1}}" 
    + ros2 service call /stereo_camera/change_state lifecycle_msgs/srv/ChangeState "{transition: {id: 3}}" 

    + ros2 topic echo /image_rgb 400*500 bgr8
    
4. 连接Xming
    + xming host 文件中的ip需要是狗子ip
    + export DISPLAY=10.0.0.182:0.0
        + xhost +
    + **要在每个terminal都手打一遍！！**
5. 检查是否连接成功
    + ros2 topic list
    + ros2 topic echo /<名称>
    + note：开深度相机时echo要加上/az2/


#### 如何配置Xming实现远程主机（Windows）屏显
##### 远程主机（自己的电脑，此处用的是Windows）
+ 下载Xming[下载网址](https://sourceforge.net/projects/xming/?source=typ_redirect)
+ 打开Xming安装目录，目录下x0.hosts文件，在localhost下另起一行粘贴入{本机IP}（10.0.0.254），保存
+ 如果在上一步之前打开过Xming，要关闭后重启
+ 远程配置完毕
+ 查看【远程IP】：WindowsPowershell输入ipconfig查看局域网IPv4 ip地址（10.0.0.xxx）
+ 
##### 本机（此处为狗子的linux系统）  
+ sudo apt-get install x11-xserver-utils
+ xstart（只需执行一次，之后重启狗子无需再执行，下面其余命令在重启后要重新执行）
+ export DISPLAY={远程IP}:0.0
+ xhost +
+ 切换rgb相机传回图像类别：/opt/ros2/cyberdog/share/camera_test/config（注意**不在**/home/mi目录下，要在open folder那边直接复制上面路径）下yaml文件，修改format_rgb参数（改为rgb对应选项）

#### 更新
+ sudo apt update
+ sudo apt upgrade

### 进度  
0523 zzr:  
+ upgrade了白狗
+ 成功display  

0524 zzr wmy：
+ 校准狗的姿势
+ 修改data receive的方式
+ 成功运行keeper

0525 zzr:
+ pass掉了激光雷达和TOF方案
+ 打开了深度相机
+ realsense_cam_suber实现了打开深度图像（但发现清晰度太低）
+ 下一步：利用电视的位置识别狗的横向坐标

0526 zzr:
+ 阅读了opencv tutorial
+ new class: realsense cam suber which can recognize the black television（未测试）
+ move horizontal终于可以运行了 加了一个display 但是ballyabs还是0

0528 zzr：
+ 

### 常见报错
+ cannot open display, try:
...(useless)...  
rebuild  
export display  
xhost+  
restart xming 
change xming hosts 
cd workplace  
change the state of cam in the config yaml  
uncharge the dog  
...  
input the command with hand, don't copy it, and it works!!!!!  
**reopen the dog and the camera**
