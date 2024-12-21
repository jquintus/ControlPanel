# Control Panel

## Hardware and Software Dependencies

- Adafruit Feather RP2040
  - [Product Page](https://www.adafruit.com/product/4884)
  - [Learn Page](https://learn.adafruit.com/adafruit-feather-rp2040-pico/overview)
- Adafruit LED Arcade Button 1x4 STEMMA QT
  - [Product Page](https://www.adafruit.com/product/5296)
  - [Learn Page](https://learn.adafruit.com/adafruit-led-arcade-button-qt)
- Rotary Encoder
  - [Product Page](https://www.adafruit.com/product/5880)
  - [Learn Page](https://learn.adafruit.com/adafruit-i2c-qt-rotary-encoder)
- Arcade Buttons
  - [Green](https://www.adafruit.com/product/3487)
  - [Yellow](https://www.adafruit.com/product/3488)
  - [Red](https://www.adafruit.com/product/3489)
  - [Blue](https://www.adafruit.com/product/3490)
- [CircuitPython](https://circuitpython.org/)
  - [CircuitPython v9.11](https://circuitpython.org/board/adafruit_feather_rp2040/)
  - [Adafruit HID Library](https://docs.circuitpython.org/projects/hid/en/latest/)
  - [CircuitPython HID Keyboard and Mouse](https://learn.adafruit.com/adafruit-feather-m0-express-designed-for-circuit-python-circuitpython/circuitpython-hid-keyboard-and-mouse)

## Installing CircuitPython

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

## Cloning this repo directly to your board

By default, git wants to clone repositories to folders, so cloning directly to
the root of a filesystem requires a few extra steps.

```batch
cd e:\
git init
git remote add origin https://github.com/jquintus/ControlPanel
git pull origin main
git branch --set-upstream-to=origin/main main
```

## Update the Circuit Python Bundles

1. Go to the [CircuitPython](https://circuitpython.org/libraries) Website
2. Download the latest bundle for 9.x
3. Unzip the file
4. Select the libs you need and drop them into the `CIRCUITPY/lib` folder

### Rotary Encoder Details

![Rotary Encoder](https://cdn-shop.adafruit.com/970x728/5880-00.jpg)
![Addresses](https://cdn-learn.adafruit.com/assets/assets/000/127/722/large1024/adafruit_products_rotaryEncTable.png?1708019327)

### Arcade Button Breakout Details

![Button Breakout Board](https://cdn-learn.adafruit.com/assets/assets/000/108/466/large1024/adafruit_products_AQT_top.jpg?1643407292)

![Button Breakout Addresses](https://cdn-learn.adafruit.com/assets/assets/000/108/553/large1024/adafruit_products_seesaw_possible_addresses_by_pin_setting_starting_at_0x3A.png?1643747490)
