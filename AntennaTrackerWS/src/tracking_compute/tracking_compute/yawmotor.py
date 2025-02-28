from rclpy.node import Node
from rclpy.action import ActionClient
from std_msgs.msg import Float64, String, Bool
from stepper_interfaces.srv import AddPositionOffset, SetEngaged
from stepper_interfaces.action import MoveToTargetPosition

from std_msgs.msg import String

class yawMotor:
    def __init__(self, node: Node):
        self.node = node
        self.node.get_logger().info("Yaw Motor initialized within TrackingComputeNode")

        # variables
        self.position = 0.0

        # subscriptions
        self.sc_error_sub = self.node.create_subscription(String, '/stepper_controller/error', self.sc_error_callback, 10)
        self.sc_position_sub = self.node.create_subscription(Float64, '/stepper_controller/position', self.sc_error_callback, 10)
        self.sc_is_moving_sub = self.node.create_subscription(Bool, '/stepper_controller/is_moving', self.sc_error_callback, 10)
        self.sc_is_attached_sub = self.node.create_subscription(Bool, '/stepper_controller/is_attached', self.sc_error_callback, 10)

        # services
        self.add_position_offset_cli = self.node.create_client(AddPositionOffset, '/stepper_controller/add_position_offset')
        while not self.add_position_offset_cli.wait_for_service(timeout_sec=1.0):
            self.node.get_logger().info('AddPositionOffset not available, waiting again...')

        self.set_engaged_cli = self.node.create_client(SetEngaged, '/stepper_controller/set_engaged')
        while not self.set_engaged_cli.wait_for_service(timeout_sec=1.0):
            self.node.get_logger().info('SetEngaged not available, waiting again...')

        # actions
        self.move_to_target_position_acli = ActionClient(self.node, MoveToTargetPosition, '/stepper_controller/move_to_target_position')

    # yaw motor functions
    def move(self, target):
        self.send_move_to_target_position_goal(target)
        return
    
    def toggle_engagement(self, bool):
        self.send_set_engaged_request(bool)
        return
    
    def get_position(self):
        return self.position
    
    # Make the position go to 0
    def position_offset(self):
        offset = -self.position
        self.send_add_position_offset_request(offset)
        return

    # Subscription Callbacks
    def sc_error_callback(self, msg):
        self.node.get_logger().info(f"Error: {msg.data}")

    def sc_position_callback(self, msg):
        self.node.get_logger().info(f"Current Position: {msg.data}")
        self.position = int(msg.data)

    def sc_is_moving_callback(self, msg):
        self.node.get_logger().info(f"Is Moving: {msg.data}")

    def sc_is_attached_callback(self, msg):
        self.node.get_logger().info(f"Is Attached: {msg.data}")

    # Service Calls
    def send_add_position_offset_request(self, offset):
        """Send a request to add a position offset."""
        req = AddPositionOffset.Request()
        req.offset = offset
        future = self.add_position_offset_cli.call_async(req)
        future.add_done_callback(self.add_position_offset_response)

    def add_position_offset_response(self, future):
        try:
            response = future.result()
            self.node.get_logger().info(f"AddPositionOffset Response: {response.success}")
        except Exception as e:
            self.node.get_logger().error(f"Service call failed: {e}")

    def send_set_engaged_request(self, engaged):
        req = SetEngaged.Request()
        req.engaged = engaged

        future = self.set_engaged_cli.call_async(req)
        future.add_done_callback(self.callback_set_engaged_response)

    def callback_set_engaged_response(self, future):
        try:
            response = future.result()
            if response.success:
                self.node.get_logger().info('Successfully set engaged state.')
            else:
                self.node.get_logger().error('Failed to set engaged state.')
        except Exception as e:
            self.node.get_logger().error(f'Service call failed: {e}')

    # Action Calls
    def send_move_to_target_position_goal(self, target):
        """Send an action goal to move to a target position."""
        goal_msg = MoveToTargetPosition.Goal()
        goal_msg.target_position = target

        self.node.get_logger().info(f"Sending goal: {goal_msg.target_position}")
        self.move_to_target_position_acli.wait_for_server()
        self._send_goal_future = self.move_to_target_position_acli.send_goal_async(
            goal_msg
        )
        self._send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.node.get_logger().info("Goal rejected")
            return

        self.node.get_logger().info("Goal accepted")
        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        result = future.result().result
        self.node.get_logger().info(f"Result: {result.success}")