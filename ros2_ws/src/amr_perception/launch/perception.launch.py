from pathlib import Path

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
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
    image_topic = LaunchConfiguration("image_topic")
    debug_image_topic = LaunchConfiguration("debug_image_topic")

    yolo_detector = Node(
        package="amr_perception",
        executable="yolo_detector_node",
        name="yolo_detector",
        output="screen",
        parameters=[
            str(params_file),
            {
                "image_topic": image_topic,
                "debug_image_topic": debug_image_topic,
            },
        ],
    )

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "image_topic",
                default_value="/camera/image",
                description="Camera image topic consumed by perception",
            ),
            DeclareLaunchArgument(
                "debug_image_topic",
                default_value="/perception/image",
                description="Annotated image topic published by perception",
            ),
            yolo_detector,
        ]
    )