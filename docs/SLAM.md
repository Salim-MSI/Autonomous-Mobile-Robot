# SLAM Guide

## Start Mapping

Source the workspace and launch the project's SLAM launch file.

```bash
cd ~/AMR-Project/Autonomous-Mobile-Robot/ros2_ws
source /opt/ros/jazzy/setup.bash
source install/setup.bash
```

Verify the main data streams:

```bash
ros2 topic hz /scan
ros2 topic echo /odom
ros2 topic echo /map
```

## Save a Map

Create the destination directory:

```bash
mkdir -p ~/AMR-Project/Autonomous-Mobile-Robot/ros2_ws/src/amr_localization/maps
```

Save the current occupancy map:

```bash
ros2 run nav2_map_server map_saver_cli   -f ~/AMR-Project/Autonomous-Mobile-Robot/ros2_ws/src/amr_localization/maps test_world
```

This should generate:

```text
test_world.pgm
test_world.yaml
```

Do not stop SLAM before `map_saver_cli` reports that the map has been saved successfully.
