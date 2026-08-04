from pathlib import Path

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:

    rviz_config = Path(
        get_package_share_directory("amr_slam")
    ) / "rviz" / "slam.rviz"

    amr_slam_share = Path(
        get_package_share_directory("amr_slam")
    )

    slam_toolbox_share = Path(
        get_package_share_directory("slam_toolbox")
    )

    params_file = (
        amr_slam_share
        / "config"
        / "mapper_params_online_async.yaml"
    )

    slam_toolbox_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            str(
                slam_toolbox_share
                / "launch"
                / "online_async_launch.py"
            )
        ),
        launch_arguments={
            "slam_params_file": str(params_file),
            "use_sim_time": "true",
        }.items(),
    )

    rviz = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="screen",
        arguments=["-d", str(rviz_config)],
    )

    return LaunchDescription([
        slam_toolbox_launch,
        rviz,
    ])