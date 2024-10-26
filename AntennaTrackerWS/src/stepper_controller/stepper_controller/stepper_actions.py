from rclpy.action import ActionServer, CancelResponse, GoalResponse
from stepper_interfaces.action import MoveToTargetPosition
from std_msgs.msg import String
import time

def setup_actions(self):

    # Actions
    self.move_to_target_position_act = ActionServer( #shorthand MTTPA
        self,
        MoveToTargetPosition,
        '/stepper_controller/move_to_target_position',
        self.mttpa_execute_callback, # execute action
        goal_callback=self.mttpa_goal_callback, # Goal acceptance
        cancel_callback=self.mttpa_cancel_callback # cancel action
    )
    return

# Action callbacks
def mttpa_execute_callback(self, goal_handle):
    target_position = goal_handle.request.target_position

    self.setTargetPosition(target_position)

    
    feedback_msg = MoveToTargetPosition.Feedback()
    feedback_msg.current_position = self.getCurrentPosition() # could be an error point (but fuck it)
    is_moving = True

    # Initialize result
    result = MoveToTargetPosition.Result()  
    result.success = False  # Assume failure
    result.final_position = feedback_msg.current_position  # Initialize with current position

    while is_moving:
        try:
            is_moving = self.getIsMoving()
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                return result
            feedback_msg.current_position = self.getCurrentPosition()
            goal_handle.publish_feedback(feedback_msg)
        except self.PhidgetException as e:
            errorMsg = str(e)
            msg = String()
            msg.data = errorMsg
            self.error_pub.publish(msg)
            self.get_logger().error(msg.data)

            goal_handle.abort()
            result.success = False  # Mark goal as failed
            result.final_position = feedback_msg.current_position  # Update to current position
            return result

        # wait before checking again
        time.sleep(0.1)

    goal_handle.succeed()

    #return the result
    result.success = True
    result.final_position = feedback_msg.current_position
    return result
    
def mttpa_goal_callback(self, goal_request):
    # This could be made into a queue, but I'm not certain its needed
    self.get_logger().info("Move To Target Position called")
    try:
        if self.getIsMoving():
            self.get_logger().info("Rejected Move To Target Position, due to already moving")
            return GoalResponse.REJECT
    except self.PhidgetException as e:
        errorMsg = str(e)
        msg = String()
        msg.data = errorMsg
        self.error_pub.publish(msg)
        self.get_logger().error(msg.data)
        return GoalResponse.REJECT
    
    self.get_logger().info("Accepted Move To Target Position")
    return GoalResponse.ACCEPT
    # Add logic for if target position is within valid range (idk what our valid range is rn)
        
def mttpa_cancel_callback(self, goal_handle):
    try:
        # Stop movement if it's currently moving
        if self.getIsMoving():
            self.setTargetPosition(self.getPosition())  # Tell stepper target location is current location to stop
        return CancelResponse.ACCEPT

    except self.PhidgetException as e:
        errorMsg = str(e)
        msg = String()
        msg.data = errorMsg
        self.error_pub.publish(msg)
        self.get_logger().error(msg.data)
        return CancelResponse.REJECT