import time
import board
import neopixel
import threading
import signal
import sys
import os

# Configuration
LED_PIN = board.D10             # GPIO pin for data
LED_COUNT = 50                  # Number of LEDs
BRIGHTNESS = 1.0                # 0.0 to 1.0
LED_ORDER = neopixel.GRBW       # For SK6812 RGBW

# NeoPixel setup
pixels = neopixel.NeoPixel(
    LED_PIN, LED_COUNT, brightness=BRIGHTNESS, auto_write=False, pixel_order=LED_ORDER
)

# Globals
stop_event = threading.Event()
current_thread = None
command_file = "/tmp/led_command"

def set_all(color):
    for i in range(LED_COUNT):
        pixels[i] = color
    pixels.show()

def rainbow_cycle(wait=0.01):
    def wheel(pos):
        if pos < 85:
            return (pos * 3, 255 - pos * 3, 0, 0)
        elif pos < 170:
            pos -= 85
            return (255 - pos * 3, 0, pos * 3, 0)
        else:
            pos -= 170
            return (0, pos * 3, 255 - pos * 3, 0)

    while not stop_event.is_set():
        for j in range(256):
            for i in range(LED_COUNT):
                pixel_index = (i * 256 // LED_COUNT) + j
                pixels[i] = wheel(pixel_index & 255)
            pixels.show()
            time.sleep(wait)
            if stop_event.is_set():
                break

def theater_chase(wait=0.1):
    while not stop_event.is_set():
        for q in range(3):
            for i in range(0, LED_COUNT, 3):
                if i + q < LED_COUNT:
                    pixels[i + q] = (255, 255, 255, 0)
            pixels.show()
            time.sleep(wait)
            for i in range(0, LED_COUNT, 3):
                if i + q < LED_COUNT:
                    pixels[i + q] = (0, 0, 0, 0)

def strobe(wait=0.05):
    while not stop_event.is_set():
        set_all((255, 255, 255, 0))
        time.sleep(wait)
        set_all((0, 0, 0, 0))
        time.sleep(wait)

def fade(wait=0.05):
    brightness = 0
    direction = 1
    while not stop_event.is_set():
        color = (brightness, brightness, brightness, 0)
        set_all(color)
        brightness += direction * 5
        if brightness >= 255 or brightness <= 0:
            direction *= -1
        time.sleep(wait)

def color_effect(r, g, b, w=0):
    while not stop_event.is_set():
        set_all((r, g, b, w))
        time.sleep(0.1)

EFFECTS = {
    "rainbow": rainbow_cycle,
    "theater": theater_chase,
    "strobe": strobe,
    "fade": fade,
    "red": lambda: color_effect(255, 0, 0),
    "green": lambda: color_effect(0, 255, 0),
    "blue": lambda: color_effect(0, 0, 255),
    "white": lambda: color_effect(0, 0, 0, 255),
    "yellow": lambda: color_effect(255, 255, 0),
    "purple": lambda: color_effect(128, 0, 128),
    "cyan": lambda: color_effect(0, 255, 255),
    "off": lambda: set_all((0, 0, 0, 0)),
}

def signal_handler(sig, frame):
    stop_event.set()
    set_all((0, 0, 0, 0))
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

def run_effect(effect_func):
    global current_thread, stop_event
    stop_event.set()  # Stop previous thread
    if current_thread and current_thread.is_alive():
        current_thread.join()

    stop_event.clear()
    current_thread = threading.Thread(target=effect_func)
    current_thread.start()

def main():
    print("LED control script started, listening for effect changes...")
    last_command = ""

    # Ensure the command file exists
    if not os.path.exists(command_file):
        with open(command_file, "w") as f:
            f.write("off")

    while True:
        try:
            with open(command_file, "r") as f:
                command = f.read().strip().lower()
        except Exception:
            command = "off"

        if command != last_command and command in EFFECTS:
            print(f"Running effect: {command}")
            run_effect(EFFECTS[command])
            last_command = command

        time.sleep(0.2)

if __name__ == "__main__":
    main()
