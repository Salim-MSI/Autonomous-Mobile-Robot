# Troubleshooting

This document lists the most common issues encountered while developing or using the Autonomous Mobile Robot (AMR) project, along with their causes and solutions.

---

# Table of Contents

- Workspace
- Build
- Gazebo
- ros2_control
- LiDAR
- SLAM
- Localization
- Navigation
- Joystick
- TF
- Networking (WSL)
- Useful Diagnostic Commands

---

# Workspace

## ROS packages cannot be found

### Symptoms

```
Package 'amr_xxx' not found
```

### Solution

Verify that the workspace has been sourced.

```bash
source /opt/ros/jazzy/setup.bash

source install/setup.bash
```

Verify:

```bash
ros2 pkg list | grep amr
```

---

## Package exists but changes are ignored

Clean the workspace.

```bash
rm -rf build install log

colcon build --symlink-install
```

---

# Build

## Build fails

Clean the workspace.

```bash
rm -rf build install log

colcon build --symlink-install
```

---

## Missing dependency

Run:

```bash
rosdep install \
    --from-paths src \
    --ignore-src \
    -r \
    -y
```

---

# Gazebo

## Robot does not appear

Verify:

```bash
ros2 param get \
/robot_state_publisher \
robot_description
```

---

## Gazebo starts but robot falls

Possible causes:

- Invalid inertia
- Wrong collision geometry
- Incorrect joint origin

Check the URDF.

---

## Robot wheels do not rotate

Verify controllers:

```bash
ros2 control list_controllers
```

Expected:

```
joint_state_broadcaster active

diff_drive_controller active
```

---

# ros2_control

## Controller inactive

Verify:

```bash
ros2 control list_controllers
```

Activate:

```bash
ros2 control switch_controllers \
--activate diff_drive_controller
```

---

## Controller manager missing

Verify:

```bash
ros2 node list
```

Expected:

```
controller_manager
```

---

# LiDAR

## No LiDAR data

Verify:

```bash
ros2 topic hz /scan
```

Expected:

```
≈ 8–10 Hz
```

---

## Scan contains only inf

Possible causes:

- Empty world
- Robot outside the environment
- Incorrect sensor position

---

# SLAM

## SLAM Toolbox not running

Verify:

```bash
ros2 node list
```

Expected:

```
/slam_toolbox
```

---

## Map cannot be saved

Use:

```bash
ros2 run nav2_map_server map_saver_cli \
-f \
~/AMR-Project/Autonomous-Mobile-Robot/ros2_ws/src/amr_localization/maps/test_world
```

---

## Generated map is empty

Possible causes:

- Robot never moved
- LiDAR not publishing
- SLAM not started

---

# Localization

## No map received

Verify:

```bash
ros2 topic echo /map --once
```

If messages are received:

Configure RViz:

| Parameter | Value |
|-----------|-------|
| Reliability | Reliable |
| Durability | Transient Local |

---

## Map Server inactive

Verify:

```bash
ros2 lifecycle get /map_server
```

Expected:

```
active [3]
```

---

## AMCL inactive

Verify:

```bash
ros2 lifecycle get /amcl
```

Expected:

```
active [3]
```

---

## AMCL cannot publish a pose

Cause:

Initial pose not initialized.

Solution:

Use

```
2D Pose Estimate
```

---

## Failed to transform initial pose in time

Example:

```
Lookup would require extrapolation into the future
```

Usually harmless immediately after clicking **2D Pose Estimate**.

---

# Navigation

## Robot does not move

Verify velocity commands:

```bash
ros2 topic echo \
/diff_drive_controller/cmd_vel
```

---

Verify odometry:

```bash
ros2 topic echo \
/diff_drive_controller/odom
```

---

## Failed to make progress

Possible causes:

- Robot blocked
- Bad odometry
- Velocity commands not reaching controller

Verify:

```bash
ros2 topic echo \
/diff_drive_controller/cmd_vel

ros2 topic echo \
/diff_drive_controller/odom
```

---

## Action server is inactive

Verify:

```bash
ros2 lifecycle get \
/planner_server

ros2 lifecycle get \
/controller_server

ros2 lifecycle get \
/bt_navigator
```

Expected:

```
active [3]
```

---

## Navigation lifecycle nodes remain inactive

Verify:

```bash
ros2 param get \
/lifecycle_manager_navigation \
node_names
```

Ensure every listed node exists:

```bash
ros2 node list
```

---

## Robot teleports

Cause:

Using

```
2D Pose Estimate
```

instead of

```
2D Goal Pose
```

---

## Goal rejected

Verify:

```bash
ros2 action list
```

Expected:

```
/navigate_to_pose
```

---

# Joystick

## UDP bridge not running

Verify:

```bash
ros2 node list
```

Expected:

```
udp_joystick_node
```

---

## Robot does not respond

Verify:

```bash
ros2 topic echo \
/diff_drive_controller/cmd_vel
```

---

## Wrong WSL IP

Retrieve:

```bash
hostname -I
```

Update the Windows sender.

---

## UDP port already in use

Verify:

```bash
ss -lun | grep 5005
```

---

## Automatic stop does not work

Verify:

```bash
ros2 param get \
/udp_joystick_node \
command_timeout
```

---

# TF

## Missing TF frames

Generate:

```bash
ros2 run tf2_tools view_frames
```

Expected hierarchy:

```
map

↓

odom

↓

base_link

↓

lidar_link
```

---

## Invalid frame ID

Example:

```
Invalid frame ID "map"
```

Verify:

```bash
ros2 topic echo /tf
```

Check:

- robot_state_publisher
- AMCL
- diff_drive_controller

---

# Networking (WSL)

## Windows cannot communicate with ROS

Retrieve WSL IP:

```bash
hostname -I
```

Use the first address.

---

## WSL IP changes

WSL assigns a new IP after every restart.

Always verify:

```bash
hostname -I
```

before launching the Windows sender.

---

# Useful Diagnostic Commands

Workspace

```bash
ros2 pkg list | grep amr
```

Nodes

```bash
ros2 node list
```

Topics

```bash
ros2 topic list
```

Actions

```bash
ros2 action list
```

Controllers

```bash
ros2 control list_controllers
```

TF

```bash
ros2 run tf2_tools view_frames
```

Lifecycle

```bash
ros2 lifecycle nodes
```

Controller Manager

```bash
ros2 control list_hardware_interfaces
```

LiDAR

```bash
ros2 topic hz /scan
```

Odometry

```bash
ros2 topic echo \
/diff_drive_controller/odom
```

Velocity Commands

```bash
ros2 topic echo \
/diff_drive_controller/cmd_vel
```

Map

```bash
ros2 topic echo \
/map --once
```

AMCL

```bash
ros2 topic echo \
/amcl_pose
```