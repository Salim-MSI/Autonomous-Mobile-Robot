from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    camera_node = Node(
        package="camera_ros",
        executable="camera_node",

        name="camera",
        output="screen",

        parameters=[
            {
                "width": 640,
                "height": 480,
            }
        ],

        remappings=[
            ("~/image_raw", "/camera/image_raw"),
            ("~/camera_info", "/camera/camera_info"),
        ],
    )

    return LaunchDescription([
        camera_node
    ])