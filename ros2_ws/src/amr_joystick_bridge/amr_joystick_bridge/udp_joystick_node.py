#!/usr/bin/env python3

import json
import socket
import time
from typing import Optional

import rclpy
from geometry_msgs.msg import TwistStamped
from rclpy.node import Node


class UdpJoystickNode(Node):
    def __init__(self) -> None:
        super().__init__("udp_joystick_node")

        self.declare_parameter("port", 5005)
        self.declare_parameter(
            "cmd_vel_topic",
            "/diff_drive_controller/cmd_vel",
        )
        self.declare_parameter("command_timeout", 0.5)
        self.declare_parameter("max_linear_speed", 0.6)
        self.declare_parameter("max_angular_speed", 1.5)

        port = int(self.get_parameter("port").value)
        topic = str(self.get_parameter("cmd_vel_topic").value)

        self.command_timeout = float(
            self.get_parameter("command_timeout").value
        )
        self.max_linear_speed = float(
            self.get_parameter("max_linear_speed").value
        )
        self.max_angular_speed = float(
            self.get_parameter("max_angular_speed").value
        )

        self.publisher = self.create_publisher(
            TwistStamped,
            topic,
            10,
        )

        self.socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_DGRAM,
        )

        self.socket.setsockopt(
            socket.SOL_SOCKET,
            socket.SO_REUSEADDR,
            1,
        )

        self.socket.bind(("0.0.0.0", port))
        self.socket.setblocking(False)

        self.last_message_time: Optional[float] = None
        self.last_command_was_zero = True

        self.timer = self.create_timer(0.02, self.update)

        self.get_logger().info(
            f"Pont manette UDP actif sur le port {port}"
        )
        self.get_logger().info(
            f"Publication vers {topic}"
        )

    @staticmethod
    def clamp(value: float, minimum: float, maximum: float) -> float:
        return max(minimum, min(maximum, value))

    def publish_command(
        self,
        linear_x: float,
        angular_z: float,
    ) -> None:
        message = TwistStamped()
        message.header.stamp = self.get_clock().now().to_msg()
        message.header.frame_id = "base_link"

        message.twist.linear.x = linear_x
        message.twist.angular.z = angular_z

        self.publisher.publish(message)

        self.last_command_was_zero = (
            abs(linear_x) < 1e-6
            and abs(angular_z) < 1e-6
        )

    def update(self) -> None:
        now = time.monotonic()
        received_packet = False

        while True:
            try:
                payload, _address = self.socket.recvfrom(4096)
            except BlockingIOError:
                break
            except OSError as error:
                self.get_logger().error(f"Erreur UDP : {error}")
                break

            received_packet = True

            try:
                data = json.loads(payload.decode("utf-8"))

                enabled = bool(data.get("enabled", False))

                if enabled:
                    linear_x = float(data.get("linear_x", 0.0))
                    angular_z = float(data.get("angular_z", 0.0))
                else:
                    linear_x = 0.0
                    angular_z = 0.0

                linear_x = self.clamp(
                    linear_x,
                    -self.max_linear_speed,
                    self.max_linear_speed,
                )

                angular_z = self.clamp(
                    angular_z,
                    -self.max_angular_speed,
                    self.max_angular_speed,
                )

                self.publish_command(linear_x, angular_z)
                self.last_message_time = now

            except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as error:
                self.get_logger().warning(
                    f"Commande UDP invalide : {error}"
                )

        # Arrêt automatique si Windows cesse d’envoyer.
        if (
            not received_packet
            and self.last_message_time is not None
            and now - self.last_message_time > self.command_timeout
            and not self.last_command_was_zero
        ):
            self.publish_command(0.0, 0.0)
            self.get_logger().warning(
                "Connexion manette perdue : arrêt du robot."
            )

    def destroy_node(self) -> bool:
        self.publish_command(0.0, 0.0)
        self.socket.close()
        return super().destroy_node()


def main(args=None) -> None:
    rclpy.init(args=args)

    node = UdpJoystickNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
