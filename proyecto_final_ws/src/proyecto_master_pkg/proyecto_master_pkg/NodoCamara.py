import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

class CameraNode(Node):
    def __init__(self):
        super().__init__('camera_node')
        self.publisher_ = self.create_publisher(Image, 'camara_topic', 10)
        self.timer_ = self.create_timer(0.1, self.timer_callback)
        self.bridge = CvBridge()
        self.camera = cv2.VideoCapture('/dev/video1')  # Número de dispositivo de la cámara
        

    def timer_callback(self):
        ret, frame = self.camera.read()
        if ret:
            img_msg = self.bridge.cv2_to_imgmsg(frame, 'bgr8')
            self.publisher_.publish(img_msg)

def main(args=None):
    rclpy.init(args=args)
    camera_node = CameraNode()
    rclpy.spin(camera_node)
    camera_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
