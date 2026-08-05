# Software Architecture

This document describes the overall architecture of the Autonomous Mobile Robot (AMR) software stack.

The project follows a modular ROS 2 architecture where each subsystem is isolated into its own package. This design simplifies development, testing, maintenance, and future migration from simulation to the physical robot.

---

# Table of Contents

- High-Level Architecture
- ROS 2 Workspace
- Package Overview
- Runtime Architecture
- Data Flow
- TF Tree
- Navigation Stack
- Software Layers
- Hardware Architecture
- Simulation vs Real Robot
- Design Principles
- Future Architecture

---

# High-Level Architecture

```
                        User
                         │
                         ▼
               Web Dashboard (Future)
                         │
                         ▼
                   FastAPI (Future)
                         │
                         ▼
                  ROS 2 Bringup
                         │
 ┌──────────────┬──────────────┬──────────────┐
 │              │              │              │
 ▼              ▼              ▼              ▼
Description  Simulation  Localization  Navigation
 │              │              │              │
 └──────────────┴──────────────┴──────────────┘
                         │
                         ▼
                   ros2_control
                         │
                         ▼
                Differential Drive
                         │
                         ▼
                 Gazebo / Real Robot
```

---

# ROS 2 Workspace

```
ros2_ws
└── src
    ├── amr_bringup
    ├── amr_description
    ├── amr_simulation
    ├── amr_slam
    ├── amr_localization
    ├── amr_navigation
    ├── amr_joystick_bridge
    └── ...
```

Each package has a single responsibility.

---

# Package Overview

## amr_bringup

Responsible for launching the complete robot stack.

Contains:

- Simulation launch files
- SLAM launch files
- Localization launch files
- Navigation launch files
- Teleoperation launch files

---

## amr_description

Robot description.

Contains:

- URDF
- Xacro
- Meshes
- ros2_control description
- Sensor definitions

---

## amr_simulation

Simulation environment.

Contains:

- Gazebo worlds
- Simulation launch files

---

## amr_slam

Online mapping.

Contains:

- SLAM Toolbox configuration
- RViz configuration

---

## amr_localization

Robot localization.

Contains:

- AMCL configuration
- Map Server
- Maps
- RViz configuration

---

## amr_navigation

Autonomous navigation.

Contains:

- Navigation2 parameters
- Planner configuration
- Controller configuration
- Costmaps
- RViz configuration

---

## amr_joystick_bridge

UDP bridge between Windows and ROS 2.

Receives joystick commands over UDP and publishes velocity commands to ROS.

---

# Runtime Architecture

```
                  Launch File
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
                gz_ros2_control
                       │
                       ▼
             controller_manager
                       │
         ┌─────────────┴─────────────┐
         ▼                           ▼
joint_state_broadcaster      diff_drive_controller
         │                           │
         └─────────────┬─────────────┘
                       ▼
                     Robot
```

---

# Data Flow

```
LiDAR

↓

/scan

↓

SLAM Toolbox / AMCL

↓

map → odom

↓

Navigation2

↓

Planner

↓

Controller

↓

Velocity Smoother

↓

/diff_drive_controller/cmd_vel

↓

diff_drive_controller

↓

Robot
```

---

# TF Tree

Expected transform hierarchy:

```
map
 │
odom
 │
base_link
 ├── chassis
 ├── lidar_link
 ├── left_wheel
 ├── right_wheel
 └── caster_wheel
```

Frame responsibilities:

| Frame | Published By |
|--------|--------------|
| map | AMCL |
| odom | diff_drive_controller |
| base_link | robot_state_publisher |
| sensor frames | robot_state_publisher |

---

# Navigation Stack

```
Goal

↓

BT Navigator

↓

Planner Server

↓

Controller Server

↓

Velocity Smoother

↓

diff_drive_controller

↓

Robot
```

Main components:

- BT Navigator
- Planner Server
- Controller Server
- Behavior Server
- Velocity Smoother
- Lifecycle Manager

---

# Software Layers

```
Application Layer
│
├── Bringup
├── Dashboard (Future)
├── API (Future)
│
Navigation Layer
│
├── Nav2
├── AMCL
├── SLAM
│
Robot Layer
│
├── robot_state_publisher
├── ros2_control
├── diff_drive_controller
│
Hardware Layer
│
├── Motors
├── Encoders
├── LiDAR
├── Camera
├── IMU
```

---

# Hardware Architecture

```
                    Raspberry Pi 5
                          │
      ┌───────────────────┼────────────────────┐
      ▼                   ▼                    ▼
    LiDAR               Camera               IMU
      │
      ▼
 ros2_control
      │
      ▼
  ESP32 / STM32
      │
      ▼
 Motor Driver
      │
      ▼
 Differential Drive
```

Future hardware additions:

- RGB camera
- RGB-D camera
- IMU
- Wheel encoders
- Emergency stop
- Battery monitoring

---

# Simulation vs Real Robot

Simulation:

```
Gazebo

↓

ros2_control

↓

Simulated Sensors

↓

Navigation
```

Real Robot:

```
Physical Sensors

↓

ROS Drivers

↓

ros2_control

↓

Navigation
```

The software stack remains identical.

Only the hardware interface changes.

---

# Design Principles

The project follows several software engineering principles:

- Modular package organization
- Separation of responsibilities
- Reusable launch files
- Parameterized configuration
- Hardware abstraction
- Simulation-first development
- Incremental integration
- Clear documentation

---

# Future Architecture

Planned software components:

```
Robot

↓

ROS 2

↓

Computer Vision

↓

YOLO

↓

Object Tracking

↓

Mission Manager

↓

FastAPI

↓

Web Dashboard

↓

Remote Monitoring
```

Future technologies:

- Docker
- Docker Compose
- GitHub Actions
- EKF Sensor Fusion
- Camera Perception
- Person Detection
- Object Detection
- Mission Scheduler
- REST API
- WebSocket
- React Dashboard

---

# Architecture Goals

The architecture has been designed to:

- Keep each package independent.
- Allow simulation and real hardware to share the same software stack.
- Minimize coupling between components.
- Simplify debugging and testing.
- Facilitate future extensions.
- Support modern robotics development practices.