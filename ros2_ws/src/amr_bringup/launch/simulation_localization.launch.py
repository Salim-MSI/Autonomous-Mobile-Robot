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

    localization_share = Path(
        get_package_share_directory("amr_localization")
    )

    use_sim_time = LaunchConfiguration("use_sim_time")
    use_rviz = LaunchConfiguration("use_rviz")
    use_joystick = LaunchConfiguration("use_joystick")
    use_gamepad = LaunchConfiguration("use_gamepad")
    use_udp_bridge = LaunchConfiguration("use_udp_bridge")
    map_file = LaunchConfiguration("map")
    params_file = LaunchConfiguration("params_file")
    autostart = LaunchConfiguration("autostart")

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

    localization = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            str(
                localization_share
                / "launch"
                / "localization.launch.py"
            )
        ),
        launch_arguments={
            "use_sim_time": use_sim_time,
            "map": map_file,
            "params_file": params_file,
            "autostart": autostart,
        }.items(),
    )

    rviz = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="screen",
        arguments=[
            "-d",
            str(
                localization_share
                / "rviz"
                / "localization.rviz"
            ),
        ],
        parameters=[
            {"use_sim_time": use_sim_time},
        ],
        condition=IfCondition(use_rviz),
    )

    default_map = (
        localization_share
        / "maps"
        / "test_world.yaml"
    )

    default_params_file = (
        localization_share
        / "config"
        / "localization_params.yaml"
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
            DeclareLaunchArgument(
                "map",
                default_value=str(default_map),
                description="Map YAML file",
            ),
            DeclareLaunchArgument(
                "params_file",
                default_value=str(default_params_file),
            ),
            DeclareLaunchArgument(
                "autostart",
                default_value="true",
            ),
            simulation,
            localization,
            rviz,
        ]
    )