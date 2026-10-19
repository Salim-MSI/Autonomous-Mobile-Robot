from pathlib import Path

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    use_sim_time = LaunchConfiguration("use_sim_time")
    use_rviz = LaunchConfiguration("use_rviz")

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
            "use_sim_time": use_sim_time,
        }.items(),
    )

    rviz = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="screen",
        arguments=["-d", str(rviz_config)],
        condition=IfCondition(use_rviz),
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            "use_sim_time",
            default_value="true",
        ),
        DeclareLaunchArgument(
            "use_rviz",
            default_value="true",
        ),
        slam_toolbox_launch,
        rviz,
    ])