# Use the official ROS 2 Jazzy image
FROM ros:jazzy

# Set the working directory inside the container
WORKDIR /workspace

# Install system dependencies with explicit Python 3.12
RUN apt-get update && apt-get install -y \
    build-essential \
    python3.12-venv \
    python3-colcon-common-extensions \
    python3-pip \
    libusb-1.0-0-dev \
    udev \
    wget \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# Phidget22 Libraries for stepper motor (note: might need $(lsb_release -sc)-raspbian)
RUN wget -qO /usr/share/keyrings/phidgets.gpg \
    https://www.phidgets.com/gpgkey/pubring.gpg \
    && echo deb [signed-by=/usr/share/keyrings/phidgets.gpg] \
    http://www.phidgets.com/debian $(lsb_release -sc) main \
    > /etc/apt/sources.list.d/phidgets.list \
    && apt-get update \
    && apt-get install libphidget22

# Copy udev rules file... I'm pretty sure I need to do this on host ngl
COPY phidgets.rules /etc/udev/rules.d/99-phidgets.rules

# Copy the entire project into the container
COPY . /workspace/

# Create virtual environment (using system Python)
RUN python3 -m venv --copies /opt/venv

# Install Python dependencies in virtual environment
RUN /opt/venv/bin/pip install --no-cache-dir -r /workspace/requirements.txt

# Build ROS workspace with environment activation
RUN . /opt/ros/jazzy/setup.sh && \
    colcon build

# Ensure launch script is executable
RUN chmod +x /workspace/launch.sh

# Source ROS environments, activate virtualenv, and launch application
CMD ["/bin/bash", "-c", "source /opt/ros/jazzy/setup.sh && \
    source /workspace/install/setup.sh && \
    export PYTHONPATH=$PYTHONPATH:/opt/venv/lib/python3.12/site-packages && \
    exec ./launch.sh"]