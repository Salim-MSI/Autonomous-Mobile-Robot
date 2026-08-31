from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    camera_node = Node(
        package="camera_ros",
        executable="camera_node",
        name="camera",
        namespace="camera",
        output="screen",
        parameters=[
            {
                "width": 640,
                "height": 480,
                "FrameDurationLimits": [33333, 33333],
            }
        ],
    )

    return LaunchDescription([
        camera_node,
    ])