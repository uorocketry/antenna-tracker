#!/usr/bin/env python3
import os
import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool
from gpiozero import Button, Device
from gpiozero.pins.mock import MockFactory  # Import mock components


class switchesNode(Node):

    def __init__(self):
        super().__init__("switches_node")
        self.get_logger().info("ROS2 Limit Switches Node Initialized")

        self.mock_mode = os.environ.get('MOCK_GPIO') == '1'
        self.oscillate = os.environ.get('OSCILLATE_SWITCHES') == '1'        

        # Configure mock GPIO if not on Pi
        if self.mock_mode:
            self.get_logger().info("Using MOCK GPIO")
            Device.pin_factory = MockFactory()

        # Initialize GPIO pins (mock or real based on configuration)
        self.gpio_yaw = Button(22, pull_up=False)  # GPIO 22 == Pin 15
        self.gpio_pitch = Button(23, pull_up=False)  # GPIO 23 == Pin 16

        # Publishers
        self.yaw_pub = self.create_publisher(Bool, '/switch/yaw', 10)
        self.pitch_pub = self.create_publisher(Bool, '/switch/pitch', 10)

        # Set up event listeners
        self.gpio_yaw.when_pressed = self.create_switch_callback(self.gpio_yaw, self.yaw_pub)
        self.gpio_yaw.when_released = self.create_switch_callback(self.gpio_yaw, self.yaw_pub)
        self.gpio_pitch.when_pressed = self.create_switch_callback(self.gpio_pitch, self.pitch_pub)
        self.gpio_pitch.when_released = self.create_switch_callback(self.gpio_pitch, self.pitch_pub)

        if self.mock_mode and self.oscillate:
                self.get_logger().info("Starting test mock switch oscillation")
                self.oscillation_timer = self.create_timer(10, self.toggle_switches)  # Toggle every 10 second
                self.switch_states = {self.gpio_yaw: False, self.gpio_pitch: False}

    def toggle_switches(self):
        """Toggle mock switch states periodically"""
        for switch in [self.gpio_yaw, self.gpio_pitch]:
            new_state = not self.switch_states[switch]
            
            # Directly manipulate mock pin
            if new_state:
                switch.pin.drive_high()
            else:
                switch.pin.drive_low()
            
            self.switch_states[switch] = new_state
            self.get_logger().info(f"Toggled {switch.pin.number} to {'HIGH' if new_state else 'LOW'}")


    def create_switch_callback(self, button, publisher):
        """Factory function to create callbacks with closure context"""
        def callback():
            state = button.is_pressed
            msg = Bool()
            msg.data = state
            publisher.publish(msg)
            self.get_logger().debug(f"GPIO {button.pin} state: {state}")
        return callback

    def on_shutdown(self):
        self.get_logger().info("Shutting down switches node")
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = switchesNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.on_shutdown()
        rclpy.shutdown()


if __name__ == '__main__':
    main()