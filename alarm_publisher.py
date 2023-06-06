import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool
import subprocess

class MoisturePublisher(Node):
    def __init__(self):
        super().__init__('water_moisture_publisher')
        self.publisher = self.create_publisher(Bool, 'moisture', 10)
        time_period = 0.5
        self.timer = self.create_timer(time_period, self.publish_moisture)  # timer on 0.5 second

    def publish_moisture(self):
        # subprocess, used to execute secondary script
        process = subprocess.Popen(['python3', 'moisture.py'], stdout=subprocess.PIPE)
        data = process.communicate()

        # moisture
        moisture = data[0]

        # message as boolean
        msg = Bool()
        msg.data = bool(moisture)

        # publish message
        self.publisher.publish(msg)
        self.get_logger().info('Published moisture data: %s' % moisture)

def main(args=None):
    rclpy.init(args=args)
    publisher = MoisturePublisher()
    rclpy.spin(publisher)
    publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
