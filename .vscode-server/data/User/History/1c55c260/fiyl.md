# Cyberdog-7-3
The keeper (white dog)

# Config
+ name：az2
+ ip：10.0.0.252
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

# TODO
* 自定位系统的若干尝试：
    * 激光雷达：范围在前半部分的3m内 无法有效利用
    * TOF：范围在1.5mm到0.66m内 无法有效利用
    * 深度相机+opencv
        * 动态定位：通过球的两次坐标信息+距离球的两次距离信息计算白狗坐标
        * 静态定位
    * 左右rgb相机+opencv
    * 前置rgb相机+opencv
* 自定位系统的应用：
    * 保证比赛过程中不会因为误差而不断出界：校准狗的位置和角度
    * 射门之后（球不在视野范围内）白狗应回到原点
    * 辅助守门判断
* 其他任务：
    * 在movex中添加一个display相机的功能用来调试  
* 判断射门意图（？
* 预测球的路径（？
* 横过来


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

    + /az2/camera/depth/image_rect_raw 深度图
    + /az2/camera/infra1/image_rect_raw 左目
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
    
    + /image_rgb
4. 连接Xming
    + export DISPLAY=local ip:0.0
        + xhost +
5. 检查是否连接成功
    + ros2 topic list
    + ros2 topic echo /<名称>
    + note：开深度相机时echo要加上/az2/


#### 如何配置Xming实现远程主机（Windows）屏显
##### 远程主机（自己的电脑，此处用的是Windows）
+ 下载Xming[下载网址](https://sourceforge.net/projects/xming/?source=typ_redirect)
+ 打开Xming安装目录，目录下x0.hosts文件，在localhost下另起一行粘贴入{本机IP}（10.0.0.252），保存
+ 如果在上一步之前打开过Xming，要关闭后重启
+ 远程配置完毕
+ 查看【远程IP】：WindowsPowershell输入ipconfig查看局域网IPv4 ip地址（10.0.0.xxx）
+ 
##### 本机（此处为狗子的linux系统）  
+ sudo apt-get install x11-xserver-utils
+ xstart（只需执行一次，之后重启狗子无需再执行，下面其余命令在重启后要重新执行）
+ export DISPLAY={远程IP}:0.0
+ xhost +
\* 切换rgb相机传回图像类别：/opt/ros2/cyberdog/share/camera_test/config（注意**不在**/home/mi目录下，要在open folder那边直接复制上面路径）下yaml文件，修改format_rgb参数（改为rgb对应选项）

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

0525
+ topic list:  
head_tof_payload
keep_distance_level
lidar_mapping_alive
local_costmap/local_costmap/transition_event