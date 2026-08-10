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


def generate_launch_description():

    bringup_share = Path(
        get_package_share_directory("amr_bringup")
    )

    perception_share = Path(
        get_package_share_directory("amr_perception")
    )

    use_sim_time = LaunchConfiguration("use_sim_time")
    use_rviz = LaunchConfiguration("use_rviz")

    perception_params = LaunchConfiguration(
        "perception_params_file"
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

    perception = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            str(
                perception_share
                / "launch"
                / "perception.launch.py"
            )
        ),
        launch_arguments={
            "use_sim_time": use_sim_time,
            "params_file": perception_params,
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
                perception_share
                / "rviz"
                / "perception.rviz"
            ),
        ],
        parameters=[
            {
                "use_sim_time": use_sim_time,
            }
        ],
    )

    default_params = (
        perception_share
        / "config"
        / "perception.yaml"
    )

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "use_sim_time",
                default_value="true",
            ),
            DeclareLaunchArgument(
                "use_rviz",
                default_value="False",
            ),
            DeclareLaunchArgument(
                "perception_params_file",
                default_value=str(default_params),
            ),
            simulation,
            perception,
            rviz,
        ]
    )