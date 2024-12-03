import board
import os
import microcontroller

class BoardDetails:
    def __init__(self):
        pass

    def get_details(self):
        lines = []
        lines.append(f"CircuitPython Version: {os.uname().version}")
        lines.append(f"Machine Info: {os.uname().machine}")
        lines.append(f"Board: {board.board_id}")

        # Get the unique ID of the microcontroller
        unique_id = microcontroller.cpu.uid
        unique_id_str = ":".join("{:02x}".format(byte) for byte in unique_id)

        # Get the microcontroller name
        #cpu_name = microcontroller.cpu.name

        # Get the frequency of the CPU
        cpu_frequency = microcontroller.cpu.frequency

        # Print board-specific information
        lines.append(f"Microcontroller Unique ID: {unique_id_str}")
        #print("CPU Name:", cpu_name)
        lines.append(f"CPU Frequency (Hz): {cpu_frequency}")

        return lines
