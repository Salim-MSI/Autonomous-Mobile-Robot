# Localization Guide

This guide explains how to localize the robot on a previously generated map using **Adaptive Monte Carlo Localization (AMCL)**.

Localization is the process of estimating the robot's pose within a known environment. Unlike SLAM, the map is already available and remains fixed during operation.

---

# Table of Contents

- Overview
- Localization Pipeline
- Requirements
- Launch Localization
- Localization Workflow
- AMCL Overview
- TF Tree
- Validation
- Useful Commands
- Troubleshooting

---

# Overview

The localization system estimates the robot's pose on a previously generated occupancy grid map.

This project uses:

- Nav2 Map Server
- AMCL (Adaptive Monte Carlo Localization)
- TF2
- LiDAR
- Wheel Odometry

The localization result is later used by Navigation2 to plan and execute autonomous paths.

---

# Localization Pipeline

```
              Saved Map
                  │
                  ▼
            Nav2 Map Server
                  │
                  ▼
               Occupancy Grid
                  │
                  ▼
LiDAR ───────► AMCL ◄────── Odometry
                  │
                  ▼
             map → odom TF
                  │
                  ▼
            Robot Localization
```

---

# Requirements

Before starting localization:

- Simulation is operational
- A valid map has been generated
- LiDAR publishes `/scan`
- Odometry is available
- TF tree is valid

Verify the map exists:

```bash
ls ~/AMR-Project/Autonomous-Mobile-Robot/ros2_ws/src/amr_localization/maps
```

Expected:

```
test_world.yaml
test_world.pgm
```

---

# Launch Localization

Launch the localization stack:

```bash
ros2 launch amr_bringup simulation_localization.launch.py
```

The following components are started:

- Gazebo Harmonic
- robot_state_publisher
- ros2_control
- LiDAR
- Map Server
- AMCL
- RViz2

---

# Localization Workflow

1. Launch the simulation.
2. Wait until the map appears in RViz.
3. Click **2D Pose Estimate**.
4. Place the robot approximately at its real position.
5. Rotate the arrow to match the robot orientation.
6. Drive the robot a short distance.
7. Observe the AMCL particle cloud converging.

Once the particle cloud converges, the robot is considered localized.

---

# AMCL Overview

AMCL estimates the robot pose using a particle filter.

Inputs:

- Occupancy grid map
- LaserScan
- Wheel odometry

Outputs:

- Robot pose
- Particle cloud
- map → odom transform

AMCL continuously compares LiDAR measurements with the known map to refine the robot position.

---

# TF Tree

Expected TF hierarchy:

```
map
 │
odom
 │
base_link
 ├── lidar_link
 ├── left_wheel
 ├── right_wheel
 └── chassis
```

The transform:

```
map → odom
```

is published by **AMCL**.

The transform:

```
odom → base_link
```

is published by the **diff_drive_controller**.

---

# Validation

## Verify AMCL

```bash
ros2 node list | grep amcl
```

Expected:

```
/amcl
```

---

## Verify the Map Server

```bash
ros2 lifecycle get /map_server
```

Expected:

```
active [3]
```

---

## Verify AMCL

```bash
ros2 lifecycle get /amcl
```

Expected:

```
active [3]
```

---

## Verify the map

```bash
ros2 topic echo /map --once
```

A valid OccupancyGrid message should be received.

---

## Verify localization

```bash
ros2 topic echo /amcl_pose
```

The pose should change as the robot moves.

---

## Verify TF

```bash
ros2 run tf2_ros tf2_echo map base_link
```

The pose should update continuously while driving.

---

# Useful Topics

| Topic | Description |
|--------|-------------|
| `/map` | Occupancy grid |
| `/scan` | LiDAR data |
| `/amcl_pose` | Estimated robot pose |
| `/particle_cloud` | AMCL particles |
| `/tf` | Robot transforms |

---

# Useful Commands

List nodes:

```bash
ros2 node list
```

Lifecycle status:

```bash
ros2 lifecycle get /map_server

ros2 lifecycle get /amcl
```

Check localization:

```bash
ros2 topic echo /amcl_pose
```

Check TF:

```bash
ros2 run tf2_ros tf2_echo map base_link
```

Check odometry:

```bash
ros2 topic echo /diff_drive_controller/odom
```

---

# Troubleshooting

## No map appears in RViz

Verify:

```bash
ros2 topic echo /map --once
```

If no message is received:

- Check that the map server is active.
- Verify the map path.
- Verify the YAML file exists.

---

## AMCL does not localize

Verify:

```bash
ros2 lifecycle get /amcl
```

The node must be **active**.

---

## "AMCL cannot publish a pose"

This message usually indicates that the initial pose has not been set.

Solution:

Use **2D Pose Estimate** in RViz.

---

## "Failed to transform initial pose in time"

This warning often occurs immediately after setting the initial pose.

It is generally harmless if localization starts correctly afterwards.

---

## "No map received"

Possible causes:

- Map server not active.
- Wrong map file.
- Incorrect QoS in RViz.

Ensure the **Map** display uses **Transient Local** durability.

---

## Robot jumps to another position

Possible causes:

- Incorrect initial pose.
- Poor map quality.
- Wrong odometry.
- Incorrect TF tree.

---

## Localization drifts

Possible causes:

- Incorrect wheel odometry.
- Poor LiDAR calibration.
- Low-quality map.
- Incorrect AMCL parameters.

---

# Validation Checklist

Before proceeding to Navigation:

- Simulation launches successfully.
- Map loads correctly.
- Map server is active.
- AMCL is active.
- Initial pose can be set.
- Particle cloud converges.
- `/amcl_pose` updates.
- `map → odom` transform exists.
- Robot position remains stable while stopped.

---

> **Note**
>
> The `/map` topic is published with **Transient Local** durability.
> RViz must use the same durability policy to receive previously published maps.

# Next Steps

Once localization is working correctly:

1. **NAV2.md** — Configure autonomous navigation.
2. Send navigation goals using **2D Goal Pose**.
3. Validate obstacle avoidance and path planning.