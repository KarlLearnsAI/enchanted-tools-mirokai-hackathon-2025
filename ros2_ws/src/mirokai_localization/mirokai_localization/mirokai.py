import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from geometry_msgs.msg import PoseStamped
from mirokai_interfaces.srv import GetPose

class Mirokai(Node):
    def __init__(self):
        super().__init__('mirokai_localization')

        # Initialize the current pose
        self.current_pose = PoseStamped()

        # Subscriber to odometry data
        self.odom_subscriber = self.create_subscription(
            Odometry,
            '/odometry/filtered',
            self.odom_callback,
            10
        )
        self.odom_subscriber

        # Sevice to show current pose
        self.current_pose_service = self.create_service(
            GetPose,
            'mirokai_localization/get_current_pose',
            self.handle_get_pose
        )

        self.get_logger().info("Node is running and the service is ready!")
    
    def odom_callback(self, msg):
        self.current_pose.header = msg.header
        self.current_pose.pose = msg.pose.pose
        # position = msg.pose.pose.position
        # orientation = msg.pose.pose.orientation
        # self.get_logger().info(
        #     f'Position: x = {position.x:.2f}, y = {position.y:.2f}, z = {position.z:.2f}'
        # )

    def handle_get_pose(self, request, response):
        pose = self.current_pose
        self.get_logger().info(
            f"Service called! Current posee is: x = {pose.pose.position.x:.2f}, and y = {pose.pose.position.y:.2f}"
        )
        response.pose_stamped = pose
        return response
    
    def __del__(self):
        self.get_logger().info("Node is being destroyed! Disconnecting the robot...")

def main():
    rclpy.init()
    mirokai = Mirokai()
    try:
        rclpy.spin(mirokai)
    except KeyboardInterrupt:
        mirokai.get_logger().info('Node interrupted by user.')
    finally:
        mirokai.get_logger().info('Shutting down.')
        mirokai.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
