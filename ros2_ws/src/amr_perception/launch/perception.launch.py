from pathlib import Path

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:

    perception_share = Path(
        get_package_share_directory("amr_perception")
    )

    params_file = (
        perception_share
        / "config"
        / "perception.yaml"
    )

    yolo_detector = Node(
        package="amr_perception",
        executable="yolo_detector_node",
        name="yolo_detector",
        output="screen",
        parameters=[str(params_file)],
    )

    return LaunchDescription(
        [
            yolo_detector,
        ]
    )