# Installation Guide

## 1. Supported Environment

The project is currently developed and tested with:

- Ubuntu 24.04 LTS
- WSL 2 on Windows 11
- ROS 2 Jazzy Jalisco
- Gazebo Harmonic
- Python 3
- CMake and colcon

A native Ubuntu installation can also be used. The Windows-specific joystick sender is only required when the controller is read from Windows and ROS 2 runs inside WSL.

---

## 2. Install ROS 2 Jazzy

Follow the official ROS 2 Jazzy installation procedure for Ubuntu 24.04, then verify the installation:

```bash
source /opt/ros/jazzy/setup.bash
ros2 --help
```

To source ROS 2 automatically in every Bash terminal:

```bash
echo "source /opt/ros/jazzy/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

---

## 3. Install Development Tools

```bash
sudo apt update
sudo apt install -y \
  git \
  build-essential \
  cmake \
  python3 \
  python3-pip \
  python3-rosdep \
  python3-colcon-common-extensions \
  python3-vcstool
```

Initialize `rosdep` if it has not already been initialized:

```bash
sudo rosdep init
rosdep update
```

If `rosdep init` reports that it has already been initialized, continue with `rosdep update`.

---

## 4. Install ROS 2 Runtime Dependencies

### Robot description and visualization

```bash
sudo apt install -y \
  ros-jazzy-xacro \
  ros-jazzy-robot-state-publisher \
  ros-jazzy-joint-state-publisher \
  ros-jazzy-joint-state-publisher-gui \
  ros-jazzy-rviz2
```

### Gazebo simulation

```bash
sudo apt install -y \
  ros-jazzy-ros-gz \
  ros-jazzy-ros-gz-sim \
  ros-jazzy-ros-gz-bridge
```

### Navigation2

```bash
sudo apt install -y \
  ros-jazzy-navigation2 \
  ros-jazzy-nav2-bringup
```

The released Nav2 packages for Jazzy are named `ros-jazzy-navigation2` and `ros-jazzy-nav2-bringup`. There is no standard package named `ros2-jazzy-nav2`.

### SLAM Toolbox and map server

```bash
sudo apt install -y \
  ros-jazzy-slam-toolbox \
  ros-jazzy-nav2-map-server
```

### Teleoperation and joystick support

```bash
sudo apt install -y \
  ros-jazzy-joy \
  ros-jazzy-teleop-twist-joy \
  ros-jazzy-teleop-twist-keyboard
```

### Useful diagnostics

```bash
sudo apt install -y \
  ros-jazzy-tf2-tools \
  ros-jazzy-rqt \
  ros-jazzy-rqt-graph
```

---

## 5. Clone the Repository

```bash
mkdir -p ~/AMR-Project
cd ~/AMR-Project

git clone git@github.com:Salim-MSI/Autonomous-Mobile-Robot.git
cd Autonomous-Mobile-Robot/ros2_ws
```

For an HTTPS clone instead:

```bash
git clone https://github.com/Salim-MSI/Autonomous-Mobile-Robot.git
```

---

## 6. Install Package Dependencies with rosdep

From the ROS 2 workspace root:

```bash
cd ~/AMR-Project/Autonomous-Mobile-Robot/ros2_ws

source /opt/ros/jazzy/setup.bash

rosdep install \
  --from-paths src \
  --ignore-src \
  --rosdistro jazzy \
  -r -y
```

This is the preferred method for installing dependencies declared in each package's `package.xml`.

Any dependency required by the source code should be declared in `package.xml` so that a clean clone can be configured with `rosdep`.

---

## 7. Build the Workspace

```bash
cd ~/AMR-Project/Autonomous-Mobile-Robot/ros2_ws

source /opt/ros/jazzy/setup.bash

colcon build --symlink-install
```

Only source the workspace after a successful build:

```bash
source install/setup.bash
```

A safe chained version is:

```bash
source /opt/ros/jazzy/setup.bash && \
colcon build --symlink-install && \
source install/setup.bash
```

To source the workspace automatically, add the following line to `~/.bashrc`:

```bash
echo "source ~/AMR-Project/Autonomous-Mobile-Robot/ros2_ws/install/setup.bash" >> ~/.bashrc
```

Do this only after the workspace has built successfully.

---

## 8. Clean Rebuild

Use a clean rebuild after changing package installation rules, renaming files, modifying CMake configuration, or switching branches:

```bash
cd ~/AMR-Project/Autonomous-Mobile-Robot/ros2_ws

rm -rf build install log

source /opt/ros/jazzy/setup.bash
colcon build --symlink-install
source install/setup.bash
```

---

## 9. Verify the Installation

List the project packages:

```bash
ros2 pkg list | grep '^amr_'
```

Expected packages may include:

```text
amr_bringup
amr_control
amr_description
amr_joystick_bridge
amr_localization
amr_navigation
amr_simulation
amr_slam
```

The exact list depends on the current repository branch.

Verify important external packages:

```bash
ros2 pkg prefix nav2_bringup
ros2 pkg prefix slam_toolbox
ros2 pkg prefix ros_gz_sim
ros2 pkg prefix robot_state_publisher
```

