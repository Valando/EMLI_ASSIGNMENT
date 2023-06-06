import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from std_msgs.msg import Bool

class StateNode(Node):
    def __init__(self):
        super().__init__('state_node')
        self.button_subscriber = self.create_subscription(String, 'button_state', self.button_callback, 10)
        self.alarm_subscriber = self.create_subscription(Bool, 'alarm', self.alarm_callback, 10)
        self.run_pump_subscriber = self.create_subscription(Bool, 'run_pump', self.pump_run_callback, 10)
        self.alarm_state = False
        self.pump_12hr = False
        self.button_count = 0
        self.motor_status = False
        self.publisher = self.create_publisher(String, 'pump_control', 10)

    def pump_run_callback(self, msg):
        self.pump_12hr = msg.data
        self.pump_control_logic()

    def button_callback(self, msg):
        button_count, motor_status = msg.data.strip("[]").split(",")
        self.button_count = int(button_count.strip())
        self.motor_status = bool(motor_status.strip())
        self.pump_control_logic()
    
    def alarm_callback(self, msg):
        self.alarm_state = msg.data
        self.pump_control_logic()
        
    def pump_control_logic(self):
        msg = Bool()
        if self.alarm_state:
            msg.data = False
        else:
            msg.data = self.motor_status or self.pump_12hr
        self.get_logger().info('Publishing: "%s"' % msg.data)
        self.publisher_.publish(msg)
    
def main(args=None):
    rclpy.init(args=args)
    state_node = StateNode()
    rclpy.spin(state_node)
    state_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
