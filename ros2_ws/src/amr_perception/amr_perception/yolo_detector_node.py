import rclpy
from rclpy.node import Node

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

            output_msg = self.bridge.cv2_to_imgmsg(
                annotated,
                encoding='bgr8'
            )

            output_msg.header = msg.header

            self.publisher.publish(output_msg)

        except Exception as e:
            self.get_logger().error(str(e))


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