import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Quaternion, Pose, Point, Twist, Vector3
from tf_transformations import quaternion_from_euler

class StaticOdomPublisher(Node):
    def __init__(self):
        super().__init__('static_odom_publisher')
        self.odom_pub = self.create_publisher(Odometry, 'odom', 10)
        self.timer = self.create_timer(0.1, self.publish_odom)

    def publish_odom(self):
        msg = Odometry()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'odom'
        msg.child_frame_id = 'base_link'

        # 위치 0,0,0
        msg.pose.pose.position = Point(x=0.0, y=0.0, z=0.0)
        q = quaternion_from_euler(0, 0, 0)
        msg.pose.pose.orientation = Quaternion(x=q[0], y=q[1], z=q[2], w=q[3])

        # 속도 0
        msg.twist.twist.linear = Vector3(x=0.0, y=0.0, z=0.0)
        msg.twist.twist.angular = Vector3(x=0.0, y=0.0, z=0.0)

        self.odom_pub.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = StaticOdomPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

