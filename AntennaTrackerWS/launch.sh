#!/bin/bash
echo "Sourcing ROS workstation"
source install/setup.bash
echo "if it fails/crashes at some point. Then it's probably environment related"
ros2 launch ./launch/antenna_launch.py