#!/bin/bash
echo "Run in non virtual environment (might not work in virtual environment)"
deactivate

# Clean previous builds
echo "Removing build, install, and log directories..."
rm -rf build/ install/ log/

# Source the ROS 2 workspace environment
echo "Sourcing ROS 2 environment..."
source /opt/ros/jazzy/setup.bash

# Build the workspace using colcon
echo "Starting colcon build..."
colcon build
echo "Build completed!"