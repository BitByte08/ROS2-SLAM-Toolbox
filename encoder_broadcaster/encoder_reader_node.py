import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32MultiArray
import serial

class EncoderReaderNode(Node):
    def __init__(self):
        super().__init__('encoder_reader')
        self.pub = self.create_publisher(Int32MultiArray, 'encoder_counts', 10)

        # 시리얼 포트 설정
        self.ser = serial.Serial('/dev/ttyUSB1', 115200, timeout=1)

        self.timer = self.create_timer(0.1, self.timer_callback)  # 10Hz

    def timer_callback(self):
        if self.ser.in_waiting:
            line = self.ser.readline().decode('utf-8').strip()
            try:
                counts = list(map(int, line.split(',')))
                msg = Int32MultiArray(data=counts)
                self.pub.publish(msg)
                self.get_logger().info(f"Published encoder counts: {counts}")
            except Exception as e:
                self.get_logger().warn(f"Failed to parse line: {line} ({e})")

def main(args=None):
    rclpy.init(args=args)
    node = EncoderReaderNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

