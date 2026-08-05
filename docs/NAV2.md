# Navigation2 Guide

## Requirements

Before launching Nav2, confirm that:

- a valid map YAML file is available;
- `/scan` is published;
- odometry is published;
- the TF chain connects `map`, `odom`, `base_link`, and sensor frames;
- localization is active;
- the robot footprint and costmaps are configured.

## Diagnostics

```bash
ros2 lifecycle nodes
ros2 topic echo /amcl_pose
ros2 topic echo /map
ros2 topic hz /scan
ros2 run tf2_ros tf2_echo map base_link
```

Send navigation goals only after localization and costmaps are stable.
