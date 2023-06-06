import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool
from std_msgs.msg import String

class RelayNode(Node):
    def __init__(self):
        super().__init__('relay_node')
        self.subscription_alarm = self.create_subscription(
            Bool,
            'alarm',
            self.alarm_callback,
            10
        )
        self.subscription_moisture = self.create_subscription(
            Bool,
            'moisture',
            self.moisture_callback,
            10
        )
        self.publisher = self.create_publisher(String, 'led_state', 10)

    def alarm_callback(self, msg):
        if msg.data:
            url1 = 'http://192.168.20.222/led/red/on'
            url2 = 'http://192.168.20.222/led/yellow/off'
            url3 = 'http://192.168.20.222/led/green/off'
        else:
            url1 = 'http://192.168.20.222/led/green/on'
            url2 = 'http://192.168.20.222/led/yellow/off'
            url3 = 'http://192.168.20.222/led/red/off'
            
        self.publish_url(url1)
        self.publish_url(url2)
        self.publish_url(url3)
        
    def moisture_callback(self, msg):
        if msg.data:
            url1 = 'http://192.168.20.222/led/yellow/on'
            url2 = 'http://192.168.20.222/led/green/off'
            url3 = 'http://192.168.20.222/led/red/off'
        else:
            url1 = 'http://192.168.20.222/led/green/on'
            url2 = 'http://192.168.20.222/led/yellow/off'
            url3 = 'http://192.168.20.222/led/red/off'

        self.publish_url(url1)
        self.publish_url(url2)
        self.publish_url(url3)
        
    def publish_url(self, url):
        msg = String()
        msg.data = url
        self.publisher.publish(msg)
        self.get_logger().info('Published URL: %s' % url)

def main(args=None):
    rclpy.init(args=args)
    node = RelayNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
