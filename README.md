# Control Panel

Have you ever wanted all of the hotkeys possible for your computer and all your
apps? This project is intended for you. It uses mostly Adafruit hardware and
CircuitPython to build a highly customizable Control Panel for your computer. It
features light up arcade buttons that are a whole lot of fun to smash.

## Hardware

- Adafruit Feather RP2040
  - [Product Page](https://www.adafruit.com/product/4884)
  - [Learn Page](https://learn.adafruit.com/adafruit-feather-rp2040-pico/overview)
- Adafruit LED Arcade Button 1x4 STEMMA QT
  - [Product Page](https://www.adafruit.com/product/5296)
  - [Learn Page](https://learn.adafruit.com/adafruit-led-arcade-button-qt)
- Rotary Encoder
  - [Product Page](https://www.adafruit.com/product/5880)
  - [Learn Page](https://learn.adafruit.com/adafruit-i2c-qt-rotary-encoder)
- TFT FeatherWing - 2.4" 320x240 Touchscreen v1
  - [Product Page](https://www.adafruit.com/product/3315)
  - [Learn Page](https://learn.adafruit.com/adafruit-2-4-tft-touch-screen-featherwing)
- Arcade Buttons
  - [Green](https://www.adafruit.com/product/3487)
  - [Yellow](https://www.adafruit.com/product/3488)
  - [Red](https://www.adafruit.com/product/3489)
  - [Blue](https://www.adafruit.com/product/3490)
  - [Arcade Button Quick-Connect Wire Pairs](https://www.adafruit.com/product/1152)

### Feather RP2040

- Measures 2.0" x 0.9" x 0.28" (50.8mm x 22.8mm x 7mm) without headers soldered
  in
- 5 grams
- RP2040 32-bit Cortex M0+ dual core running at ~125 MHz @ 3.3V logic and power
- 264 KB RAM
- 8 MB SPI FLASH chip for storing files and CircuitPython/MicroPython code
  storage. No EEPROM
- 21 x GPIO pins with following capabilities:
  - Four 12 bit ADCs (one more than Pico)
  - Two I2C, Two SPI and two UART peripherals
  - 16 x PWM outputs - for servos, LEDs, etc
- 200mA lipoly charger with charging status indicator LED
- Pin #13 red LED for general purpose blinking
- RGB NeoPixel
- On-board STEMMA QT
- Both Reset button and Bootloader select button for quick restarts (no
  unplugging-replugging to relaunch code)
- 3.3V Power/enable pin
- 4 mounting holes
- 12 MHz crystal for perfect timing.
- 3.3V regulator with 500mA peak current output
- USB Type C connector lets you access built-in ROM USB bootloader and serial
  port debugging

![Feather RP2040](https://cdn-learn.adafruit.com/assets/assets/000/100/340/large1024/adafruit_products_FeatherRP_top.jpg?1614788806)

![Feather RP2040 Pinouts](https://cdn-learn.adafruit.com/assets/assets/000/107/203/large1024/adafruit_products_feather-rp2040-pins.png?1639162603)

### Rotary Encoder Details

![Rotary Encoder](https://cdn-shop.adafruit.com/970x728/5880-00.jpg)
![Addresses](https://cdn-learn.adafruit.com/assets/assets/000/127/722/large1024/adafruit_products_rotaryEncTable.png?1708019327)

### Arcade Button Breakout Details

![Button Breakout Board](https://cdn-learn.adafruit.com/assets/assets/000/108/466/large1024/adafruit_products_AQT_top.jpg?1643407292)

![Button Breakout Addresses](https://cdn-learn.adafruit.com/assets/assets/000/108/553/large1024/adafruit_products_seesaw_possible_addresses_by_pin_setting_starting_at_0x3A.png?1643747490)

### 2.4" TFT FeatherWing

![TFT FeatherWing](https://cdn-shop.adafruit.com/970x728/3315-05.jpg)

![TFT FeatherWing Back](https://cdn-learn.adafruit.com/assets/assets/000/125/507/large1024/featherwings_3315-10.jpg?1697817722)
(Note that is the image of the v2. I am using the v1 model for this project.)

## CircuitPython

- [CircuitPython](https://circuitpython.org/)
  - [CircuitPython v9.11](https://circuitpython.org/board/adafruit_feather_rp2040/)
  - [Adafruit HID Library](https://docs.circuitpython.org/projects/hid/en/latest/)
  - [CircuitPython HID Keyboard and Mouse](https://learn.adafruit.com/adafruit-feather-m0-express-designed-for-circuit-python-circuitpython/circuitpython-hid-keyboard-and-mouse)

### Installing CircuitPython

1. [Install instructions from Adafruit](https://learn.adafruit.com/welcome-to-circuitpython/installing-circuitpython)
2. [Download CircuitPython for your board](https://circuitpython.org/)
3. Download the .uf2 file from the sie above
4. Plug the board in to your USB drive
5. Wait a second or two for it to fully boot (likely the LED will be changing
   colors)
6. Hold the `Boot Select` button on the end of the board down while you press
   and release the `Reset` button by the LED
7. The board will restart quickly
8. You will see a new drive on your computer named something like `RPI-RP2`
   (Names may differ depending on the board you're using)
9. Copy the .uf2 file to that drive
10. The device will reboot one more time and you will see another new drive on
    your computer named `CIRCUITPY`
11. Done.

### Cloning this repo directly to your board

By default, git wants to clone repositories to folders, so cloning directly to
the root of a filesystem requires a few extra steps.

```batch
cd e:\
git init
git remote add origin https://github.com/jquintus/ControlPanel
git pull origin main
git branch --set-upstream-to=origin/main main
```

### Update the Circuit Python Bundles

1. Go to the [CircuitPython](https://circuitpython.org/libraries) Website
2. Download the latest bundle for 9.x
3. Unzip the file
4. Select the libs you need and drop them into the `CIRCUITPY/lib` folder
