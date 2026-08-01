# Specifications — Autonomous Mobile Robot

## 1. Project Vision

Develop an autonomous differential-drive mobile robot capable of mapping indoor environments, localizing itself, navigating toward target destinations, avoiding obstacles, and detecting people or objects using onboard perception.

The project must first operate in simulation before being deployed on a physical robot. Its architecture should be modular, well documented, and fully testable.

---

## 2. Main Objectives

- Build a differential-drive mobile base.
- Control the motors using a C++ microcontroller firmware.
- Publish odometry and robot state to ROS 2.
- Perform 2D mapping using a LiDAR.
- Localize the robot on an existing map.
- Navigate autonomously using Nav2.
- Detect people and objects using a camera.
- Trigger safety behaviors based on perception.
- Monitor the robot through a REST API and a web dashboard.
- Deploy the main software services using Docker.
- Add testing, logging, and continuous integration.

---

## 3. Scope of the First Complete Release

### 3.1 Mandatory Features

1. Teleoperation using a keyboard or game controller.
2. Closed-loop wheel speed control using PID.
3. Wheel encoder acquisition.
4. Odometry estimation.
5. IMU integration.
6. Encoder and IMU sensor fusion.
7. 2D SLAM mapping.
8. Map saving and loading.
9. Autonomous localization.
10. Navigation to a target pose.
11. Static and dynamic obstacle avoidance.
12. Human detection.
13. Safety stop or speed reduction.
14. Robot state reporting (battery, velocity, position, errors).
15. REST API to send navigation goals and stop the robot.
16. Minimal monitoring dashboard.
17. Reproducible execution using Docker Compose.
18. Documentation and demonstration video.

---

## 4. Use Cases

### UC-01 — Teleoperation

The user sends velocity commands. The robot moves while respecting speed limits and emergency stop mechanisms.

### UC-02 — Mapping

The robot is teleoperated through an indoor environment and generates a 2D occupancy map that can be saved.

### UC-03 — Autonomous Navigation

The user selects a destination on the map. The robot plans a path, avoids obstacles, and reaches the target.

---

## 5. Functional Requirements

| ID | Requirement | Priority | Acceptance Criteria |
|----|-------------|---------:|---------------------|
| FR-01 | The robot shall receive `/cmd_vel` commands. | High | Commanded velocity is applied within 150 ms. |
| FR-02 | The firmware shall regulate the speed of each wheel. | High | Average tracking error below 10% during straight-line motion. |
| FR-03 | The system shall publish odometry. | High | Stable publication rate of at least 20 Hz. |
| FR-04 | The robot shall generate a 2D occupancy map. | High | A usable map of a room or corridor is produced. |
| FR-05 | The robot shall localize itself on an existing map. | High | Average localization error below 20 cm in a controlled indoor environment. |
| FR-06 | The robot shall reach a target pose. | High | At least 8 successful missions out of 10. |
| FR-07 | The robot shall avoid obstacles. | High | No collisions during validation scenarios. |
| FR-08 | The system shall detect people. | Medium | Real-time detection at a minimum of 10 FPS. |
| FR-09 | Hazard detection shall trigger a safety stop. | High | Robot stops within 300 ms after the decision is made. |
| FR-10 | The API shall expose the robot status. | Medium | `/status` endpoint available and documented. |
| FR-11 | The API shall allow navigation goals to be sent. | Medium | Goals can be submitted and tracked through the API. |
| FR-12 | The system shall log critical errors. | Medium | Timestamped logs are available for inspection. |

---

## 6. Non-Functional Requirements

| ID | Requirement | Target |
|----|-------------|--------|
| NFR-01 | Modularity | ROS 2 packages separated by responsibility. |
| NFR-02 | Maintainability | Modern C++, typed Python, coding standards enforced. |
| NFR-03 | Testability | Unit and integration tests available. |
| NFR-04 | Reproducibility | Fully documented installation and versioned containers. |
| NFR-05 | Safety | Independent hardware and software emergency stops. |
| NFR-06 | Robustness | Microcontroller watchdog and communication timeout. |
| NFR-07 | Performance | Motor control loop ≥100 Hz, odometry ≥20 Hz. |
| NFR-08 | Observability | Logging, ROS diagnostics, and system metrics. |
| NFR-09 | Portability | Full simulation available without physical hardware. |
| NFR-10 | Documentation | Architecture, installation, usage, and testing documented. |

---

## 7. Design Assumptions

- Primarily designed for indoor, relatively flat environments.
- Differential-drive base with two driven wheels and one or two caster wheels.
- Horizontally mounted 2D LiDAR.
- Forward-facing camera.
- Linux onboard computer running ROS 2.
- Dedicated microcontroller for real-time tasks.
- Communication between the onboard computer and microcontroller via USB serial, CAN, or micro-ROS.
- Initial release developed using ROS 2 Jazzy or Humble, depending on hardware compatibility.

---

## 8. Preliminary Hardware Targets

| Subsystem | Primary Choice | Alternative |
|-----------|----------------|-------------|
| Onboard Computer | Raspberry Pi 5 | Jetson Orin Nano |
| Microcontroller | ESP32 | STM32 Nucleo |
| LiDAR | RPLIDAR A1/A2 | YDLIDAR |
| Camera | USB RGB Camera | RGB-D Camera |
| IMU | BNO085 / ICM-20948 | MPU-9250 |
| Motors | Two DC motors with encoders | Equivalent geared motors |
| Motor Driver | Cytron MDDS30 / TB6612 (depending on power) | Compatible driver |
| Battery | Li-ion/LiPo with BMS | Commercial protected battery pack |
| Chassis | 3D-printed parts + aluminum profiles | Commercial mobile robot chassis |

The exact hardware references will be finalized after motor torque, power consumption, and budget calculations.

---

## 9. Initial Constraints

- Prototype budget: **€600–€1,200**
- Target weight: **5–12 kg**
- Maximum software speed: **0.5 m/s (indoor)**
- Target operating time: **60–120 minutes**
- Maximum width: **45 cm**
- Payload capacity: **at least 2 kg**
- Designed for flat indoor surfaces with small thresholds.
- Easily accessible hardware emergency stop button.

---

## 10. Planned ROS 2 Interfaces

### Main Topics

- `/cmd_vel`
- `/odom`
- `/joint_states`
- `/imu/data`
- `/scan`
- `/camera/image_raw`
- `/camera/camera_info`
- `/detections`
- `/battery_state`
- `/diagnostics`

### TF Frames

- `map`
- `odom`
- `base_link`
- `base_footprint`
- `laser_frame`
- `camera_link`
- `imu_link`
- `left_wheel_link`
- `right_wheel_link`

### Actions and Services

- Nav2 `NavigateToPose` action
- Software emergency stop service
- Error reset service
- Map save service

---

## 11. Version 1 Success Criteria

The project will be considered complete when:

1. A single command launches either the robot or the simulation.
2. The robot can generate a 2D map of an indoor environment.
3. The robot can localize itself on that map.
4. The robot reaches multiple navigation goals without collisions.
5. It detects a person and executes an appropriate safety behavior.
6. Its status is available through an external interface.
7. The main software components are tested and documented.
8. A demonstration video successfully reproduces all validation scenarios.