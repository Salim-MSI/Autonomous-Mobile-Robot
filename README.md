# Autonomous Mobile Robot (AMR)

<p align="center">

Autonomous Mobile Robot platform built with **ROS 2 Jazzy**, **Gazebo Harmonic**, **ros2_control**, **Navigation2**, **SLAM Toolbox**, **Computer Vision**, and **Embedded C++**.

Designed to bridge robotics, AI, embedded systems, and modern software engineering through a modular architecture that runs both in simulation and on a real robot.

</p>

---

## Overview

This repository contains the complete software stack of an autonomous differential-drive mobile robot.

The objective is to build an industrial-grade robotics platform capable of:

- autonomous navigation
- simultaneous localization and mapping (SLAM)
- localization on pre-built maps
- obstacle avoidance
- embedded motor control
- computer vision
- object and human detection
- web-based monitoring
- API-based mission control

The project is developed incrementally:

```
Simulation
        ↓
Embedded firmware
        ↓
Localization
        ↓
Navigation
        ↓
Computer Vision
        ↓
Artificial Intelligence
        ↓
Real Robot
```

---

# Main Features

Current features include:

- Differential-drive robot model
- URDF/Xacro robot description
- Gazebo Harmonic simulation
- ros2_control integration
- LiDAR simulation
- SLAM Toolbox
- Map saving
- AMCL localization
- Navigation2
- Joystick teleoperation
- Keyboard teleoperation
- Modular ROS2 architecture

Planned features:

- Wheel encoders
- IMU sensor fusion
- Extended Kalman Filter
- RGB camera
- YOLO object detection
- Person tracking
- Safety supervisor
- FastAPI backend
- React dashboard
- Docker deployment
- Continuous Integration

---

# Software Architecture

```
                        Web Dashboard
                              │
                              ▼
                         FastAPI Backend
                              │
                              ▼
                        ROS 2 Bringup
                              │
      ┌───────────────┬───────────────┬──────────────┐
      │               │               │              │
      ▼               ▼               ▼              ▼
Localization      Navigation      Perception      Control
      │               │               │              │
      └───────────────┴───────────────┴──────────────┘
                              │
                       ros2_control
                              │
                      Differential Drive
                              │
                      Gazebo / Real Robot
```

---

# Repository Structure

```
Autonomous-Mobile-Robot/

backend/
docker/
docs/
firmware/
frontend/
hardware/
scripts/
tests/

ros2_ws/
└── src/
    ├── amr_bringup
    ├── amr_description
    ├── amr_simulation
    ├── amr_slam
    ├── amr_localization
    ├── amr_navigation
    ├── amr_joystick_bridge
    └── ...
```

---

# Technologies

## Robotics

- ROS 2 Jazzy
- Gazebo Harmonic
- ros2_control
- Navigation2
- SLAM Toolbox
- robot_localization
- RViz2
- TF2
- URDF
- Xacro

## Embedded

- C++
- ESP32
- STM32
- PlatformIO
- FreeRTOS

## Artificial Intelligence

- PyTorch
- OpenCV
- YOLO
- ONNX Runtime

## Backend

- FastAPI
- WebSockets

## Frontend

- React
- Next.js

## DevOps

- Docker
- Docker Compose
- GitHub Actions

---

# Quick Start

Clone the repository

```bash
git clone git@github.com:Salim-MSI/Autonomous-Mobile-Robot.git
cd Autonomous-Mobile-Robot/ros2_ws
```

Install dependencies

```bash
rosdep install \
  --from-paths src \
  --ignore-src \
  --rosdistro jazzy \
  -r -y
```

Build

```bash
colcon build --symlink-install
```

Source the workspace

```bash
source install/setup.bash
```

Launch the simulation

```bash
ros2 launch amr_bringup simulation.launch.py
```

---

# Documentation

| Guide | Description |
|--------|-------------|
| INSTALLATION.md | Complete installation procedure |
| SIMULATION.md | Gazebo simulation |
| SLAM.md | Mapping using SLAM Toolbox |
| LOCALIZATION.md | AMCL localization |
| NAV2.md | Autonomous navigation |
| JOYSTICK.md | Windows joystick bridge |
| TROUBLESHOOTING.md | Common issues |
| ARCHITECTURE.md | Software architecture |
| SPECIFICATIONS.md | System specifications |

---

# Development Status

| Module | Status |
|---------|--------|
| Repository | ✅ |
| Documentation | ✅ |
| URDF | ✅ |
| Gazebo | ✅ |
| ros2_control | ✅ |
| LiDAR | ✅ |
| SLAM | ✅ |
| Localization | ✅ |
| Navigation | ✅ |
| Camera | 🟡 |
| Perception | ⬜ |
| YOLO | ⬜ |
| Firmware | ⬜ |
| EKF | ⬜ |
| Backend | ⬜ |
| Dashboard | ⬜ |
| Docker | ⬜ |
| Hardware | ⬜ |

---

# Roadmap

Phase 1
- Simulation
- Robot description
- ros2_control
- LiDAR
- SLAM

Phase 2
- Localization
- Navigation
- Sensor Fusion
- Embedded firmware

Phase 3
- Computer Vision
- Object Detection
- Human Tracking

Phase 4
- REST API
- Web Dashboard
- Docker Deployment

Phase 5
- Physical Robot
- Field Testing

---

# Project Goals

This project aims to demonstrate modern robotics software engineering by combining:

- Autonomous Robotics
- Artificial Intelligence
- Embedded Systems
- Computer Vision
- Software Architecture
- MLOps
- DevOps
- Continuous Integration
- Testing
- Documentation

The software is designed to remain modular, reusable, and maintainable throughout the transition from simulation to the physical robot.

---

# License

This project is distributed under the Apache 2.0 License.

---

# Author

**Salim Mansouri**

Robotics • Artificial Intelligence • Embedded Systems • Computer Vision