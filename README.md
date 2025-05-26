# Klipper-sk6812
a way to use SK6812 LED strips with Klipper on a Raspberry PI

🔧 Installation Instructions for SK6812 LED Control with Klipper
This guide will walk you through installing SK6812 RGBW LED effects support for Klipper via a background service and Klipper macros.

✅ Requirements
Raspberry Pi running Raspberry Pi OS

Klipper installed (e.g. via KIAUH)

SK6812 RGBW LED strip wired to GPIO (defaults to GPIO D10)

5V external power supply for LEDs (recommended) - I run mine direct off my RPI GPIO without any problems (yet)

📁 Step 1: Clone the Repository
bash
Copy
Edit
cd ~
git clone https://github.com/slothking87/Klipper-sk6812.git
cd Klipper-sk6812
📦 Step 2: Install Dependencies
bash
Copy
Edit
sudo apt update
sudo apt install python3-pip
pip3 install rpi_ws281x adafruit-circuitpython-neopixel
🧠 neopixel library handles SK6812 RGBW support. No additional kernel modules are required.

🧠 Step 3: Setup the LED Control Service
Copy the systemd service:

bash
Copy
Edit
sudo cp klipper_led.service /etc/systemd/system/klipper_led.service
Enable and start the service:

bash
Copy
Edit
sudo systemctl daemon-reexec
sudo systemctl enable klipper_led.service
sudo systemctl start klipper_led.service
This runs led_control.py in the background and listens for commands via /tmp/led_command.

🧩 Step 4: Add Klipper Macros
Copy the macro file into your Klipper config folder (or include it in your main config):

bash
Copy
Edit
cp klipper_led_macros.cfg ~/printer_data/config/
Include it in your printer.cfg:

ini
Copy
Edit
[include klipper_led_macros.cfg]
This file contains:

Commands like LED_FADE, LED_WHITE, LED_RAINBOW, etc.

Automatic LED effects for printer states (start, error, complete).

▶️ Step 5: Use the Macros
From Fluidd, Mainsail, or via G-code:

LED_FADE — Fade effect (e.g. bed heating)

LED_WHITE — Solid white (e.g. printing)

LED_RAINBOW — Completion

LED_THEATER — Error

LED_OFF — Turns off the strip

⚙️ Customization
Change LED pin or count in led_control.py:

python
Copy
Edit
LED_PIN = board.D10
LED_COUNT = 50
Add more effects to the EFFECTS dictionary inside led_control.py.

🧪 Test It Manually (Optional)
To test an effect directly:

bash
Copy
Edit
echo red > /tmp/led_command
✅ Done!
Your LEDs should now respond to printer state automatically using the macros provided!
