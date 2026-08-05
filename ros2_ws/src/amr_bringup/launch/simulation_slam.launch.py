from pathlib import Path

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    IncludeLaunchDescription,
)
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    bringup_share = Path(
        get_package_share_directory("amr_bringup")
    )

    slam_share = Path(
        get_package_share_directory("amr_slam")
    )

    use_sim_time = LaunchConfiguration("use_sim_time")
    use_rviz = LaunchConfiguration("use_rviz")
    use_joystick = LaunchConfiguration("use_joystick")
    use_gamepad = LaunchConfiguration("use_gamepad")
    use_udp_bridge = LaunchConfiguration("use_udp_bridge")

    simulation = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            str(
                bringup_share
                / "launch"
                / "simulation.launch.py"
            )
        ),
        launch_arguments={
            "use_sim_time": use_sim_time,
            "use_joystick": use_joystick,
            "use_gamepad": use_gamepad,
            "use_udp_bridge": use_udp_bridge,
        }.items(),
    )

    slam = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            str(
                slam_share
                / "launch"
                / "slam.launch.py"
            )
        ),
        launch_arguments={
            "use_sim_time": use_sim_time,
        }.items(),
    )

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "use_sim_time",
                default_value="true",
            ),
            DeclareLaunchArgument(
                "use_rviz",
                default_value="true",
            ),
            DeclareLaunchArgument(
                "use_joystick",
                default_value="true",
            ),
            DeclareLaunchArgument(
                "use_gamepad",
                default_value="false",
            ),
            DeclareLaunchArgument(
                "use_udp_bridge",
                default_value="false",
            ),
            simulation,
            slam,
        ]
    )