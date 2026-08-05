# Joystick Control Guide

## 1. Architecture

The current development setup uses:

- the game controller connected to Windows;
- `amr_joystick_sender` executed from Windows PowerShell;
- the ROS 2 receiver/bridge executed inside WSL;
- UDP communication between Windows and the WSL network interface.

The IP address required by the Windows sender is the WSL IP address, not necessarily the normal Windows Wi-Fi or Ethernet address shown by `ipconfig`.

---

## 2. Important WSL IP Detail

Open a WSL Bash terminal and run:

```bash
hostname -I
```

Example output:

```text
172.25.64.1 172.18.0.1
```

Use the address associated with the active WSL interface. In most configurations, this is the first address returned.

To print only the first address:

```bash
hostname -I | awk '{print $1}'
```

Example:

```text
172.25.64.1
```

The WSL IP address can change when WSL or Windows restarts. Retrieve it again whenever the joystick sender can no longer reach the ROS 2 bridge.

Do not blindly use the address returned by Windows `ipconfig`: the sender must target the WSL address on which the bridge is listening.

---

## 3. Recommended Startup Order

Use the following order every time.

### Terminal 1 — Start the robot or simulation in WSL

```bash
cd ~/AMR-Project/Autonomous-Mobile-Robot/ros2_ws

source /opt/ros/jazzy/setup.bash
source install/setup.bash

# Launch the required robot or simulation bringup file.
```

### Terminal 2 — Retrieve the WSL address

```bash
hostname -I | awk '{print $1}'
```

Keep this address available for the PowerShell sender.

### Terminal 3 — Start the joystick receiver in WSL

```bash
cd ~/AMR-Project/Autonomous-Mobile-Robot/ros2_ws

source /opt/ros/jazzy/setup.bash
source install/setup.bash

# Launch the amr_joystick_bridge receiver using the command
# defined by the package or project launch file.
```

The receiver must be running before testing controller commands.

### Windows PowerShell — Run the sender

Open PowerShell in the directory containing the Windows sender script and execute (powershell):

```powershell
python amr_joystick_sender.py
```

Configure or provide the WSL IP address obtained from (bash):

```bash
hostname -I | awk '{print $1}'
```

Use the argument or configuration method implemented by the script. For example, if the sender exposes a host option (powershell):

```powershell
python aamr_joystick_sender.py --host <WSL_IP>
```

Replace `<WSL_IP>` with the address returned by WSL. Do not add an option that the script does not implement; check its help output first:

```powershell
python amr_joystick_sender.py --help
```

---

## 4. PowerShell Script Policy

The Windows-side entry point for controller transmission is:

```text
amr_joystick_sender
```

Do not attempt to launch the ROS 2 Linux receiver directly from PowerShell. PowerShell reads the Windows controller and sends its state to the bridge running in WSL.

The exact invocation depends on how the script is stored:

```powershell
python amr_joystick_sender.py
```

The repository should eventually provide a dedicated Windows README or a wrapper script so the command remains stable.

---

## 5. Verify ROS 2 Output

In WSL, check whether velocity commands are published:

```bash
ros2 topic list | grep cmd_vel
```

Inspect commands:

```bash
ros2 topic echo /cmd_vel
```

Depending on the configured controller stack, the output topic may instead be namespaced or use `geometry_msgs/msg/TwistStamped`.

Check its type:

```bash
ros2 topic type /cmd_vel
```

Check its publication rate:

```bash
ros2 topic hz /cmd_vel
```

---

## 6. Safety

Before enabling joystick motion:

- lift the drive wheels or place the robot in a clear area;
- verify that the emergency-stop mechanism is accessible;
- begin with reduced velocity and acceleration limits;
- confirm the dead-man switch behavior;
- ensure the robot stops when communication is interrupted.

The receiver should implement a timeout that publishes a zero command when packets stop arriving.

---

## 7. Troubleshooting

### No commands are received

1. Retrieve the current WSL IP again:

```bash
hostname -I | awk '{print $1}'
```

2. Confirm that the PowerShell sender targets that address.
3. Confirm that the receiver is running.
4. Confirm that both sender and receiver use the same UDP port.
5. Check Windows Defender Firewall.
6. Restart WSL if the virtual network is in an inconsistent state:

```powershell
wsl --shutdown
```

Then reopen WSL, retrieve the new IP, restart the ROS 2 bridge, and relaunch `amr_joystick_sender`.

### Controller is not detected in Windows

Verify that Windows recognizes the controller:

```powershell
joy.cpl
```

This opens the Windows game-controller panel.

### `/cmd_vel` exists but the robot does not move

Check:

```bash
ros2 topic echo /cmd_vel
ros2 topic info /cmd_vel -v
ros2 node list
ros2 topic echo /odom
```

Also verify that the simulation or motor controller subscribes to the same command topic.
