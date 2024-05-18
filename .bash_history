
mkdir -p workplace/src
cd workplace/src/
ros2 pkg create --build-type ament_python learning
cd ..
colcon build
ros2 run learning stand
colcon build
cd workplace
colcon build
ros2 run learning stand
git init
git config --global user.name"lx88882222" 
git remote add origin https://github.com/zr-zhou0o0/Cyberdog-7-3.git
git add workplace
git commit -m "0517"
git config --global user.email "1712818580@qq.com"
git config --global user.name "lx88882222"
git commit -m "0517"
git push origin master
sudo apt install libopencv-dev python3-opencv
sudo apt update
sudo apt install libopencv-dev python3-opencv
cd workplace
colcon build
ros2 run learning keeper
ros2 run learning track
ros2 launch camera_test stereo_camera.py
ros2 lifecycle set /az2/camera/camera configure
ros2 lifecycle set /az2/camera/camera activat
ros2 service call /stereo_camera/change_state lifecycle_msgs/srv/ChangeState "{transition: {id: 1}}" 
ros2 service call /stereo_camera/change_state lifecycle_msgs/srv/ChangeState "{transition: {id: 3}}"
ros2 run learning track
ros2 lifecycle set /az2/camera/camera configure
ros2 lifecycle set /az2/camera/camera activate
ros2 service call /stereo_camera/change_state lifecycle_msgs/srv/ChangeState "{transition: {id: 1}}" 
ros2 service call /stereo_camera/change_state lifecycle_msgs/srv/ChangeState "{transition: {id: 3}}"
export DISPLAY=10.0.0.200:0.0
xhost +
cd workplace
colcon bulid
colcon build
ros2 run learning track
