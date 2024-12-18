import board
from adafruit_seesaw import seesaw, rotaryio, digitalio

class MockEncoder:
    def __init__(self):
       pass 

    @property
    def position(self):
        return 0
    
class MockButton:
    def __init__(self):
        pass

    @property
    def value(self):
        return False
    
class Arcade:
    def __init__(self):
        self.encoder = None
        self.encoder_button = None
        try:
            i2c = board.I2C()  # uses board.SCL and board.SDA
            ss = seesaw.Seesaw(i2c, addr=0x36)

            seesaw_product = (ss.get_version() >> 16) & 0xFFFF
            print("Found product {}".format(seesaw_product))
            if seesaw_product != 4991:
                print("Wrong firmware loaded?  Expected 4991")

            # Configure seesaw pin used to read knob button presses
            # The internal pull up is enabled to prevent floating input
            ss.pin_mode(24, ss.INPUT_PULLUP)
            self.encoder_button = digitalio.DigitalIO(ss, 24)

            self.encoder = rotaryio.IncrementalEncoder(ss)
        except:
            print("Could not load some or all of the peripherals")
            if (self.encoder is None): 
                self.encoder = MockEncoder()
                self.encoder_button = MockButton()

    @property
    def encoder_position(self):
        return self.encoder.position

    @property
    def encoder_pressed(self):
        return self.encoder_button.value
