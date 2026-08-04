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


def generate_launch_description() -> LaunchDescription:
    simulation_share = Path(
        get_package_share_directory("amr_simulation")
    )

    slam_share = Path(
        get_package_share_directory("amr_slam")
    )

    use_sim_time = LaunchConfiguration("use_sim_time")
    launch_slam = LaunchConfiguration("launch_slam")

    simulation_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            str(
                simulation_share
                / "launch"
                / "simulation.launch.py"
            )
        ),
        launch_arguments={
            "use_sim_time": use_sim_time,
        }.items(),
    )

    slam_launch = IncludeLaunchDescription(
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
        condition=IfCondition(launch_slam),
    )

    # Laisse le temps à Gazebo, ros2_control, TF et /scan de démarrer.
    delayed_slam_launch = TimerAction(
        period=5.0,
        actions=[
            slam_launch,
        ],
    )

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "use_sim_time",
                default_value="true",
                description="Use Gazebo simulation clock",
            ),
            DeclareLaunchArgument(
                "launch_slam",
                default_value="true",
                description="Launch SLAM Toolbox",
            ),
            simulation_launch,
            delayed_slam_launch,
        ]
    )