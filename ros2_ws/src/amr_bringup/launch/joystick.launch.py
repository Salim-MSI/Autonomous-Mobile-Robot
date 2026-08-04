#!/usr/bin/env python3

from pathlib import Path

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    package_share = Path(
        get_package_share_directory("amr_bringup")
    )

    joystick_config = package_share / "config" / "joystick.yaml"

    joy_node = Node(
        package="joy",
        executable="joy_node",
        name="joy_node",
        parameters=[str(joystick_config)],
        output="screen",
    )

    teleop_node = Node(
        package="teleop_twist_joy",
        executable="teleop_node",
        name="teleop_node",
        parameters=[str(joystick_config)],
        remappings=[
            (
                "/cmd_vel",
                "/diff_drive_controller/cmd_vel",
            ),
        ],
        output="screen",
    )

    return LaunchDescription([
        joy_node,
        teleop_node,
    ])