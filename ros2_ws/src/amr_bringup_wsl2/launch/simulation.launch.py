from pathlib import Path

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    IncludeLaunchDescription,
    TimerAction,
)
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def include_launch(package_name: str, launch_name: str):
    package_share = Path(
        get_package_share_directory(package_name)
    )
    return PythonLaunchDescriptionSource(
        str(package_share / "launch" / launch_name)
    )


def generate_launch_description() -> LaunchDescription:
    simulation_share = Path(
        get_package_share_directory("amr_simulation")
    )
    bringup_share = Path(
        get_package_share_directory("amr_bringup_rasp5")
    )

    world = LaunchConfiguration("world")
    use_sim_time = LaunchConfiguration("use_sim_time")
    use_rviz = LaunchConfiguration("use_rviz")
    use_localization = LaunchConfiguration("use_localization")
    use_navigation = LaunchConfiguration("use_navigation")
    use_slam = LaunchConfiguration("use_slam")
    use_perception = LaunchConfiguration("use_perception")
    use_joystick = LaunchConfiguration("use_joystick")
    use_gamepad = LaunchConfiguration("use_gamepad")
    use_udp_bridge = LaunchConfiguration("use_udp_bridge")
    map_file = LaunchConfiguration("map")
    autostart = LaunchConfiguration("autostart")
    startup_delay = LaunchConfiguration("startup_delay")

    default_world = simulation_share / "worlds" / "empty.world.sdf"

    simulation = IncludeLaunchDescription(
        include_launch("amr_simulation", "simulation.launch.py"),
        launch_arguments={
            "world": world,
            "use_sim_time": use_sim_time,
            "use_rviz": use_rviz,
        }.items(),
    )

    localization = IncludeLaunchDescription(
        include_launch(
            "amr_localization",
            "localization.launch.py",
        ),
        launch_arguments={
            "use_sim_time": use_sim_time,
            "map": map_file,
            "params_file": str(
                Path(
                    get_package_share_directory("amr_localization")
                )
                / "config"
                / "localization_params.yaml"
            ),
            "autostart": autostart,
        }.items(),
        condition=IfCondition(use_localization),
    )

    navigation = IncludeLaunchDescription(
        include_launch(
            "amr_navigation",
            "navigation.launch.py",
        ),
        launch_arguments={
            "use_sim_time": use_sim_time,
            "autostart": autostart,
        }.items(),
        condition=IfCondition(use_navigation),
    )

    slam = IncludeLaunchDescription(
        include_launch(
            "amr_slam",
            "slam.launch.py",
        ),
        launch_arguments={
            "use_sim_time": use_sim_time,
            "use_rviz": "false",
        }.items(),
        condition=IfCondition(use_slam),
    )

    perception = IncludeLaunchDescription(
        include_launch(
            "amr_perception",
            "perception.launch.py",
        ),
        launch_arguments={
            "use_sim_time": use_sim_time,
        }.items(),
        condition=IfCondition(use_perception),
    )

    joystick = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            str(bringup_share / "launch" / "joystick.launch.py")
        ),
        launch_arguments={
            "use_gamepad": use_gamepad,
            "use_udp_bridge": use_udp_bridge,
            "cmd_vel_topic": "/diff_drive_controller/cmd_vel",
        }.items(),
        condition=IfCondition(use_joystick),
    )

    delayed_localization = TimerAction(
        period=startup_delay,
        actions=[localization],
    )
    delayed_navigation = TimerAction(
        period=startup_delay,
        actions=[navigation],
    )
    delayed_slam = TimerAction(
        period=startup_delay,
        actions=[slam],
    )

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "world",
                default_value=str(default_world),
                description="Gazebo world file",
            ),
            DeclareLaunchArgument(
                "use_sim_time",
                default_value="true",
            ),
            DeclareLaunchArgument(
                "use_rviz",
                default_value="true",
            ),
            DeclareLaunchArgument(
                "use_localization",
                default_value="false",
                description="Launch AMCL localization",
            ),
            DeclareLaunchArgument(
                "use_navigation",
                default_value="false",
                description="Launch Nav2 navigation",
            ),
            DeclareLaunchArgument(
                "use_slam",
                default_value="false",
                description="Launch SLAM Toolbox",
            ),
            DeclareLaunchArgument(
                "use_perception",
                default_value="false",
                description="Launch perception",
            ),
            DeclareLaunchArgument(
                "use_joystick",
                default_value="false",
                description="Launch joystick input",
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
                default_value=str(
                    Path(
                        get_package_share_directory("amr_localization")
                    )
                    / "maps"
                    / "test_world.yaml"
                ),
                description="Map YAML file",
            ),
            DeclareLaunchArgument(
                "autostart",
                default_value="true",
            ),
            DeclareLaunchArgument(
                "startup_delay",
                default_value="20.0",
                description=(
                    "Seconds to wait for Gazebo, TF and controllers "
                    "before localization/navigation"
                ),
            ),
            simulation,
            delayed_localization,
            delayed_navigation,
            delayed_slam,
            perception,
            joystick,
        ]
    )
