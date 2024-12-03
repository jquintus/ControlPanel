
"""
This test will initialize the display using displayio and draw a solid green
background, a smaller purple rectangle, and some yellow text. All drawing is done
using native displayio modules.

Pinouts are for the 2.4" TFT FeatherWing or Breakout with a Feather M4 or M0.
"""
import board
import os
import microcontroller
import board
from adafruit_seesaw import seesaw, rotaryio, digitalio
from screen import Screen
from serial import Serial

screen = Screen()
com = Serial(screen)

def write_board_info():
    screen.write(f"CircuitPython Version: {os.uname().version}")
    screen.write(f"Machine Info: {os.uname().machine}")
    screen.write(f"Board: {board.board_id}")

    # Get the unique ID of the microcontroller
    unique_id = microcontroller.cpu.uid
    unique_id_str = ":".join("{:02x}".format(byte) for byte in unique_id)

    # Get the microcontroller name
    #cpu_name = microcontroller.cpu.name

    # Get the frequency of the CPU
    cpu_frequency = microcontroller.cpu.frequency

    # Print board-specific information
    screen.write(f"Microcontroller Unique ID: {unique_id_str}")
    #print("CPU Name:", cpu_name)
    screen.write(f"CPU Frequency (Hz): {cpu_frequency}")

screen.write("Hello World!")
screen.write("")
#write_board_info()
screen.write("Receiving...")

com.write("hello world ;) \r\n")

def try_to_read_usb_cdc_2():
    global current_idx
    line = com.readline()
    if(line):
        line = line.decode('utf-8').strip()
        com.write(f"received: {line}\r\n")
        screen.write(line)
        line = line.lower()
        if(line == "i love ksenia"):
            show_heart()
        elif(line == "clear"):
            clear()
        elif(line == "list"):
            for file in bmp_files:
                writeln(file[:-4])

            writeln("heart")
            writeln("i love ksenia")
        elif(line == "up"):
            current_idx += 1
            show_by_idx(current_idx)
        elif(line == "down"):
            current_idx -= 1
            show_by_idx(current_idx)
        else:
            show_bmp(line)

def show_by_idx(idx):
    idx = idx % max_idx

    print(f"Showing index {idx}: {bmp_files[idx]}")
    show_bmp(bmp_files[idx])

def show_heart():
    show_bmp("heart")

def show_bmp(bmp):
    filename = bmp if bmp[-4:] == ".bmp" else f"{bmp}.bmp"
    if filename in bmp_files:
        screen.show_bmp(filename)

# List to store .bmp files
bmp_files = []

for file in os.listdir('/'):
    if file.endswith('.bmp'):
        bmp_files.append(file)

show_bmp("world")

# max_idx = len(bmp_files)
# print(f"Max Index: {max_idx}")

# i2c = board.I2C()  # uses board.SCL and board.SDA
# seesaw = seesaw.Seesaw(i2c, addr=0x36)

# seesaw_product = (seesaw.get_version() >> 16) & 0xFFFF
# print("Found product {}".format(seesaw_product))
# if seesaw_product != 4991:
#     print("Wrong firmware loaded?  Expected 4991")

# # Configure seesaw pin used to read knob button presses
# # The internal pull up is enabled to prevent floating input
# seesaw.pin_mode(24, seesaw.INPUT_PULLUP)
# button = digitalio.DigitalIO(seesaw, 24)

# button_held = False

# encoder = rotaryio.IncrementalEncoder(seesaw)
# last_position = encoder.position

# while True:
#     try_to_read_usb_cdc_2()
#         # negate the position to make clockwise rotation positive
#     position = encoder.position

#     if position != last_position:
#         last_position = position
#         print(f"Current Position {position}")
#         show_by_idx(position)

#     if not button.value and not button_held:
#         button_held = True
#         print("Button pressed")

#     if button.value and button_held:
#         button_held = False
#         print("Button released")

while True:
    pass