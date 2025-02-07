# uOttawa Rocketry Antenna Tracker
Summed up, track the rocket and follow it with an antenna

## Important info
Currently this repository is split into 2 sections. \
Antenna_Tracker_Code (legacy repository) \
& \
AntennaTrackerWS (in work repository)

## How to build yourself (on Ubuntu)
Install These technologies \
[Python3](https://www.python.org/) \
[ROS 2 Jazzy Jalisco](https://docs.ros.org/en/jazzy/index.html) \

Run these commands
```bash
git clone <repo-url>
cd antenna-tracker/AntennaTrackerWS
python -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
```
## Notes
When running colcon build, make sure to deactivate the virtual enviroment. \
```bash
sudo apt install ros-jazzy-mavros
wget https://raw.githubusercontent.com/mavlink/mavros/ros2/mavros/scripts/install_geographiclib_datasets.sh
./install_geographiclib_datasets.sh
```