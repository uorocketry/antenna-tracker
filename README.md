# uOttawa Rocketry Antenna Tracker
Summed up, track the rocket and follow it with an antenna

## Important info
Currently this repository is split into 2 sections. \
Antenna_Tracker_Code (legacy repository) \
& \
AntennaTrackerWS (in work repository)

**Switch Information** \
Pull Down Switches \
Yaw Switch = Pin 15 = GPIO 22 \
Pitch Switch = Pin 16 = GPIO 23 \
Refer to [pineout.xyz](https://pinout.xyz/)

## Build options
There are currently 2 ways to build this program. \
    1. Docker \
    2. Ubuntu 24.04 LTS

If you just plan to only use this program. I recommend using docker compose.

**Initial step** \
Clone repository
```bash
git clone <repo-url>
cd antenna-tracker/AntennaTrackerWS
```
### Docker compose
In docker-compose.yml set the environment variable to what is required for your use case.

```
environment:
      - MOCK_GPIO=1
      - OSCILLATE_SWITCHES=1
      - ROS_DOMAIN_ID=${ROS_DOMAIN_ID:-0}
```
Then run
```bash
docker compose up
```
### Ubuntu 24.04 LTS
Install These technologies \
[Python3](https://www.python.org/) \
[ROS 2 Jazzy Jalisco](https://docs.ros.org/en/jazzy/index.html)

**Run these commands**

Install mavros
```bash
sudo apt install ros-jazzy-mavros
wget https://raw.githubusercontent.com/mavlink/mavros/ros2/mavros/scripts/install_geographiclib_datasets.sh
./install_geographiclib_datasets.sh
```
Install Phidget22 Libraries
```bash
curl -fsSL https://www.phidgets.com/downloads/setup_linux | sudo -E bash -
sudo apt install -y libphidget22
```
Install gpiozero
```bash
sudo apt install gpiozero
```
Install Python deps
```bash
python -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
```
## Notes
When running colcon build, make sure to deactivate the virtual enviroment.