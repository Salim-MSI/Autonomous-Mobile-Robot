from glob import glob
import os

from setuptools import find_packages, setup


package_name = "amr_perception"


setup(
    name=package_name,
    version="0.0.1",

    packages=find_packages(exclude=["test"]),

    data_files=[
        (
            "share/ament_index/resource_index/packages",
            ["resource/amr_perception"],
        ),
        (
            "share/amr_perception",
            ["package.xml"],
        ),
        (
            os.path.join(
                "share",
                "amr_perception",
                "launch",
            ),
            glob("launch/*.launch.py"),
        ),
        (
            os.path.join(
                "share",
                "amr_perception",
                "config",
            ),
            glob("config/*.yaml"),
        ),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="Salim",
    maintainer_email="your_email@example.com",
    description="Perception package for the Autonomous Mobile Robot.",
    license="Apache-2.0",
    entry_points={
        "console_scripts": [
            "yolo_detector_node = amr_perception.yolo_detector_node:main",
        ],
    },
)