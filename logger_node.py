import os
import time
import rclpy
from rclpy.node import Node
from influxdb import InfluxDBClient

class LoggerNode(Node):
    def __init__(self):
        super().__init__('logger_node')
        self.log_file = '/home/EMLI_TEAM_24/log/healthlogging.log'
        self.last_mod_time = os.path.getmtime(self.log_file)
        self.influxdb_client = InfluxDBClient(host='localhost', port=8086)
        self.influxdb_client.switch_database('rpi_health')

        self.create_timer(10.0, self.callback) 

    def callback(self):
        mod_time = os.path.getmtime(self.log_file)
        if mod_time != self.last_mod_time:
            self.last_mod_time = mod_time
            with open(self.log_file, 'r') as f:
                lines = [line for line in f.read().splitlines() if line] 
                data = lines[-9:] if len(lines) >= 9 else lines

                measurements = dict(item.split(': ') for item in '\n'.join(data).split('\n') if ': ' in item)
                json_body = [{'measurement': key, 'fields': {'value': float(clean_data(value).split()[0])}} for key, value in measurements.items()]
                self.influxdb_client.write_points(json_body)
    
def clean_data(value):
    for ch in ['°C', 'KB', '%']:
        if ch in value:
            value = value.replace(ch, '')
    return value

def main(args=None):
    rclpy.init(args=args)

    logger_node = LoggerNode()

    rclpy.spin(logger_node)

    logger_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
