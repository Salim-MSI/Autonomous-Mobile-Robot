from pathlib import Path

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def generate_launch_description() -> LaunchDescription:
    bringup_share = Path(
        get_package_share_directory("amr_bringup")
    )

    description_share = Path(
        get_package_share_directory("amr_description")
    )

    rplidar_share = Path(
        get_package_share_directory("rplidar_ros")
    )

    use_lidar = LaunchConfiguration("use_lidar")

    description = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            str(
                description_share
                / "launch"
                / "display.launch.py"
            )
        ),
        launch_arguments={
            "use_rviz": "false",
            "use_gui": "false",
        }.items(),
    )

    lidar = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            str(
                rplidar_share
                / "launch"
                / "rplidar_a1_launch.py"
            )
        ),
        launch_arguments={
            "serial_port": "/dev/ttyUSB0",
            "frame_id": "lidar_link",
        }.items(),
    )

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "use_lidar",
                default_value="true",
            ),
            description,
            lidar,
        ]
    )