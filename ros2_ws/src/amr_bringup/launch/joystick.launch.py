from pathlib import Path

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
import os


def generate_launch_description() -> LaunchDescription:

    joystick_config = os.path.join(get_package_share_directory("amr_bringup"),'config','joystick.yaml')

    use_gamepad = LaunchConfiguration("use_gamepad")
    use_udp_bridge = LaunchConfiguration("use_udp_bridge")
    cmd_vel_topic = LaunchConfiguration("cmd_vel_topic")

    joy_node = Node(
        package="joy_linux",
        executable="joy_linux_node",
        name="joy_linux_node",
        output="screen",
        parameters=[joystick_config],
        condition=IfCondition(use_gamepad),
    )

    teleop_node = Node(
        package="teleop_twist_joy",
        executable="teleop_node",
        name="teleop_twist_joy_node",
        output="screen",
        parameters=[joystick_config],
        remappings=[
            ("/cmd_vel", cmd_vel_topic),
        ],
        condition=IfCondition(use_gamepad),
    )

    udp_joystick_bridge = Node(
        package="amr_joystick_bridge",
        executable="udp_joystick_node",
        name="udp_joystick_bridge",
        output="screen",
        remappings=[
            ("/cmd_vel", cmd_vel_topic),
        ],
        condition=IfCondition(use_udp_bridge),
    )

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "use_gamepad",
                default_value="false",
                description="Start the Linux joystick and teleop nodes",
            ),
            DeclareLaunchArgument(
                "use_udp_bridge",
                default_value="false",
                description="Start the UDP joystick bridge",
            ),
            DeclareLaunchArgument(
                "cmd_vel_topic",
                default_value="/diff_drive_controller/cmd_vel",
                description="Velocity command topic",
            ),
            joy_node,
            teleop_node,
            udp_joystick_bridge,
        ]
    )