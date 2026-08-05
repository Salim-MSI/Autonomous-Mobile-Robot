from pathlib import Path

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    IncludeLaunchDescription,
)
from launch.conditions import IfCondition
from launch.launch_description_sources import (
    PythonLaunchDescriptionSource,
)
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch.actions import TimerAction


def generate_launch_description() -> LaunchDescription:
    bringup_share = Path(
        get_package_share_directory("amr_bringup")
    )

    localization_share = Path(
        get_package_share_directory("amr_localization")
    )

    navigation_share = Path(
        get_package_share_directory("amr_navigation")
    )

    use_sim_time = LaunchConfiguration("use_sim_time")
    use_rviz = LaunchConfiguration("use_rviz")
    map_file = LaunchConfiguration("map")
    autostart = LaunchConfiguration("autostart")

    localization_params_file = LaunchConfiguration(
        "localization_params_file"
    )

    navigation_params_file = LaunchConfiguration(
        "navigation_params_file"
    )

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
            "use_joystick": "false",
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
            "params_file": localization_params_file,
            "autostart": autostart,
        }.items(),
    )

    navigation = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            str(
                navigation_share
                / "launch"
                / "navigation.launch.py"
            )
        ),
        launch_arguments={
            "use_sim_time": use_sim_time,
            "params_file": navigation_params_file,
        }.items(),
    )

    delayed_navigation = TimerAction(
        period=5.0,
        actions=[navigation],
    )

    rviz = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="screen",
        arguments=[
            "-d",
            str(
                navigation_share
                / "rviz"
                / "navigation.rviz"
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

    default_localization_params = (
        localization_share
        / "config"
        / "localization_params.yaml"
    )

    default_navigation_params = (
        navigation_share
        / "config"
        / "nav2_params.yaml"
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
                "map",
                default_value=str(default_map),
            ),
            DeclareLaunchArgument(
                "localization_params_file",
                default_value=str(
                    default_localization_params
                ),
            ),
            DeclareLaunchArgument(
                "navigation_params_file",
                default_value=str(
                    default_navigation_params
                ),
            ),
            DeclareLaunchArgument(
                "autostart",
                default_value="true",
            ),
            simulation,
            localization,
            delayed_navigation,
            rviz,
        ]
    )