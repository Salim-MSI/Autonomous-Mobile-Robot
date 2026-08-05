# Joystick Guide

This guide explains how to remotely control the robot using a gamepad connected to a Windows computer.

Unlike a standard ROS 2 joystick setup, this project uses a lightweight UDP bridge between Windows and the ROS 2 workspace running under WSL2.

---

# Table of Contents

- Overview
- Architecture
- Communication Pipeline
- Requirements
- Windows Setup
- WSL Setup
- Launch the Joystick
- Validation
- Useful Commands
- Troubleshooting

---

# Overview

The joystick system allows the robot to be driven from Windows while the ROS 2 stack runs inside WSL2.

The communication is performed over UDP.

Advantages:

- No ROS installation on Windows.
- Low latency.
- Lightweight protocol.
- Compatible with any Windows gamepad.
- Works over Wi-Fi or Ethernet.

---

# Architecture

```
Xbox Controller
       │
       ▼
Windows Application
(amr_joystick_sender)
       │
       ▼
UDP
       │
       ▼
WSL2
       │
       ▼
udp_joystick_node
       │
       ▼
/diff_drive_controller/cmd_vel
       │
       ▼
diff_drive_controller
       │
       ▼
Robot
```

---

# Communication Pipeline

```
Gamepad

↓

Windows Sender

↓

UDP

↓

WSL Network

↓

UDP Bridge

↓

ROS 2

↓

diff_drive_controller

↓

Robot
```

---

# Requirements

Before using the joystick:

- Windows application compiled.
- ROS workspace built.
- Simulation running.
- UDP port available.
- WSL networking operational.

---
# Operating Procedure

1. Launch the Windows joystick sender.
2. Enter the current WSL IP address.
3. Connect to the robot.
4. **Press and hold the Enable button.**
5. Move the joysticks to drive the robot.
6. Release the Enable button to stop immediately.

# Windows Setup

Launch the Windows joystick sender.

The application sends velocity commands to the WSL IP address using UDP.

Retrieve the WSL IP:

```bash
hostname -I
```

Typical output:

```
172.xx.xx.xx
```

Use the first address in the Windows application.

> **Important**
>
> The WSL IP address changes after restarting Windows or WSL.
> Always verify the address before launching the sender.

---

# WSL Setup

Build the workspace:

```bash
colcon build --symlink-install
```

Source the workspace:

```bash
source install/setup.bash
```

---

# Launch the Joystick

Start the bridge:

```bash
ros2 launch amr_bringup joystick.launch.py use_udp_bridge:=True
```

---

# Validation

Verify the bridge is running:

```bash
ros2 node list
```

Expected:

```
/udp_joystick_node
```

---

Verify velocity commands:

```bash
ros2 topic echo /diff_drive_controller/cmd_vel
```

Moving the joystick should publish velocity commands.

---

Verify robot motion

The robot should respond smoothly to joystick inputs.

If communication stops, the robot automatically receives a zero velocity command after the configured timeout.

---

# Enable Button

The Windows application includes an **Enable** button acting as a dead-man switch.

> **Important**
>
> The **Enable** button must remain pressed while driving the robot.
>
> When the button is released, the application immediately sends zero velocity commands, causing the robot to stop safely.

This safety mechanism prevents unintended robot motion if the operator releases the controls.

---

# Parameters

The bridge exposes several configurable parameters.

| Parameter | Description |
|-----------|-------------|
| `port` | UDP listening port |
| `cmd_vel_topic` | Velocity command topic |
| `command_timeout` | Automatic stop timeout |
| `max_linear_speed` | Maximum linear speed |
| `max_angular_speed` | Maximum angular speed |

Example:

```bash
ros2 param list /udp_joystick_node
```

---

# Useful Commands

List nodes

```bash
ros2 node list
```

Topics

```bash
ros2 topic list
```

Monitor velocity commands

```bash
ros2 topic echo /diff_drive_controller/cmd_vel
```

Check topic frequency

```bash
ros2 topic hz /diff_drive_controller/cmd_vel
```

View bridge parameters

```bash
ros2 param list /udp_joystick_node
```

---

# Safety Features

The joystick bridge includes several safety mechanisms.

## Dead-Man Switch

The Windows application implements a **dead-man switch** using the **Enable** button.

The operator must keep the button pressed while driving the robot.

When the button is released:

- the sender immediately transmits zero velocity commands;
- the robot stops;
- navigation commands are cancelled.

This prevents unintended robot motion.

---

## Communication Timeout

If the UDP bridge stops receiving packets for longer than the configured timeout, it automatically publishes a zero velocity command.

This protects against:

- Windows application crashes;
- Wi-Fi interruptions;
- Ethernet disconnections;
- unexpected communication loss.

---

# Troubleshooting

## Robot does not move

Verify that the bridge is running:

```bash
ros2 node list
```

Expected:

```
/udp_joystick_node
```

---

## No commands received

Verify:

```bash
ros2 topic echo /diff_drive_controller/cmd_vel
```

If no messages are received:

- Check the Windows sender.
- Verify the UDP port.
- Verify the WSL IP address.

---

## Wrong WSL IP

Retrieve the current address:

```bash
hostname -I
```

Update the Windows application accordingly.

---

## Port already in use

Verify:

```bash
ss -lun | grep 5005
```

If another process is using the port, stop it or choose another port.

---

## Robot continues moving

Normally the bridge publishes a zero velocity command after the timeout.

Verify:

```bash
ros2 param get /udp_joystick_node command_timeout
```

Increase the timeout if necessary.

---

## Commands are ignored

Verify:

```bash
ros2 topic echo /diff_drive_controller/cmd_vel
```

If commands are published but the robot does not move:

```bash
ros2 control list_controllers
```

Expected:

```
joint_state_broadcaster    active
diff_drive_controller      active
```

---

# Validation Checklist

Before continuing:

- Windows sender is running.
- WSL IP is correct.
- UDP bridge is running.
- `/diff_drive_controller/cmd_vel` receives commands.
- Robot moves correctly.
- Automatic stop works after timeout.
- No packet loss is observed.
