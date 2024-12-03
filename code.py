import board
import os
import microcontroller
import board
from screen import Screen
from serial import Serial
from arcade import Arcade

screen = Screen()
com = Serial(screen)

arcade = Arcade()
button_held = False
last_position = arcade.encoder_position

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
    line = com.read_line()
    if(line):
        line = line.decode('utf-8').strip()
        com.write(f"received: {line}\r\n")
        screen.write(line)
        line = line.lower()
        if(line == "i love ksenia"):
            show_heart()
        elif(line == "clear"):
            screen.clear()
        elif(line == "list"):
            for file in bmp_files:
                com.writeln(file[:-4])

            com.writeln("heart")
            com.writeln("i love ksenia")
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

bmp_files = [file for file in os.listdir('/') if file.endswith('.bmp')]

show_bmp("world")

max_idx = len(bmp_files)
print(f"Max Index: {max_idx}")

while True:
    try_to_read_usb_cdc_2()
        # negate the position to make clockwise rotation positive
    position = arcade.encoder_position

    if position != last_position:
        last_position = position
        print(f"Current Position {position}")
        show_by_idx(position)

    if not arcade.button_value and not button_held:
        button_held = True
        print("Button pressed")

    if arcade.button_value and button_held:
        button_held = False
        print("Button released")
