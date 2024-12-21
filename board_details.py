"""
Retrieve information about the device so that we can identify different boards.

Author: Josh Quintus
Date: December 2024
"""
# pyright: reportMissingImports=false
# pylint: disable=import-error
# pylint: disable=no-member

import os
import board
import microcontroller

# pylint: disable=too-few-public-methods
class BoardDetails:
    """
    Retrieve information about the device so that we can identify different boards.
    """
    def __init__(self):
        self.os_version = os.uname().version
        self.machine = os.uname().machine
        self.board_id = board.board_id

        unique_id = microcontroller.cpu.uid
        self.unique_id = ":".join(f"{byte:02x}" for byte in unique_id)

        #self.cpu_name = microcontroller.cpu.name
        self.cpu_frequency = microcontroller.cpu.frequency

    def get_details(self):
        """
        Return the details about the board
        """
        lines = []
        lines.append(f"CircuitPython Version: {self.os_version}")
        lines.append(f"Machine Info: {self.machine}")
        lines.append(f"Board: {self.board_id}")
        lines.append(f"Microcontroller Unique ID: {self.unique_id}")
        lines.append(f"CPU Frequency (Hz): {self.cpu_frequency}")

        return lines
