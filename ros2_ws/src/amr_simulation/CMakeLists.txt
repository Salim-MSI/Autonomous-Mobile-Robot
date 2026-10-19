cmake_minimum_required(VERSION 3.8)
project(amr_simulation)

find_package(ament_cmake REQUIRED)

install(
  PROGRAMS
    scripts/camera_info_relay.py
  DESTINATION lib/${PROJECT_NAME}
  RENAME camera_info_relay
)

install(
  DIRECTORY
    rviz
    launch
    worlds
    urdf
  DESTINATION share/${PROJECT_NAME}
)

ament_package()