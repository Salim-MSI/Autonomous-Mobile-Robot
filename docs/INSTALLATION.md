# Installation Guide

This guide explains how to set up the Autonomous Mobile Robot (AMR) development environment from a clean machine.

The project is designed for **ROS 2 Jazzy**, **Ubuntu 24.04**, and **Gazebo Harmonic**.

---

# Table of Contents

- Supported Environment
- Prerequisites
- Install ROS 2
- Install Development Tools
- Install Project Dependencies
- Clone the Repository
- Install Workspace Dependencies
- Build the Workspace
- Verify the Installation
- Clean Rebuild
- Common Verification Commands
- Troubleshooting

---

# Supported Environment

The project is actively developed and tested with:

| Component | Version |
|----------|---------|
| Ubuntu | 24.04 LTS |
| Windows | Windows 11 + WSL2 |
| ROS | ROS 2 Jazzy Jalisco |
| Gazebo | Harmonic |
| Python | 3.12 |
| CMake | Latest |
| colcon | Latest |

Although native Ubuntu is supported, the primary development environment currently uses **WSL2**.

---

# Prerequisites

Before starting, make sure you have:

- Ubuntu 24.04
- Internet connection
- Git
- Python 3
- Approximately 10 GB of free disk space

---

# Install ROS 2 Jazzy

Follow the official ROS 2 installation guide for Ubuntu 24.04.

After installation, verify:

```bash
source /opt/ros/jazzy/setup.bash

ros2 --help
```

If the command succeeds, ROS 2 is correctly installed.

Automatically source ROS:

```bash
echo "source /opt/ros/jazzy/setup.bash" >> ~/.bashrc

source ~/.bashrc
```

---

# Install Development Tools

```bash
sudo apt update

sudo apt install -y \
    git \
    build-essential \
    cmake \
    python3 \
    python3-pip \
    python3-colcon-common-extensions \
    python3-vcstool \
    python3-rosdep
```

Initialize rosdep (only once):

```bash
sudo rosdep init

rosdep update
```

If rosdep was already initialized:

```bash
rosdep update
```

---

# Install ROS 2 Packages

## Robot Description

```bash
sudo apt install -y \
    ros-jazzy-xacro \
    ros-jazzy-robot-state-publisher \
    ros-jazzy-joint-state-publisher \
    ros-jazzy-rviz2
```

---

## Gazebo Harmonic

```bash
sudo apt install -y \
    ros-jazzy-ros-gz \
    ros-jazzy-ros-gz-sim \
    ros-jazzy-ros-gz-bridge
```

---

## ros2_control

```bash
sudo apt install -y \
    ros-jazzy-ros2-control \
    ros-jazzy-ros2-controllers \
    ros-jazzy-gz-ros2-control
```

---

## Navigation2

```bash
sudo apt install -y \
    ros-jazzy-navigation2 \
    ros-jazzy-nav2-bringup
```

---

## Localization and Mapping

```bash
sudo apt install -y \
    ros-jazzy-slam-toolbox \
    ros-jazzy-nav2-map-server \
    ros-jazzy-nav2-amcl
```

---

## Teleoperation

```bash
sudo apt install -y \
    ros-jazzy-joy \
    ros-jazzy-teleop-twist-keyboard \
    ros-jazzy-teleop-twist-joy
```

---

## Diagnostics

```bash
sudo apt install -y \
    ros-jazzy-tf2-tools \
    ros-jazzy-rqt \
    ros-jazzy-rqt-graph
```

---

# Clone the Repository

SSH

```bash
mkdir -p ~/AMR-Project

cd ~/AMR-Project

git clone git@github.com:Salim-MSI/Autonomous-Mobile-Robot.git
```

HTTPS

```bash
git clone https://github.com/Salim-MSI/Autonomous-Mobile-Robot.git
```

Move into the ROS workspace:

```bash
cd Autonomous-Mobile-Robot/ros2_ws
```

---

# Install Workspace Dependencies

```bash
source /opt/ros/jazzy/setup.bash

rosdep install \
    --from-paths src \
    --ignore-src \
    --rosdistro jazzy \
    -r \
    -y
```

All package dependencies should be declared in each package.xml.

---

# Build the Workspace

```bash
cd ~/AMR-Project/Autonomous-Mobile-Robot/ros2_ws

source /opt/ros/jazzy/setup.bash

colcon build --symlink-install
```

After a successful build:

```bash
source install/setup.bash
```

To automatically source the workspace:

```bash
echo "source ~/AMR-Project/Autonomous-Mobile-Robot/ros2_ws/install/setup.bash" >> ~/.bashrc

source ~/.bashrc
```

---

# Verify the Installation

Check that all AMR packages are visible:

```bash
ros2 pkg list | grep '^amr_'
```

Typical output:

```text
amr_bringup
amr_description
amr_simulation
amr_slam
amr_localization
amr_navigation
amr_joystick_bridge
```

Verify important external packages:

```bash
ros2 pkg prefix nav2_bringup

ros2 pkg prefix slam_toolbox

ros2 pkg prefix ros_gz_sim

ros2 pkg prefix robot_state_publisher
```

---

# Quick Functional Test

Launch the simulation:

```bash
ros2 launch amr_bringup simulation.launch.py
```

Open another terminal:

```bash
source install/setup.bash

ros2 node list
```

You should see several ROS nodes including:

- robot_state_publisher
- controller_manager
- joint_state_broadcaster
- diff_drive_controller

---

# Clean Rebuild

Whenever installation rules, package names, or CMake files change:

```bash
cd ~/AMR-Project/Autonomous-Mobile-Robot/ros2_ws

rm -rf build install log

source /opt/ros/jazzy/setup.bash

colcon build --symlink-install

source install/setup.bash
```

---

# Common Verification Commands

Workspace

```bash
ros2 pkg list | grep amr
```

Topics

```bash
ros2 topic list
```

Nodes

```bash
ros2 node list
```

TF

```bash
ros2 run tf2_tools view_frames
```

Controllers

```bash
ros2 control list_controllers
```

Robot description

```bash
ros2 param get /robot_state_publisher robot_description
```

---

# Troubleshooting

## `/opt/ros/jazzy/setup.bash` not found

ROS 2 is not installed correctly.

Verify:

```bash
ls /opt/ros
```

---

## Packages are missing

Run:

```bash
rosdep install \
    --from-paths src \
    --ignore-src \
    -r \
    -y
```

---

## Build fails

Perform a clean rebuild:

```bash
rm -rf build install log

colcon build --symlink-install
```

---

## ROS packages are not found

Verify that the workspace is sourced:

```bash
source install/setup.bash
```

---

## WSL networking problems

Retrieve the current WSL IP:

```bash
hostname -I | awk '{print $1}'
```

The address may change after restarting Windows or WSL.

---

# Next Steps

Once the installation is complete, continue with:

1. **SIMULATION.md**
2. **SLAM.md**
3. **LOCALIZATION.md**
4. **NAV2.md**
5. **JOYSTICK.md**