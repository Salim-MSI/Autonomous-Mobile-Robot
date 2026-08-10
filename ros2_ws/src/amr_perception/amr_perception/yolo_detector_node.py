#!/usr/bin/env python3

import time

import cv2
import rclpy

from cv_bridge import CvBridge
from rclpy.node import Node
from sensor_msgs.msg import Image
from ultralytics import YOLO
import traceback


class YoloDetectorNode(Node):

    def __init__(self) -> None:
        super().__init__("yolo_detector")

        self.declare_parameter("model", "yolov8n.pt")
        self.declare_parameter("image_topic", "/camera/image")
        self.declare_parameter(
            "debug_image_topic",
            "/perception/debug_image",
        )
        self.declare_parameter("confidence", 0.50)
        self.declare_parameter("inference_rate", 5.0)
        self.declare_parameter("device", "cpu")

        model_name = str(
            self.get_parameter("model").value
        )

        image_topic = str(
            self.get_parameter("image_topic").value
        )

        debug_topic = str(
            self.get_parameter("debug_image_topic").value
        )

        self.confidence = float(
            self.get_parameter("confidence").value
        )

        self.inference_rate = float(
            self.get_parameter("inference_rate").value
        )

        self.device = str(
            self.get_parameter("device").value
        )

        self.bridge = CvBridge()

        self.model = YOLO(model_name)

        self.subscription = self.create_subscription(
            Image,
            image_topic,
            self.image_callback,
            10,
        )

        self.debug_publisher = self.create_publisher(
            Image,
            debug_topic,
            10,
        )

        self.last_inference_time = 0.0

        self.get_logger().info(
            f"YOLO detector started with model: {model_name}"
        )

        self.get_logger().info(
            f"Input image topic: {image_topic}"
        )

        self.get_logger().info(
            f"Inference rate: {self.inference_rate:.1f} Hz"
        )

    def image_callback(self, message: Image) -> None:
        now = time.monotonic()

        min_period = 1.0 / self.inference_rate

        if now - self.last_inference_time < min_period:
            return

        self.last_inference_time = now

        try:
            image = self.bridge.imgmsg_to_cv2(
                message,
                desired_encoding="bgr8",
            )

            results = self.model.predict(
                source=image,
                conf=self.confidence,
                device=self.device,
                verbose=False,
            )

            boxes = results[0].boxes

            self.get_logger().info(
                f"Detections: {len(boxes)}"
            )

            for box in boxes:
                class_id = int(box.cls[0])
                confidence = float(box.conf[0])
                class_name = self.model.names[class_id]

                self.get_logger().info(
                    f"{class_name}: {confidence:.2f}"
                )

            annotated_image = results[0].plot()
            annotated_image = annotated_image.astype(
                "uint8",
                copy=False,
            )
            annotated_image = annotated_image.copy(order="C")

            output = Image()
            output.header = message.header
            output.height = annotated_image.shape[0]
            output.width = annotated_image.shape[1]
            output.encoding = "bgr8"
            output.is_bigendian = False
            output.step = annotated_image.shape[1] * 3
            output.data = annotated_image.tobytes()

            self.debug_publisher.publish(output)

        except Exception as error:
            self.get_logger().error(
                f"YOLO inference failed: "
                f"{type(error).__name__}: {error}"
            )

def main(args=None) -> None:
    rclpy.init(args=args)

    node = YoloDetectorNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()