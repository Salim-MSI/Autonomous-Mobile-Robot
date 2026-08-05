# Simulation Guide

This document explains how to launch, validate, and troubleshoot the AMR simulation.

The simulation is based on **Gazebo Harmonic**, **ros2_control**, and **ROS 2 Jazzy**. It reproduces the robot software stack used on the physical platform, allowing development and testing before deployment on real hardware.

---

# Table of Contents

- Overview
- Simulation Architecture
- Requirements
- Launch the Simulation
- Simulation Workflow
- Validate the Simulation
- Robot Interfaces
- ROS Graph
- TF Tree
- Useful Commands
- Troubleshooting

---

# Overview

The simulation provides a complete virtual environment for developing and testing the robot without requiring physical hardware.

Current simulated components include:

- Differential-drive mobile robot
- URDF/Xacro robot model
- ros2_control
- Differential drive controller
- LiDAR sensor
- Gazebo Harmonic physics
- RViz visualization

Future versions will include:

- RGB camera
- IMU
- Wheel encoders
- RGB-D camera
- GPS (optional)

---

# Simulation Architecture

```
                 ROS 2
                   │
                   ▼
         robot_state_publisher
                   │
                   ▼
             Robot Description
                   │
                   ▼
             Gazebo Harmonic
                   │
        gz_ros2_control plugin
                   │
                   ▼
          controller_manager
                   │
      ┌────────────┴────────────┐
      ▼                         ▼
joint_state_broadcaster   diff_drive_controller
      │                         │
      └────────────┬────────────┘
                   ▼
                Robot
```

---

# Requirements

Before launching the simulation:

- Workspace successfully built
- ROS 2 sourced
- Gazebo Harmonic installed
- ros2_control installed

Source the workspace:

```bash
source /opt/ros/jazzy/setup.bash
source install/setup.bash
```

---

# Launch the Simulation

Start the complete simulation:

```bash
ros2 launch amr_bringup simulation.launch.py
```

The following components are automatically started:

- Gazebo Harmonic
- robot_state_publisher
- ros2_control
- controller_manager
- joint_state_broadcaster
- diff_drive_controller
- RViz2 (optional)

---

# Simulation Workflow

```
URDF/Xacro
      │
      ▼
robot_state_publisher
      │
      ▼
Gazebo
      │
      ▼
ros2_control
      │
      ▼
Controllers
      │
      ▼
Joint States
```

---

# Validate the Simulation

## Robot Description

```bash
ros2 param get /robot_state_publisher robot_description
```

---

## Controllers

```bash
ros2 control list_controllers
```

Expected:

```
joint_state_broadcaster    active
diff_drive_controller      active
```

---

## Topics

```bash
ros2 topic list
```

Important topics include:

```
/joint_states
/robot_description
/tf
/tf_static
/scan
/diff_drive_controller/cmd_vel
/diff_drive_controller/odom
```

---

## TF Tree

Generate the TF tree:

```bash
ros2 run tf2_tools view_frames
```

Expected hierarchy:

```
odom
 │
base_link
 ├── lidar_link
 ├── left_wheel
 ├── right_wheel
 └── chassis
```

---

## Robot Motion

Publish a velocity command:

```bash
ros2 topic pub \
/diff_drive_controller/cmd_vel \
geometry_msgs/msg/TwistStamped \
"{header:{frame_id:'base_link'},twist:{linear:{x:0.2},angular:{z:0.0}}}"
```

The robot should move forward.

---

# Robot Interfaces

## Subscribed Topics

| Topic | Type | Description |
|--------|------|-------------|
| /diff_drive_controller/cmd_vel | TwistStamped | Velocity command |

---

## Published Topics

| Topic | Description |
|--------|-------------|
| /joint_states | Wheel states |
| /tf | Robot transforms |
| /odom | Robot odometry |
| /scan | LiDAR scan |

---

# Useful Commands

List nodes

```bash
ros2 node list
```

List topics

```bash
ros2 topic list
```

Check LiDAR frequency

```bash
ros2 topic hz /scan
```

Echo odometry

```bash
ros2 topic echo /diff_drive_controller/odom
```

Controllers

```bash
ros2 control list_controllers
```

---

# Troubleshooting

## Gazebo does not start

Check:

```bash
gz sim --version
```

---

## Robot does not appear

Verify:

```bash
ros2 param get /robot_state_publisher robot_description
```

---

## Controllers remain inactive

Check:

```bash
ros2 control list_controllers
```

Expected:

```
joint_state_broadcaster active
diff_drive_controller active
```

---

## Robot does not move

Verify that commands are published:

```bash
ros2 topic echo /diff_drive_controller/cmd_vel
```

Verify odometry:

```bash
ros2 topic echo /diff_drive_controller/odom
```

---

## No LiDAR data

Check:

```bash
ros2 topic hz /scan
```

Expected frequency:

```
≈ 8–10 Hz
```

---

## Missing TF frames

Generate the TF tree:

```bash
ros2 run tf2_tools view_frames
```

Verify:

```
odom
base_link
lidar_link
```

---

# Next Steps

Once the simulation is fully operational:

1. **SLAM.md** — Build a map using SLAM Toolbox.
2. **LOCALIZATION.md** — Localize the robot on a saved map.
3. **NAV2.md** — Perform autonomous navigation.
4. **JOYSTICK.md** — Drive the robot using a gamepad.