from glob import glob
import os

from setuptools import find_packages, setup
from setuptools.command.develop import develop


class ColconDevelopCommand(develop):
    """Keep compatibility with colcon's editable-install cleanup option."""

    user_options = develop.user_options + [
        ("uninstall", None, "Accepted for colcon compatibility"),
        ("editable", None, "Accepted for colcon compatibility"),
        ("build-directory=", None, "Accepted for colcon compatibility"),
        ("script-dir=", None, "Accepted for colcon compatibility"),
    ]
    boolean_options = develop.boolean_options + ["uninstall", "editable"]

    def initialize_options(self):
        super().initialize_options()
        self.uninstall = False
        self.editable = False
        self.build_directory = None
        self.script_dir = None

    def run(self):
        # Recent setuptools removed develop's --uninstall option, while the
        # ROS 2 colcon task still passes both options during editable builds.
        self.editable = True
        super().run()


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
    cmdclass={"develop": ColconDevelopCommand},
)