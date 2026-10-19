from pathlib import Path

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def generate_launch_description() -> LaunchDescription:
    rplidar_share = Path(
        get_package_share_directory("rplidar_ros")
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
            lidar,
        ]
    )