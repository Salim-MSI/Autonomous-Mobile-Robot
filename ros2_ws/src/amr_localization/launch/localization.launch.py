from pathlib import Path

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description() -> LaunchDescription:
    localization_share = Path(
        get_package_share_directory("amr_localization")
    )

    default_map = (
        localization_share
        / "maps"
        / "test_world.yaml"
    )

    default_params_file = (
        localization_share
        / "config"
        / "localization_params.yaml"
    )

    use_sim_time = LaunchConfiguration("use_sim_time")
    autostart = LaunchConfiguration("autostart")
    map_file = LaunchConfiguration("map")
    params_file = LaunchConfiguration("params_file")

    map_server = Node(
        package="nav2_map_server",
        executable="map_server",
        name="map_server",
        output="screen",
        parameters=[
            params_file,
            {
                # Injection explicite du chemin de carte
                "yaml_filename": map_file,
                "use_sim_time": ParameterValue(
                    use_sim_time,
                    value_type=bool,
                ),
            },
        ],
    )

    amcl = Node(
        package="nav2_amcl",
        executable="amcl",
        name="amcl",
        output="screen",
        parameters=[
            params_file,
            {
                "use_sim_time": ParameterValue(
                    use_sim_time,
                    value_type=bool,
                ),
            },
        ],
    )

    lifecycle_manager = Node(
        package="nav2_lifecycle_manager",
        executable="lifecycle_manager",
        name="lifecycle_manager_localization",
        output="screen",
        parameters=[
            {
                "use_sim_time": ParameterValue(
                    use_sim_time,
                    value_type=bool,
                ),
                "autostart": ParameterValue(
                    autostart,
                    value_type=bool,
                ),
                "node_names": [
                    "map_server",
                    "amcl",
                ],
            },
        ],
    )

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "use_sim_time",
                default_value="true",
                description="Use simulation clock",
            ),
            DeclareLaunchArgument(
                "autostart",
                default_value="true",
                description="Automatically activate localization nodes",
            ),
            DeclareLaunchArgument(
                "map",
                default_value=str(default_map),
                description="Absolute path to the map YAML file",
            ),
            DeclareLaunchArgument(
                "params_file",
                default_value=str(default_params_file),
                description="Localization parameters file",
            ),
            map_server,
            amcl,
            lifecycle_manager,
        ]
    )