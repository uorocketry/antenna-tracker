#!/bin/bash
source .venv/bin/activate
source install/setup.bash
export PYTHONPATH=$PYTHONPATH:/home/blinn/Rocketry/antenna-tracker/AntennaTrackerWS/.venv/lib/python3.12/site-packages

#!/bin/bash

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

echo "Activating ROS Workstation environment..."
source install/setup.bash

# Set PYTHONPATH for ROS 2 workspace
VENV_PYTHONPATH="/home/blinn/Rocketry/antenna-tracker/AntennaTrackerWS/.venv/lib/python3.12/site-packages"

echo "Setting PYTHONPATH..."
export PYTHONPATH=$PYTHONPATH:$VENV_PYTHONPATH

echo "Setup complete!"