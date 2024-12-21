"""
This module abstracts away the serial communication over USB

You can read and write from this connection
"""
# pyright: reportMissingImports=false
# pylint: disable=import-error

import usb_cdc

class Serial:
    """
    This class abstracts away the serial communication over USB

    You can read and write from this connection
    """
    def __init__(self, logger):
        self.com = usb_cdc.data
        self.com.timeout = 0.1

        self.logger = logger

    def deprecated___try_to_read_usb_cdc(self):
        """
        This method is deprecated. Delete it.
        """
        if self.com.in_waiting > 0:
            received_data = self.com.read(self.com.in_waiting)
            if received_data:
                print("boo")
                print("Received:", received_data)
                # Echo the received data back to the sender
                self.com.write(f"I received:  {received_data}")
                self.logger.write(received_data)

    def read_line(self):
        """
        Read one line of tex from the serial connection.
        """
        return self.com.readline()

    def write(self, msg):
        """
        Write a message to the serial connection.
        """
        self.com.write(msg)

    def writeln(self, msg):
        """
        Write a message terminated with a \r\n to the serial connection.
        """
        self.com.write(f"{msg}\r\n")

    def write_line(self, msg):
        """
        Write a message terminated with a \r\n to the serial connection.
        """
        self.com.write(f"{msg}\r\n")

    def write_lines(self, lines):
        """
        Write a series of lines each terminated with a \r\n to the serial connection.
        
        lines is a list.
        
        We add the \r\n after each entry in the list. We perform this in a single call.
        """
        msg = "\r\n".join(lines) + "\r\n"
        self.write(msg)
