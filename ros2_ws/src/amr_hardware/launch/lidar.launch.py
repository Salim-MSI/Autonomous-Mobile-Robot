from pathlib import Path

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def generate_launch_description() -> LaunchDescription:
    serial_port = LaunchConfiguration("serial_port")
    frame_id = LaunchConfiguration("frame_id")

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
            "serial_port": serial_port,
            "frame_id": frame_id,
        }.items(),
    )

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "serial_port",
                default_value="/dev/ttyUSB0",
                description="Serial device used by the real LiDAR",
            ),
            DeclareLaunchArgument(
                "frame_id",
                default_value="lidar_link",
                description="TF frame published by the real LiDAR",
            ),
            lidar,
        ]
    )