#!/bin/bash

echo "=== Klipper SK6812 LED Setup Script ==="

# Exit immediately if a command exits with a non-zero status
set -e

# Define paths
SCRIPT_DIR="/home/pi/Klipper-SK6812_LED_Status"
SERVICE_FILE="led_control.service"
SERVICE_PATH="/etc/systemd/system/led_control.service"

# Step 1: Update package list and install Python pip
echo "Installing Python dependencies..."
sudo apt update
sudo apt install -y python3-pip

# Step 2: Install required Python libraries
pip3 install --upgrade adafruit-circuitpython-neopixel rpi_ws281x

# Step 3: Allow non-root access to GPIO
echo "Enabling SPI and setting GPIO permissions..."
sudo raspi-config nonint do_spi 0
sudo usermod -a -G gpio pi

# Step 4: Copy the service file to systemd
echo "Installing systemd service..."
sudo cp "$SCRIPT_DIR/$SERVICE_FILE" "$SERVICE_PATH"
sudo chmod 644 "$SERVICE_PATH"

# Step 5: Reload systemd, enable and start the service
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl enable led_control.service
sudo systemctl restart led_control.service

echo "Setup complete. LED Control service is running."
echo "You can check status with: sudo systemctl status led_control.service"
