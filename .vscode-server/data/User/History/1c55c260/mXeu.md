# Cyberdog-7-3
The keeper (white dog)

# Config
+ name：az2
+ ip：10.0.0.252

# TODO
+ 研究一下b站上的机器人踢足球算法
+ 尝试打开左右相机和深度相机
+ 在movex中添加一个display相机的功能用来调试
+ 看一下相机是几乘几
+ 防止狗越界：  
Plan A：改变规则，利用两侧的红点判断狗的左右位置和前后位置
Plan B：利用深度相机/sensor/前面的rgb相机判断狗的左右移动和前后移动，防止越界（误差大）

### 提醒
+ 同时写代码时注意保存
+ build之前要先在终端输入`cd workplace`,否则无法更新所做的修改!
+ 单独编译某一个包 colcon build --packages-select learning
+
### 参考资料
#### 二代机器狗的开源信息：
1. [文档博客](https://miroboticslab.github.io/blogs/#/)
2. [源码地址](https://github.com/MiRoboticsLab/cyberdog_ws)

#### ROS学习参考
1. [发布订阅节点](https://blog.csdn.net/qq_38649880/article/details/104423203)
2. 
#### 其它资料
1. [第二次培训的PPT和录屏](https://cloud.tsinghua.edu.cn/d/9aefef66ac9542a6944d/)
2. [代码托管](https://git.tsinghua.edu.cn/cyberdog_competition/2024)
3. [whf的github仓库](https://github.com/HeFeiW/cyberdog_az)

### 常用命令行
<!-- 1. 打开相机： 
    + ros2 launch realsense2_camera on_dog.py
    + ros2 lifecycle set /camera/camera configure
    + ros2 lifecycle set /camera/camera activate -->
1.打开realsense(研究中......)
    + ros2 launch realsense2_camera on_dog.py
    + ros2 launch realsense2_camera realsense_align_node.launch.py
    + ros2 lifecycle set /az1/camera/camera configure
    + ros2 lifecycle set /az1/camera/camera activate
    + ros2 lifecycle set /az1/camera/camera_align configure
    + ros2 lifecycle set /az1/camera/camera_align activate
    + ros2 service call /on_dog/change_state lifecycle_msgs/srv/ChangeState "{transition: {id: 1}}"
    + ros2 service call /realsense2_camera/change_state lifecycle_msgs/srv/ChangeState "{transition: {id: 3}}"

    + ros2 service call /stereo_camera/change_state lifecycle_msgs/srv/ChangeState "{transition: {id: 1}}"
    + ros2 service call /stereo_camera/change_state lifecycle_msgs/srv/ChangeState "{transition: {id: 3}}"

2. 运行
    + cd workplace
    + colcon build
    + ros2 run learning XXX
3. 启动rgb相机
    + 窗口1:ros2 launch camera_test stereo_camera.py
    + 窗口2:# 启动lifecycle的接口
    + ros2 lifecycle set /az1/camera/camera configure 
    + ros2 lifecycle set /az1/camera/camera activate 
    + ros2 service call /stereo_camera/change_state lifecycle_msgs/srv/ChangeState "{transition: {id: 1}}" 
    + ros2 service call /stereo_camera/change_state lifecycle_msgs/srv/ChangeState "{transition: {id: 3}}"
4. 连接Xming
    + export DISPLAY=local ip:0.0
        + xhost +
5. 检查是否连接成功
    + ros2 topic list
    + ros2 topic echo /<名称>
### 运动参数
飞扑距离
x==410,y==378,area==31450
上位机：
摄像头坐标系，左-右+，球门y坐标7.9 x坐标0.2

#### 如何配置Xming实现远程主机（Windows）屏显
##### 远程主机（自己的电脑，此处用的是Windows）
+ 下载Xming[下载网址](https://sourceforge.net/projects/xming/?source=typ_redirect)
+ 打开Xming安装目录，目录下x0.hosts文件，在localhost下另起一行粘贴入{本机IP}（10.0.0.123/168），保存
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

### issue
球和球门垂直


### debug记录&提醒
+ 如果转速过大，狗子转的角度会大于预设角度
+ 打开src中的learning而非install中的learning
+ build或者git的时候记得cd

#### 规则及分析
1. 总体：  
两方红黑狗对攻  
2. 避障：  
避障线程+striker线程，避障线程在发出避障指令前判断：目前是否在射门中，若在射门中，则不发出指令。
加一个topic，记录当前状态（strike or avoid）。
3. 守门：  

4. striker：  
射门
    转到直线
    优先靠近球，再yz旋转至正确射门方向
防守

2. 如何防止踢球时卡球：  
更改rotate函数使球不处于正中间
