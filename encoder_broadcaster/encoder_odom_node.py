import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from std_msgs.msg import Int32MultiArray
from geometry_msgs.msg import Quaternion, TransformStamped
from tf2_ros import TransformBroadcaster
from tf_transformations import quaternion_from_euler
import math

class EncoderOdomNode(Node):
    def __init__(self):
        super().__init__('encoder_odom_node')

        # 로봇 파라미터
        self.wheel_radius = 0.03         # [m]
        self.pulses_per_rev = 500        # 엔코더 CPR
        self.wheel_base = 0.15           # 바퀴 간 거리 [m]

        # 상태 변수
        self.prev_left = None
        self.prev_right = None
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0

        # 퍼블리셔
        self.odom_pub = self.create_publisher(Odometry, 'odom', 10)
        self.tf_broadcaster = TransformBroadcaster(self)

        # 서브스크라이버
        self.create_subscription(Int32MultiArray, 'encoder_counts', self.encoder_callback, 10)

    def encoder_callback(self, msg):
        left = msg.data[0]
        right = msg.data[1]

        if self.prev_left is None:
            self.prev_left = left
            self.prev_right = right
            return

        # 변화량 계산
        delta_left = left - self.prev_left
        delta_right = right - self.prev_right
        self.prev_left = left
        self.prev_right = right

        # 이동 거리 계산
        d_left = 2 * math.pi * self.wheel_radius * delta_left / self.pulses_per_rev
        d_right = 2 * math.pi * self.wheel_radius * delta_right / self.pulses_per_rev
        d_center = (d_left + d_right) / 2
        delta_theta = (d_right - d_left) / self.wheel_base

        # 위치 업데이트
        self.theta += delta_theta
        self.x += d_center * math.cos(self.theta)
        self.y += d_center * math.sin(self.theta)

        # 시간
        now = self.get_clock().now().to_msg()

        # Odometry 메시지 작성
        odom = Odometry()
        odom.header.stamp = now
        odom.header.frame_id = 'odom'
        odom.child_frame_id = 'base_link'
        odom.pose.pose.position.x = self.x
        odom.pose.pose.position.y = self.y
        odom.pose.pose.position.z = 0.0

        q = quaternion_from_euler(0, 0, self.theta)
        odom.pose.pose.orientation = Quaternion(x=q[0], y=q[1], z=q[2], w=q[3])

        self.odom_pub.publish(odom)

        # TF 브로드캐스트
        tf = TransformStamped()
        tf.header.stamp = now
        tf.header.frame_id = 'odom'
        tf.child_frame_id = 'base_link'
        tf.transform.translation.x = self.x
        tf.transform.translation.y = self.y
        tf.transform.translation.z = 0.0
        tf.transform.rotation.x = q[0]
        tf.transform.rotation.y = q[1]
        tf.transform.rotation.z = q[2]
        tf.transform.rotation.w = q[3]

        self.tf_broadcaster.sendTransform(tf)

def main(args=None):
    rclpy.init(args=args)
    node = EncoderOdomNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

