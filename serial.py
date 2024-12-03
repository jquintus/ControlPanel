import usb_cdc

class Serial:
    def __init__(self, logger):
        self.com = usb_cdc.data
        self.com.timeout = 0.1
        
        self.logger = logger

    def deprecated___try_to_read_usb_cdc(self):
        if self.com.in_waiting > 0:
            received_data = self.com.read(self.com.in_waiting)
            if received_data:
                print("boo")
                print("Received:", received_data)
                # Echo the received data back to the sender
                self.com.write(f"I received:  {received_data}")
                self.logger.write(received_data)
    
    def read_line(self):
        return self.com.readline()

    def write(self, msg):
        self.com.write(msg)

    def writeln(self, msg):
        self.com.write(f"{msg}\r\n")

    def write_line(self, msg):
        self.com.write(f"{msg}\r\n")

    def write_lines(self, lines):
        msg = "\r\n".join(lines) + "\r\n"
        self.write(msg)

