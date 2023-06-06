import os
import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool

class MoistPublisher(Node):
    def __init__(self):
        super().__init__('moist_publisher')
        self.moisture_publisher_ = self.create_publisher(Bool, 'moisture', 10)
        self.run_pump_publisher_ = self.create_publisher(Bool, 'run_pump', 10)
        self.timer = self.create_timer(1.0, self.timer_callback)
        self.prev_script_value = None

    def read_script_value(self):
        script_file_path = "/home/EMLI_TEAM_24/log/motorcontrol.csv"
        if os.path.isfile(script_file_path):
            with open(script_file_path, 'r') as file:
                last_line = file.readlines()[-1]
                return int(last_line.strip())
        else:
            self.get_logger().error(f"Cannot read file: {script_file_path}")
            return None

    def timer_callback(self):
        moisture_value = 10 # Change this to read actual moisture sensor value
        status = moisture_value < 10
        moisture_msg = Bool()
        moisture_msg.data = status
        self.moisture_publisher_.publish(moisture_msg)

        script_value = self.read_script_value()
        run_pump_msg = Bool()

        if script_value is not None and script_value != self.prev_script_value and status:
            run_pump_msg.data = True
        else:
            run_pump_msg.data = False

        self.run_pump_publisher_.publish(run_pump_msg)
        self.prev_script_value = script_value

def main(args=None):
    rclpy.init(args=args)
    moist_publisher = MoistPublisher()
    rclpy.spin(moist_publisher)
    moist_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
