from pathlib import Path

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description() -> LaunchDescription:
    description_share = Path(
        get_package_share_directory("amr_description")
    )

    simulation_share = Path(
        get_package_share_directory("amr_simulation")
    )

    ros_gz_share = Path(
        get_package_share_directory("ros_gz_sim")
    )

    xacro_file = (
        description_share
        / "urdf"
        / "robot.urdf.xacro"
    )

    world_file = (
        simulation_share
        / "worlds"
        / "empty.world.sdf"
    )

    robot_description = ParameterValue(
        Command(
            [
                "xacro ",
                str(xacro_file),
            ]
        ),
        value_type=str,
    )

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            str(
                ros_gz_share
                / "launch"
                / "gz_sim.launch.py"
            )
        ),
        launch_arguments={
            "gz_args": f"-r {world_file}"
        }.items(),
    )

    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher",
        output="screen",
        parameters=[
            {
                "robot_description": robot_description,
                "use_sim_time": True,
            }
        ],
    )

    spawn_robot = Node(
        package="ros_gz_sim",
        executable="create",
        name="spawn_amr",
        output="screen",
        arguments=[
            "-topic",
            "robot_description",
            "-name",
            "amr",
            "-x",
            "0.0",
            "-y",
            "0.0",
            "-z",
            "0.10",
        ],
    )

    bridge = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        name="ros_gz_bridge",
        output="screen",
        arguments=[
            "/cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist",
            "/odom@nav_msgs/msg/Odometry@gz.msgs.Odometry",
            "/joint_states@sensor_msgs/msg/JointState@gz.msgs.Model",
            "/tf@tf2_msgs/msg/TFMessage@gz.msgs.Pose_V",
            "/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock",
        ],
    )

    return LaunchDescription(
        [
            gazebo,
            robot_state_publisher,
            spawn_robot,
            bridge,
        ]
    )