# Simulation Guide

## Preparation

```bash
cd ~/AMR-Project/Autonomous-Mobile-Robot/ros2_ws
source /opt/ros/jazzy/setup.bash
source install/setup.bash
```

Launch the simulation using the launch file provided by `amr_simulation` or `amr_bringup`.

## Validation

Verify the active nodes and topics:

```bash
ros2 node list
ros2 topic list
ros2 topic hz /scan
ros2 topic echo /odom
```

Verify the TF tree:

```bash
ros2 run tf2_tools view_frames
```

Check that the robot model, LiDAR, odometry, transforms, and velocity command interface are operational before starting SLAM or Nav2.
