from pathlib import Path

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    IncludeLaunchDescription,
    RegisterEventHandler,
    TimerAction,
)
from launch.conditions import IfCondition
from launch.event_handlers import OnProcessExit
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, LaunchConfiguration

from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description() -> LaunchDescription:
    description_share = Path(
        get_package_share_directory("amr_description")
    )

    simulation_share = Path(
        get_package_share_directory("amr_simulation")
    )

    control_share = Path(
        get_package_share_directory("amr_control")
    )

    ros_gz_share = Path(
        get_package_share_directory("ros_gz_sim")
    )

    use_sim_time = LaunchConfiguration("use_sim_time")
    use_rviz = LaunchConfiguration("use_rviz")
    world = LaunchConfiguration("world")

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

    rviz_config_file = (
        simulation_share
        / "rviz"
        / "simulation.rviz"
    )

    controller_params_file = (
        control_share
        / "config"
        / "controllers_sim.yaml"
    )

    robot_description = ParameterValue(
        Command(
            [
                "xacro ",
                str(xacro_file),
                " use_ros2_control:=true",
                " sim_mode:=true",
                " controller_params_file:=",
                str(controller_params_file),
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
            "gz_args": ["-r ", world]
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
                "use_sim_time": use_sim_time,
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

    sensor_bridge = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        name="ros_gz_bridge",
        output="screen",
        arguments=[
            "/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock",
            "/camera/image@sensor_msgs/msg/Image[gz.msgs.Image",
            "/camera/camera_info@sensor_msgs/msg/CameraInfo[gz.msgs.CameraInfo",
        ],
    )

    perception_camera_info_relay = Node(
        package="amr_simulation",
        executable="camera_info_relay",
        name="perception_camera_info_bridge",
        output="screen",
    )

    lidar_bridge = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        name="lidar_bridge",
        output="screen",
        arguments=[
            "/scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan",
        ],
        parameters=[
            {
                "override_frame_id": "lidar_link",
            }
        ],
    )

    joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        name="joint_state_broadcaster_spawner",
        arguments=[
            "joint_state_broadcaster",
            "--controller-manager",
            "/controller_manager",
            "--controller-manager-timeout",
            "60.0",
            "--service-call-timeout",
            "60.0",
        ],
        output="screen",
    )

    diff_drive_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        name="diff_drive_controller_spawner",
        arguments=[
            "diff_drive_controller",
            "--controller-manager",
            "/controller_manager",
            "--controller-manager-timeout",
            "60.0",
            "--service-call-timeout",
            "60.0",
        ],
        output="screen",
    )

    start_joint_state_broadcaster = RegisterEventHandler(
        OnProcessExit(
            target_action=spawn_robot,
            on_exit=[
                TimerAction(
                    period=5.0,
                    actions=[joint_state_broadcaster_spawner],
                ),
            ],
        )
    )

    start_diff_drive_controller = RegisterEventHandler(
        OnProcessExit(
            target_action=joint_state_broadcaster_spawner,
            on_exit=[
                TimerAction(
                    period=3.0,
                    actions=[diff_drive_controller_spawner],
                ),
            ],
        )
    )

    rviz = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="screen",
        arguments=[
            "-d",
            str(rviz_config_file),
        ],
        parameters=[
            {
                "use_sim_time": use_sim_time,
            }
        ],
        condition=IfCondition(use_rviz),
    )

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "use_sim_time",
                default_value="true",
            ),
            DeclareLaunchArgument(
                "world",
                default_value=str(world_file),
                description="Gazebo world file",
            ),

            DeclareLaunchArgument(
                "use_rviz",
                default_value="true",
            ),

            gazebo,
            robot_state_publisher,
            spawn_robot,

            sensor_bridge,
            perception_camera_info_relay,
            lidar_bridge,

            start_joint_state_broadcaster,
            start_diff_drive_controller,

            rviz,
        ]
    )