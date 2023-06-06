import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool

class PumpNode(Node):
    def __init__(self):
        super().__init__('pump_node')
        self.subscription = self.create_subscription(
            Bool,
            'pump_control',
            self.callback,
            10
        )
        self.subscription 

        self.pump_pin = 17

    def callback(self, msg):
        msg.data = bool(int(msg.data))

def main(args=None):
    rclpy.init(args=args)
    subscriber_node = PumpNode()
    rclpy.spin(subscriber_node)
    subscriber_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
