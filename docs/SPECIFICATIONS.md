# System Specifications

This document defines the functional and technical specifications of the Autonomous Mobile Robot (AMR).

It describes the system objectives, hardware platform, software architecture, operational requirements, and future extensions.

---

# Table of Contents

- Project Overview
- Objectives
- Functional Requirements
- Non-Functional Requirements
- Hardware Specifications
- Software Specifications
- Robot Characteristics
- Sensors
- Actuators
- Software Stack
- Communication
- Simulation
- Performance Targets
- Safety
- Future Improvements

---

# Project Overview

The Autonomous Mobile Robot (AMR) is a differential-drive robotic platform developed using ROS 2 Jazzy.

The project aims to provide a modular robotics platform capable of autonomous navigation in indoor environments while remaining easily extensible for research and future industrial applications.

Development follows a **simulation-first** approach before deployment on physical hardware.

---

# Objectives

The primary objectives are:

- Build a modular ROS 2 robotics platform.
- Simulate the complete robot in Gazebo.
- Generate 2D maps using SLAM.
- Localize on previously generated maps.
- Navigate autonomously.
- Support manual teleoperation.
- Integrate embedded motor control.
- Add computer vision capabilities.
- Deploy the software on a physical robot.

---

# Functional Requirements

The robot shall:

- Be controllable manually.
- Perform autonomous navigation.
- Build 2D occupancy maps.
- Localize using AMCL.
- Avoid static obstacles.
- Publish wheel odometry.
- Publish TF transforms.
- Publish LiDAR data.
- Execute velocity commands.
- Stop automatically when communication is lost.
- Support simulation and real hardware with the same software architecture.

---

# Non-Functional Requirements

The system shall be:

- Modular
- Maintainable
- Reusable
- Extensible
- Portable
- Well documented
- Testable
- Open-source friendly

The software shall follow ROS 2 best practices.

---

# Hardware Specifications

| Component | Specification |
|-----------|---------------|
| Drive type | Differential drive |
| Main computer | Raspberry Pi 5 |
| Microcontroller | ESP32 / STM32 |
| Operating System | Ubuntu 24.04 |
| ROS Distribution | ROS 2 Jazzy |

---

# Robot Characteristics

| Parameter | Value |
|-----------|-------|
| Drive configuration | Differential drive |
| Number of driven wheels | 2 |
| Caster wheel | 1 |
| Indoor operation | Yes |
| Outdoor operation | Planned |
| Simulation support | Yes |

---

# Sensors

Current sensors:

| Sensor | Status |
|---------|--------|
| LiDAR | Implemented |

Planned sensors:

- RGB camera
- RGB-D camera
- IMU
- Wheel encoders
- Battery monitor

---

# Actuators

Current actuators:

- Two DC motors
- Differential drive

Future additions:

- Pan/Tilt camera
- Robotic arm (optional)

---

# Software Specifications

The project is built around ROS 2 Jazzy.

Current packages include:

- amr_bringup
- amr_description
- amr_simulation
- amr_slam
- amr_localization
- amr_navigation
- amr_joystick_bridge

---

# Software Stack

| Layer | Technology |
|--------|------------|
| Middleware | ROS 2 Jazzy |
| Simulation | Gazebo Harmonic |
| Robot Description | URDF / Xacro |
| Controllers | ros2_control |
| Mapping | SLAM Toolbox |
| Localization | AMCL |
| Navigation | Navigation2 |
| Visualization | RViz2 |

Future technologies:

- OpenCV
- PyTorch
- FastAPI
- React
- Docker
- Docker Compose

---

# Communication

The system uses ROS 2 topics, services, actions, and TF.

Main communication interfaces:

| Interface | Purpose |
|------------|---------|
| Topics | Sensor data and commands |
| TF | Coordinate transforms |
| Services | Configuration |
| Actions | Navigation goals |

---

# Simulation

Simulation is performed using:

- Gazebo Harmonic
- ros2_control
- RViz2

The simulated robot shares the same software architecture as the physical robot.

---

# Performance Targets

| Metric | Target |
|--------|--------|
| LiDAR frequency | ~10 Hz |
| Controller frequency | 20 Hz |
| Localization | Real-time |
| Navigation | Real-time |
| Mapping | Real-time |

---

# Safety

The robot includes several software safety mechanisms:

- Automatic stop on communication loss.
- Velocity limiting.
- Obstacle avoidance.
- Recovery behaviors.
- Emergency stop (planned).

Future safety features:

- Battery monitoring.
- Collision monitoring.
- Watchdog supervision.
- Hardware emergency stop.

---

# Future Improvements

Planned developments include:

- Extended Kalman Filter (EKF).
- IMU integration.
- Wheel encoder fusion.
- RGB camera support.
- Object detection (YOLO).
- Person detection and tracking.
- FastAPI backend.
- React web interface.
- Docker deployment.
- Continuous Integration (GitHub Actions).
- Physical robot validation.
- Multi-robot support.

---

# Development Status

| Module | Status |
|---------|--------|
| Documentation | ✅ |
| URDF | ✅ |
| Gazebo | ✅ |
| ros2_control | ✅ |
| LiDAR | ✅ |
| SLAM | ✅ |
| Localization | ✅ |
| Navigation | ✅ |
| Manual Control | ✅ |
| Embedded Firmware | 🔄 |
| Computer Vision | ⏳ |
| AI | ⏳ |
| Docker | ⏳ |
| Real Robot | ⏳ |

---

# References

- ROS 2 Jazzy Documentation
- Navigation2
- SLAM Toolbox
- Gazebo Harmonic
- ros2_control