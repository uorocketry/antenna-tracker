from setuptools import find_packages, setup

package_name = 'stepper_controller'

setup(
    name=package_name,
    version='0.0.1',
    packages=find_packages(include=['stepper_controller', 'stepper_controller.*'], exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools', 'Phidget22', 'rclpy', 'time'],
    zip_safe=True,
    maintainer='blinn',
    maintainer_email='blinn@todo.todo',
    description='Stepper Controller package for controlling and managing stepper motors using ROS 2 and Phidget22.',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'stepper_controller = stepper_controller.stepper_controller_node:main',
        ],
    },
)
