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


def generate_launch_description() -> LaunchDescription:
    simulation_share = Path(
        get_package_share_directory("amr_simulation")
    )

    bringup_share = Path(
        get_package_share_directory("amr_bringup")
    )

    world = LaunchConfiguration("world")
    use_sim_time = LaunchConfiguration("use_sim_time")
    use_joystick = LaunchConfiguration("use_joystick")
    use_gamepad = LaunchConfiguration("use_gamepad")
    use_udp_bridge = LaunchConfiguration("use_udp_bridge")

    simulation = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            str(
                simulation_share
                / "launch"
                / "simulation.launch.py"
            )
        ),
        launch_arguments={
            "world": world,
            "use_sim_time": use_sim_time,
        }.items(),
    )

    joystick = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            str(
                bringup_share
                / "launch"
                / "joystick.launch.py"
            )
        ),
        launch_arguments={
            "use_gamepad": use_gamepad,
            "use_udp_bridge": use_udp_bridge,
            "cmd_vel_topic": "/diff_drive_controller/cmd_vel",
        }.items(),
        condition=IfCondition(use_joystick),
    )

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "world",
                default_value="empty.world.sdf",
                description="Gazebo world filename or path",
            ),
            DeclareLaunchArgument(
                "use_sim_time",
                default_value="true",
            ),
            DeclareLaunchArgument(
                "use_joystick",
                default_value="false",
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
            joystick,
        ]
    )