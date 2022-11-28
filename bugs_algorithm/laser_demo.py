import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan

LIDAR_TOPIC = "/scan"

class MyNode(Node):
    def __init__(self):
        node_name="lidar"
        super().__init__(node_name)
        self.__laser_sub = self.create_subscription(LaserScan, LIDAR_TOPIC, self.__lidar_handler, 10)
        self.__laser_sub
        self.get_logger().info("LIDAR Demo")

    def __lidar_handler(self, msg: LaserScan) -> None:
        regions = {
            'right':  min(min(msg.ranges[0:127]), 10),
            'fright': min(min(msg.ranges[128:255]), 10),
            'front':  min(min(msg.ranges[256:383]), 10),
            'fleft':  min(min(msg.ranges[384:511]), 10),
            'left':   min(min(msg.ranges[512:640]), 10),
        }
        self.get_logger().info("Hello ROS2")
        self.get_logger().info(str(regions))


def main(args=None):
    rclpy.init(args=args)
    node = MyNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()