from setuptools import find_packages, setup


package_name = "amr_joystick_bridge"

setup(
    name=package_name,
    version="0.0.1",
    packages=find_packages(
        exclude=["test"],
    ),
    data_files=[
        (
            "share/ament_index/resource_index/packages",
            ["resource/" + package_name],
        ),
        (
            "share/" + package_name,
            ["package.xml"],
        ),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="salim",
    maintainer_email="salim@example.com",
    description="Windows-to-ROS 2 UDP joystick bridge",
    license="Apache-2.0",
    entry_points={
        "console_scripts": [
            "udp_joystick_node = "
            "amr_joystick_bridge.udp_joystick_node:main",
        ],
    },
)