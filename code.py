"""
This is the entry point to the code.

Author: Josh Quintus
Date: December 2024
"""

# import i2c_scanner #only uncomment this when you need to scan for connected devices.

import os
from screen import Screen
from serial import Serial
from arcade import Arcade
from board_details import BoardDetails

bd = BoardDetails()
screen = Screen()
com = Serial(screen)

arcade = Arcade()
button_held = False # pylint: disable=invalid-name
last1_position = arcade.encoder1_position
last2_position = arcade.encoder2_position

screen.write("Hello World!")
screen.write("")

com.write("hello world ;) \r\n")
com.write_lines(bd.get_details())
screen.write("Receiving...")


def try_to_read_usb_cdc():
    """
    Read commands from the serial CDC connection
    """
    line = com.read_line()
    if line:
        line = line.decode('utf-8').strip()
        com.write(f"received: {line}\r\n")
        screen.write(line)
        line = line.lower()
        if line == "i love ksenia":
            show_bmp("heart")
        elif line == "clear":
            screen.clear()
        elif line == "list":
            for file in bmp_files:
                com.writeln(file[:-4])

            com.writeln("heart")
            com.writeln("i love ksenia")
        else:
            show_bmp(line)

def show_by_idx(idx):
    """
    Display the pre-loaded bitmap at the given index.
    If the index is out of bounds we handle normalizing it for you.
    """
    idx = idx % bmp_max_idx

    print(f"Showing image index {idx}: {bmp_files[idx]}")
    show_bmp(bmp_files[idx])

def show_bmp(bmp):
    """
    Display the named bitmap file from the /img directory.

    If you forget to include the `.bmp` extension, it is added for you.
    """
    filename = bmp if bmp[-4:] == ".bmp" else f"{bmp}.bmp"
    if filename in bmp_files:
        screen.show_bmp('/img/' + filename)

bmp_files = [file for file in os.listdir('/img') if file.endswith('.bmp')]

show_bmp("world")

bmp_max_idx = len(bmp_files)
print(f"Max BMP Index: {bmp_max_idx}")

while True:
    try_to_read_usb_cdc()
    # negate the position to make clockwise rotation positive
    position1 = arcade.encoder1_position
    position2 = arcade.encoder2_position

    if position1 != last1_position:
        last1_position = position1
        print(f"Current Position {position1}")
        show_by_idx(position1)

    if position2 != last2_position:
        last2_position = position2
        print(f"Current Position {position2}")
        show_by_idx(position2)

    if not arcade.encoder1_pressed and not button_held:
        button_held = True # pylint: disable=invalid-name
        print("Button pressed")

    if arcade.encoder1_pressed and button_held:
        button_held = False # pylint: disable=invalid-name
        print("Button released")

    for i in range(15):
        if arcade.get_button_value(i):
            #show_by_idx(i)
            pass
