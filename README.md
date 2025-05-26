# SK6812 LED Control for Klipper

This guide walks you through installing and configuring SK6812 RGBW LED strip support for Klipper using a background service and G-code macros.

---

## ✨ Features

* Smooth color and animation effects
* Triggered by printer states (e.g., printing, error, complete)
* Configurable via standard G-code macros

---

## ✅ Requirements

* Raspberry Pi with Raspberry Pi OS
* Klipper installed (e.g., via [KIAUH](https://github.com/dw-0/kiauh))
* SK6812 RGBW LED strip connected to GPIO pin (default: `D10`)
* External 5V power supply for LEDs

---

## 📁 Step 1: Clone the Repository

```bash
cd ~
git clone https://github.com/slothking87/Klipper-sk6812.git
cd Klipper-sk6812
```

---

## 📦 Step 2: Install Python Dependencies

```bash
sudo apt update
sudo apt install python3-pip
pip3 install rpi_ws281x adafruit-circuitpython-neopixel
```

> 🧠 The `neopixel` library provides RGBW LED support.

---

## 🤔 Step 3: Setup the LED Control Service

1. Copy the service file:

```bash
sudo cp klipper_led.service /etc/systemd/system/klipper_led.service
```

2. Enable and start the service:

```bash
sudo systemctl daemon-reexec
sudo systemctl enable klipper_led.service
sudo systemctl start klipper_led.service
```

> This starts `led_control.py` and listens for LED effect commands via `/tmp/led_command`.

---

## 🧰 Step 4: Add Klipper Macros

1. Copy the macro file to your Klipper config directory:

```bash
cp klipper_led_macros.cfg ~/printer_data/config/
```

2. Include it in your `printer.cfg`:

```ini
[include klipper_led_macros.cfg]
```

This file contains:

* Macros for solid colors and effects (e.g. `LED_RED`, `LED_RAINBOW`, etc.)
* Automatic triggers for printer states like heating, printing, error, and completion

---

## ▶️ Step 5: Use the Macros

Send these G-code commands via your interface (Fluidd, Mainsail, etc):

* `LED_FADE` — Fading effect during heating
* `LED_WHITE` — Solid white during print
* `LED_THEATER` — Theater chase on error
* `LED_RAINBOW` — Rainbow cycle on print complete
* `LED_OFF` — Turn off LEDs

---

## 📆 Step 6: Test Manually (Optional)

To verify the service is working:

```bash
echo red > /tmp/led_command
```

---

## ⚙️ Customization

Edit `led_control.py` to change pin or LED count:

```python
LED_PIN = board.D10
LED_COUNT = 50
```

Add more colors/effects to the `EFFECTS` dictionary.

---

## ✅ Done!

Your LEDs are now integrated with Klipper and respond to printer states.

Need help or want to contribute? Open an issue or PR on [GitHub](https://github.com/slothking87/Klipper-sk6812).
