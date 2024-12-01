# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
This test will initialize the display using displayio and draw a solid green
background, a smaller purple rectangle, and some yellow text. All drawing is done
using native displayio modules.

Pinouts are for the 2.4" TFT FeatherWing or Breakout with a Feather M4 or M0.
"""
import board
import terminalio
import displayio
from adafruit_display_text import label
import adafruit_ili9341
import os
import microcontroller
import busio
import usb_cdc
import time
# Support both 8.x.x and 9.x.x. Change when 8.x.x is discontinued as a stable release.
try:
    from fourwire import FourWire
except ImportError:
    from displayio import FourWire

# Release any resources currently in use for the displays
displayio.release_displays()

spi = board.SPI()
tft_cs = board.D9
tft_dc = board.D10

display_bus = FourWire(spi, command=tft_dc, chip_select=tft_cs, reset=board.D6)
display = adafruit_ili9341.ILI9341(display_bus, width=320, height=240)

# Make the display context
splash = displayio.Group()
display.root_group = splash

cursor = 0
def write1(text):
    global cursor
    cursor += 25
    if cursor > 200:
        cursor = 25

    # Draw a label
    #text_group = displayio.Group(scale=2, x=10, y=cursor)
    text_area = label.Label(terminalio.FONT, 
                            text=f"{text:26}", 
                            color=0xFFFFFF,
                            background_color=0x000000)
    text_area.x = 25
    text_area.y = cursor

    # text_group.append(text_area)  # Subgroup for text scaling
    # splash.append(text_group)
    display.root_group = text_area


def write2(text):
    # Set text, font, and color
    color = 0xFF00FF

    # Create the tet label
    padded = f"{text:26}"
    text_area = label.Label(terminalio.FONT, color=color)
    label.anchored_position = (120, 85)
    text_area.anchor_point = (1, 1)
    text_area.scale = 2

    # Set the location
    text_area.x = 10
    text_area.y = 10

    text_area.text = padded

    # Show it
    display.root_group = text_area

lines = []
def write(text):
    if not(isinstance(text, str)):
        return

    print(text)
    lines.append(text);

    if len(lines) > 8:
        lines.pop(0)

    write2('\n'.join(lines))

def clear():
    global lines
    lines = []
    write2('\n'.join(lines))


def write_board_info():
    write(f"CircuitPython Version: {os.uname().version}")
    write(f"Machine Info: {os.uname().machine}")
    write(f"Board: {board.board_id}")

    # Get the unique ID of the microcontroller
    unique_id = microcontroller.cpu.uid
    unique_id_str = ":".join("{:02x}".format(byte) for byte in unique_id)

    # Get the microcontroller name
    #cpu_name = microcontroller.cpu.name

    # Get the frequency of the CPU
    cpu_frequency = microcontroller.cpu.frequency

    # Print board-specific information
    write(f"Microcontroller Unique ID: {unique_id_str}")
    #print("CPU Name:", cpu_name)
    write(f"CPU Frequency (Hz): {cpu_frequency}")

write("Hello World!")
write("")
#write_board_info()
write("Receiving...")
#write_to_file("hello world")


#uart = busio.UART(board.TX, board.RX, baudrate=115200, timeout=0.1)
def try_to_read_data():
    if uart.in_waiting > 0:
        print("reading data...")
        # Read incoming data
        data = uart.read().decode('utf-8').strip()
        if data:
            write(data)

com = usb_cdc.data
com.timeout = 0.1
def try_to_read_usb_cdc():
    if com.in_waiting > 0:
        received_data = com.read(com.in_waiting)
        if received_data:
            print("boo")
            print("Received:", received_data)
            # Echo the received data back to the sender
            com.write(f"I received:  {received_data}")
            write(received_data)

com.write("hello world \r\n")
def try_to_read_usb_cdc_2():
    global current_idx
    line = com.readline()
    if(line):
        line = line.decode('utf-8').strip()
        com.write(f"received: {line}\r\n")
        write(line)
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
            current_idx = show_by_idx(current_idx)
        elif(line == "down"):
            current_idx -= 1
            current_idx = show_by_idx(current_idx)
        else:
            show_bmp(line)

def show_by_idx(idx):
    idx = 0 if idx > max_idx else idx
    idx = max_idx if idx < 0 else idx

    print(f"Showing index {idx}: {bmp_files[idx]}")
    show_bmp(bmp_files[idx])
    return idx

def writeln(msg):
    com.write(f"{msg}\r\n")

def show_heart():
    show_bmp("heart")

def show_bmp(bmp):
    filename = bmp if bmp[-4:] == ".bmp" else f"{bmp}.bmp"
    if filename in bmp_files:
        # Setup the file as the bitmap data source
        bitmap = displayio.OnDiskBitmap(filename)
        # Create a TileGrid to hold the bitmap
        tile_grid = displayio.TileGrid(bitmap, pixel_shader=bitmap.pixel_shader)

        # Create a Group to hold the TileGrid
        group = displayio.Group()

        # Add the TileGrid to the Group
        group.append(tile_grid)

        # Add the Group to the Display
        display.root_group = group

# List to store .bmp files
bmp_files = []

for file in os.listdir('/'):
    if file.endswith('.bmp'):
        bmp_files.append(file)

# show_bmp("world")

current_idx = -1
max_idx = len(bmp_files) - 1

while True:
    try_to_read_usb_cdc_2()
