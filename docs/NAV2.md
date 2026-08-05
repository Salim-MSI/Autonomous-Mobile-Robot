# Navigation Guide

This guide explains how to perform autonomous navigation using **Navigation2 (Nav2)**.

The robot localizes itself using **AMCL**, plans a collision-free path, and follows it while avoiding obstacles.

---

# Table of Contents

- Overview
- Navigation Architecture
- Navigation Pipeline
- Requirements
- Launch Navigation
- Navigation Workflow
- Nav2 Components
- Validation
- RViz Configuration
- Useful Commands
- Troubleshooting

---

# Overview

Navigation2 (Nav2) is the autonomous navigation framework for ROS 2.

It combines localization, global planning, local planning, obstacle avoidance, and recovery behaviors into a modular navigation stack.

This project uses:

- AMCL
- Map Server
- Planner Server
- Controller Server
- Behavior Server
- BT Navigator
- Velocity Smoother
- Lifecycle Manager

---

# Navigation Architecture

```
                  Goal
                   │
                   ▼
            BT Navigator
                   │
        ┌──────────┴──────────┐
        ▼                     ▼
 Planner Server        Behavior Server
        │                     │
        ▼                     ▼
  Global Path          Recovery Behaviors
        │
        ▼
 Controller Server
        │
        ▼
 Velocity Smoother
        │
        ▼
 diff_drive_controller
        │
        ▼
      Robot
```

---

# Navigation Pipeline

```
              Occupancy Map
                    │
                    ▼
               Global Planner
                    │
                    ▼
              Global Path
                    │
                    ▼
            Local Controller
                    │
                    ▼
          Velocity Commands
                    │
                    ▼
           diff_drive_controller
                    │
                    ▼
                 Robot
```

---

# Requirements

Before launching Navigation:

- Simulation works correctly.
- A map has been generated.
- Localization is operational.
- AMCL is active.
- Robot position is initialized.
- TF tree is valid.

Verify:

```bash
ros2 lifecycle get /map_server

ros2 lifecycle get /amcl
```

Expected:

```
active [3]
```

---

# Launch Navigation

```bash
ros2 launch amr_bringup simulation_navigation.launch.py
```

This launch starts:

- Gazebo Harmonic
- robot_state_publisher
- ros2_control
- LiDAR
- Map Server
- AMCL
- Navigation2
- RViz2

---

# Navigation Workflow

1. Launch the navigation stack.
2. Wait until the map appears.
3. Set the initial pose using **2D Pose Estimate**.
4. Wait for AMCL to converge.
5. Select **2D Goal Pose**.
6. Click the destination.
7. The robot computes and follows a path.

---

# Nav2 Components

## Map Server

Publishes the occupancy grid map.

Lifecycle node.

---

## AMCL

Provides localization.

Publishes:

```
map → odom
```

---

## Planner Server

Computes the global path.

Default planner:

```
NavFn
```

---

## Controller Server

Follows the path.

Default controller:

```
DWB
```

---

## Behavior Server

Recovery behaviors.

Examples:

- Spin
- Backup
- Wait

---

## Velocity Smoother

Smooths velocity commands before they reach the controller.

Publishes:

```
/diff_drive_controller/cmd_vel
```

---

## BT Navigator

Coordinates all navigation components using a Behavior Tree.

---

# Validation

## Verify lifecycle nodes

```bash
ros2 lifecycle get /planner_server

ros2 lifecycle get /controller_server

ros2 lifecycle get /behavior_server

ros2 lifecycle get /bt_navigator
```

Expected:

```
active [3]
```

---

## Verify the planner

```bash
ros2 node list
```

Expected:

```
planner_server
controller_server
behavior_server
velocity_smoother
bt_navigator
```

---

## Verify navigation action

```bash
ros2 action list
```

Expected:

```
/navigate_to_pose

/navigate_through_poses
```

---

## Verify velocity commands

```bash
ros2 topic echo /diff_drive_controller/cmd_vel
```

Velocity commands should be published while navigating.

---

## Verify odometry

```bash
ros2 topic echo /diff_drive_controller/odom
```

The robot pose should update continuously.

---

# RViz Configuration

For Navigation2 to operate correctly, RViz must be configured properly.

## Map

| Parameter | Value |
|-----------|-------|
| Topic | `/map` |
| Reliability | Reliable |
| Durability | Transient Local |

---

## Fixed Frame

```
map
```

---

## Navigation Goal

Use:

```
2D Goal Pose
```

Do **not** use:

```
2D Pose Estimate
```

except when initializing localization.

---

# Useful Commands

List nodes

```bash
ros2 node list
```

Lifecycle

```bash
ros2 lifecycle get /planner_server

ros2 lifecycle get /controller_server
```

Actions

```bash
ros2 action list
```

Topics

```bash
ros2 topic list
```

Controllers

```bash
ros2 control list_controllers
```

TF

```bash
ros2 run tf2_ros tf2_echo map base_link
```

---

# Troubleshooting

## No map received

Verify:

```bash
ros2 topic echo /map --once
```

If messages are received:

Configure the RViz Map display:

| Parameter | Value |
|-----------|-------|
| Reliability | Reliable |
| Durability | Transient Local |

---

## Robot does not move

Verify:

```bash
ros2 topic echo /diff_drive_controller/cmd_vel
```

No commands:

Navigation is not generating velocity commands.

Commands exist:

Verify:

```bash
ros2 topic echo /diff_drive_controller/odom
```

---

## Failed to make progress

Possible causes:

- Robot is blocked.
- Incorrect odometry.
- Velocity commands are not reaching the controller.
- Progress checker thresholds are too strict.

Verify:

```bash
ros2 topic echo /diff_drive_controller/cmd_vel

ros2 topic echo /diff_drive_controller/odom
```

---

## Action server is inactive

Verify lifecycle:

```bash
ros2 lifecycle get /bt_navigator

ros2 lifecycle get /planner_server

ros2 lifecycle get /controller_server
```

All navigation lifecycle nodes must be:

```
active [3]
```

---

## Initial pose cannot be transformed

Warning:

```
Failed to transform initial pose in time
```

This warning is usually temporary and occurs immediately after setting the initial pose.

It can generally be ignored if localization converges correctly afterwards.

---

## Robot immediately teleports

Most often, **2D Pose Estimate** was used instead of **2D Goal Pose**.

Remember:

- **2D Pose Estimate** initializes AMCL.
- **2D Goal Pose** starts autonomous navigation.

---

## Navigation goals are rejected

Check:

```bash
ros2 action list
```

Verify:

```bash
ros2 lifecycle get /bt_navigator
```

Expected:

```
active [3]
```

---

# Validation Checklist

Before considering Navigation complete:

- Simulation starts correctly.
- Map loads.
- Localization works.
- Initial pose can be set.
- All Nav2 lifecycle nodes are active.
- Goal can be sent.
- Global path is generated.
- Robot follows the path.
- Obstacle avoidance works.
- Recovery behaviors trigger when needed.
