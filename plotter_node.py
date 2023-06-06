import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from influxdb import InfluxDBClient

class PlotterNode(Node):
    def __init__(self):
        super().__init__('plotter_node')
        self.subscription = self.create_subscription(String, 'moisture_status', self.listener_callback, 10)
        self.subscription

        self.client = InfluxDBClient(host='localhost', port=8086)
        self.client.switch_database('status')

    def listener_callback(self, msg):
        status, moisture_level = msg.data.split(", ")
        can_activate_pump = int(status.split(": ")[1] == 'True')
        moisture_level = int(moisture_level.split(": ")[1])
        
        json_body = [
            {
                "measurement": "moisture_status",
                "tags": {
                    "source": "ros2_node",
                },
                "fields": {
                    "Can activate pump": can_activate_pump,
                    "moisture level": moisture_level,
                }
            }
        ]
        self.get_logger().info('Listening and writing: ')
        self.client.write_points(json_body)


def main(args=None):
    rclpy.init(args=args)
    plotter_node = PlotterNode()
    rclpy.spin(plotter_node)
    plotter_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
