from pathlib import Path

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def package_launch(package_name: str, launch_name: str):
    package_share = Path(
        get_package_share_directory(package_name)
    )
    return PythonLaunchDescriptionSource(
        str(package_share / "launch" / launch_name)
    )


def generate_launch_description() -> LaunchDescription:
    use_base = LaunchConfiguration("use_base")
    use_camera = LaunchConfiguration("use_camera")
    use_lidar = LaunchConfiguration("use_lidar")
    use_slam = LaunchConfiguration("use_slam")
    use_localization = LaunchConfiguration("use_localization")
    use_navigation = LaunchConfiguration("use_navigation")
    use_perception = LaunchConfiguration("use_perception")
    use_joystick = LaunchConfiguration("use_joystick")
    use_gamepad = LaunchConfiguration("use_gamepad")
    use_udp_bridge = LaunchConfiguration("use_udp_bridge")
    use_rviz = LaunchConfiguration("use_rviz")
    map_file = LaunchConfiguration("map")
    lidar_serial_port = LaunchConfiguration("lidar_serial_port")
    lidar_frame_id = LaunchConfiguration("lidar_frame_id")

    localization_params = (
        Path(get_package_share_directory("amr_localization"))
        / "config"
        / "localization_params.yaml"
    )

    base = IncludeLaunchDescription(
        package_launch("amr_bringup_rasp5", "launch_real_robot.launch.py"),
        condition=IfCondition(use_base),
    )

    camera = IncludeLaunchDescription(
        package_launch("amr_hardware", "camera.launch.py"),
        condition=IfCondition(use_camera),
    )

    lidar = IncludeLaunchDescription(
        package_launch("amr_hardware", "lidar.launch.py"),
        launch_arguments={
            "serial_port": lidar_serial_port,
            "frame_id": lidar_frame_id,
        }.items(),
        condition=IfCondition(use_lidar),
    )

    slam = IncludeLaunchDescription(
        package_launch("amr_slam", "slam.launch.py"),
        launch_arguments={
            "use_sim_time": "false",
            "use_rviz": use_rviz,
        }.items(),
        condition=IfCondition(use_slam),
    )

    localization = IncludeLaunchDescription(
        package_launch("amr_localization", "localization.launch.py"),
        launch_arguments={
            "use_sim_time": "false",
            "map": map_file,
            "params_file": str(localization_params),
            "autostart": "true",
        }.items(),
        condition=IfCondition(use_localization),
    )

    navigation = IncludeLaunchDescription(
        package_launch("amr_navigation", "navigation.launch.py"),
        launch_arguments={
            "use_sim_time": "false",
            "autostart": "true",
        }.items(),
        condition=IfCondition(use_navigation),
    )

    perception = IncludeLaunchDescription(
        package_launch("amr_perception", "perception.launch.py"),
        launch_arguments={
            "image_topic": "/camera/image_raw",
            "debug_image_topic": "/perception/image",
        }.items(),
        condition=IfCondition(use_perception),
    )

    joystick = IncludeLaunchDescription(
        package_launch("amr_bringup_rasp5", "joystick.launch.py"),
        launch_arguments={
            "use_gamepad": use_gamepad,
            "use_udp_bridge": use_udp_bridge,
            "cmd_vel_topic": "/diff_drive_controller/cmd_vel",
        }.items(),
        condition=IfCondition(use_joystick),
    )

    return LaunchDescription(
        [
            DeclareLaunchArgument("use_base", default_value="true"),
            DeclareLaunchArgument("use_camera", default_value="false"),
            DeclareLaunchArgument("use_lidar", default_value="true"),
            DeclareLaunchArgument("use_slam", default_value="false"),
            DeclareLaunchArgument("use_localization", default_value="false"),
            DeclareLaunchArgument("use_navigation", default_value="false"),
            DeclareLaunchArgument("use_perception", default_value="false"),
            DeclareLaunchArgument("use_joystick", default_value="false"),
            DeclareLaunchArgument("use_gamepad", default_value="false"),
            DeclareLaunchArgument("use_udp_bridge", default_value="false"),
            DeclareLaunchArgument("use_rviz", default_value="true"),
            DeclareLaunchArgument(
                "map",
                default_value=str(
                    Path(get_package_share_directory("amr_localization"))
                    / "maps"
                    / "test_world.yaml"
                ),
            ),
            DeclareLaunchArgument(
                "lidar_serial_port",
                default_value="/dev/ttyUSB0",
            ),
            DeclareLaunchArgument(
                "lidar_frame_id",
                default_value="lidar_link",
            ),
            base,
            camera,
            lidar,
            slam,
            localization,
            navigation,
            perception,
            joystick,
        ]
    )
