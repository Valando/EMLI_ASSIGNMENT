from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='plotlogger',
            executable='logger_node',
            namespace='Logger',
            name='RPI_logger'
        )
        # Node(
        #     package='plotlogger',
        #     executable='plotter_node',
        #     namespace='Plotter',
        #     name='Plant_system_plotter'
        # ),
    ])