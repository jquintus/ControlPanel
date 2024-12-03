import board
import os
import microcontroller

class BoardDetails:
    def __init__(self):
        self.os_version = os.uname().version
        self.machine = os.uname().machine
        self.board_id = board.board_id

        unique_id = microcontroller.cpu.uid
        self.unique_id = ":".join("{:02x}".format(byte) for byte in unique_id)

        #self.cpu_name = microcontroller.cpu.name
        self.cpu_frequency = microcontroller.cpu.frequency

    def get_details(self):
        lines = []
        lines.append(f"CircuitPython Version: {self.os_version}")
        lines.append(f"Machine Info: {self.machine}")
        lines.append(f"Board: {self.board_id}")
        lines.append(f"Microcontroller Unique ID: {self.unique_id}")
        lines.append(f"CPU Frequency (Hz): {self.cpu_frequency}")

        return lines
