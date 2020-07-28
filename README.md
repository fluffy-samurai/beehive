# Beehive Automation

Most of my code uses the base provided at: https://github.com/sparkfun/Qwiic-Kit-for-Pi

This if from the tutorial linked here: https://learn.sparkfun.com/tutorials/qwiic-kit-for-raspberry-pi-hookup-guide#python-library

## Requirements

- Raspberry Pi 4
- [Qwiic pHat](https://www.sparkfun.com/products/15945)
- [Qwiic Environmental Combo Breakout](https://www.sparkfun.com/products/14348)

## Initial Setup

- Set up splunk variables in `main.py`
- Using the config tool (`sudo raspi-config`), enable I2C pins.
- Add the following lines to the `/boot/config.txt`:
```
# Enable I2C clock stretching
dtparam=i2c_arm_baudrate=10000
```
- Reboot your Raspberry Pi
- Install the Python dependencies
- Run `main.py`