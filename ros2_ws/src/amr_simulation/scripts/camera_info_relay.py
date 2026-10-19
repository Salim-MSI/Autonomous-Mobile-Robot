#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import CameraInfo


class CameraInfoRelay(Node):
    def __init__(self) -> None:
        super().__init__("camera_info_relay")
        self.publisher = self.create_publisher(
            CameraInfo,
            "/perception/camera_info",
            10,
        )
        self.subscription = self.create_subscription(
            CameraInfo,
            "/camera/camera_info",
            self._relay,
            10,
        )

    def _relay(self, message: CameraInfo) -> None:
        self.publisher.publish(message)


def main(args=None) -> None:
    rclpy.init(args=args)
    node = CameraInfoRelay()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
