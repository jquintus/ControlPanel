import board
from adafruit_seesaw import seesaw, rotaryio, digitalio

class Arcade:
    def __init__(self):
        i2c = board.I2C()  # uses board.SCL and board.SDA
        ss = seesaw.Seesaw(i2c, addr=0x36)

        seesaw_product = (ss.get_version() >> 16) & 0xFFFF
        print("Found product {}".format(seesaw_product))
        if seesaw_product != 4991:
            print("Wrong firmware loaded?  Expected 4991")

        # Configure seesaw pin used to read knob button presses
        # The internal pull up is enabled to prevent floating input
        ss.pin_mode(24, ss.INPUT_PULLUP)
        self.button = digitalio.DigitalIO(ss, 24)

        self.encoder = rotaryio.IncrementalEncoder(ss)

    @property
    def encoder_position(self):
        return self.encoder.position

    @property
    def button_value(self):
        return self.button.value

        