#!/bin/bash
source install/setup.bash

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

echo "Activating ROS Workstation environment..."
source install/setup.bash

# Set PYTHONPATH for ROS 2 workspace
#VENV_PYTHONPATH="./.venv/lib/python3.12/site-packages"

echo "Setting PYTHONPATH..."
export PYTHONPATH=$PYTHONPATH:"./.venv/lib/python3.12/site-packages"

echo "Setup complete!"