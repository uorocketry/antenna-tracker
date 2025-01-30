from std_msgs.msg import String
from stepper_interfaces.srv import AddPositionOffset, GetVelocity, GetAcceleration, SetAcceleration, GetEngaged, SetEngaged

def setup_services(self):

    # Services
    self.add_position_offset_srv = self.create_service(AddPositionOffset, '/stepper_controller/add_position_offset', add_position_offset_callback)

    self.get_acceleration_srv = self.create_service(GetAcceleration, '/stepper_controller/get_acceleration', get_acceleration_callback)
    self.set_acceleration_srv = self.create_service(SetAcceleration, '/stepper_controller/set_acceleration', set_acceleration_callback)

    self.get_velocity_srv = self.create_service(GetVelocity, '/stepper_controller/get_velocity', get_velocity_callback)

    self.get_engaged_srv = self.create_service(GetEngaged, '/stepper_controller/get_engaged', get_engaged_callback)
    self.set_engaged_srv = self.create_service(SetEngaged, '/stepper_controller/set_engaged', set_engaged_callback)

    # currently baked in code (or default values), but could be a service one day - The List
    # setCurrentLimit, setMinVelocity, setMaxVelocity

    # Add a get info on board service? Such as, board serial number?
    return

def add_position_offset_callback(self, request, response):
    self.get_logger().info("add_position_offset called")
    try:
        self.stepper.addPositionOffset(request.offset)
        response.success = True
    except self.PhidgetException as e:
        errorMsg = str(e)
        msg = String()
        msg.data = errorMsg
        self.error_pub.publish(msg)
        self.get_logger().error(msg.data)
        response.success = False
    return response

def get_acceleration_callback(self, request, response):
    self.get_logger().info("get_acceleration called")
    try:
        response.acceleration = self.stepper.getAcceleration()
        response.success = True
    except self.PhidgetException as e:
        errorMsg = str(e)
        msg = String()
        msg.data = errorMsg
        self.error_pub.publish(msg)
        self.get_logger().error(msg.data)
        response.acceleration = 0.0 # default value (on error)
        response.success = False
    return response

def set_acceleration_callback(self, request, response):
    self.get_logger().info("set_acceleration called")
    try:
        self.stepper.setAcceleration(request.acceleration)
        response.success = True
    except self.PhidgetException as e:
        errorMsg = str(e)
        msg = String()
        msg.data = errorMsg
        self.error_pub.publish(msg)
        self.get_logger().error(msg.data)
        response.success = False
    return response

def get_velocity_callback(self, request, response):
    self.get_logger().info("get_velocity called")
    try:
        response.velocity = self.stepper.getVelocity()
        response.success = True
    except self.PhidgetException as e:
        errorMsg = str(e)
        msg = String()
        msg.data = errorMsg
        self.error_pub.publish(msg)
        self.get_logger().error(msg.data)
        response.velocity = 0.0 # default return value (on error)
        response.success = False
    return response

def get_engaged_callback(self, request, response):
    self.get_logger().info("get_engaged called")
    try:
        response.engaged = self.stepper.getEngaged()
        response.success = True
    except self.PhidgetException as e:
        errorMsg = str(e)
        msg = String()
        msg.data = errorMsg
        self.error_pub.publish(msg)
        self.get_logger().error(msg.data)
        response.engaged = False # default return value (on error)
        response.success = False
    return response

def set_engaged_callback(self, request, response):
    self.get_logger().info("set_engaged called")
    try:
        self.stepper.setEngaged(request.engaged)
        response.success = True
    except self.PhidgetException as e:
        errorMsg = str(e)
        msg = String()
        msg.data = errorMsg
        self.error_pub.publish(msg)
        self.get_logger().error(msg.data)
        response.success = False
    return response
