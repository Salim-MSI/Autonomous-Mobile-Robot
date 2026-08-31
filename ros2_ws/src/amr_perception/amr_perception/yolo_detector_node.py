import rclpy
from rclpy.node import Node
import numpy as np
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

from ultralytics import YOLO


class YoloDetectorNode(Node):
    def __init__(self):
        super().__init__('yolo_node')

        self.declare_parameter('image_topic', '/camera/image_raw')
        self.declare_parameter('model', 'yolov8n.pt')
        self.declare_parameter('confidence', 0.4)

        image_topic = self.get_parameter('image_topic').value
        model_name = self.get_parameter('model').value
        self.confidence = self.get_parameter('confidence').value

        self.get_logger().info(f'Loading YOLO model: {model_name}')

        self.model = YOLO(model_name)
        self.bridge = CvBridge()

        self.subscription = self.create_subscription(
            Image,
            image_topic,
            self.image_callback,
            10
        )

        self.publisher = self.create_publisher(
            Image,
            '/perception/image_annotated',
            10
        )

        self.get_logger().info(
            f'YOLO listening on {image_topic}'
        )

    def image_callback(self, msg):
        try:
            frame = self.bridge.imgmsg_to_cv2(
                msg,
                desired_encoding='bgr8'
            )

            results = self.model(
                frame,
                conf=self.confidence,
                verbose=False
            )

            annotated = results[0].plot()

            annotated = np.ascontiguousarray(
                annotated,
                dtype=np.uint8
            )

            output_msg = Image()
            output_msg.header = msg.header
            output_msg.height = annotated.shape[0]
            output_msg.width = annotated.shape[1]
            output_msg.encoding = 'bgr8'
            output_msg.is_bigendian = False
            output_msg.step = annotated.shape[1] * 3
            output_msg.data = annotated.tobytes()

            self.publisher.publish(output_msg)

        except Exception as e:
            import traceback

            self.get_logger().error(
                f'YOLO callback error: {type(e).__name__}: {repr(e)}'
            )

            traceback.print_exc()


def main(args=None):
    rclpy.init(args=args)

    node = YoloDetectorNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()