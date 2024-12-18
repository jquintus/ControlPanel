import board
import digitalio as board_digitalio
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

class LedButton:
    def __init__(self, button, led):
        self.button = button
        self.led = led
        pass

    @property 
    def value(self):
        return not self.button.value

class Arcade:
    def __init__(self):
        i2c = board.I2C()  # uses board.SCL and board.SDA
        (self.encoder, self.encoder_button) = self.__load_encoder(i2c, 0x36)
        self.buttons = self.__load_buttons(i2c, addr=0x3A)

    def __load_buttons(self, i2c, addr):
        def init_button(id, arcade_qt, button_pin, led_pin):
            print("Initializing button...")
            button = digitalio.DigitalIO(arcade_qt, button_pin)
            button.direction = board_digitalio.Direction.INPUT
            button.pull = board_digitalio.Pull.UP

            print("Initializing led...")
            led = digitalio.DigitalIO(arcade_qt, led_pin)
            return LedButton(button, led)

        try:
            ss = seesaw.Seesaw(i2c, addr)
            
            b1 = init_button(1, ss, button_pin=2,  led_pin=1)
            b2 = init_button(2, ss, button_pin=20, led_pin=0)
            b3 = init_button(3, ss, button_pin=19, led_pin=13)
            b4 = init_button(4, ss, button_pin=18, led_pin=12)
            
            return [
                b1,
                b2,
                b3,
                b4,
            ]

        except:
            print("could not load buttons")
            return [
                MockButton(),
                MockButton(),
                MockButton(),
                MockButton(),
            ]
        
        
    def __load_encoder(self, i2c, addr):
        try:
            ss = seesaw.Seesaw(i2c, addr)

            seesaw_product = (ss.get_version() >> 16) & 0xFFFF
            print("Found product {}".format(seesaw_product))
            if seesaw_product != 4991:
                print("Wrong firmware loaded?  Expected 4991")

            # Configure seesaw pin used to read knob button presses
            # The internal pull up is enabled to prevent floating input
            ss.pin_mode(24, ss.INPUT_PULLUP)
            encoder_button = digitalio.DigitalIO(ss, 24)

            encoder = rotaryio.IncrementalEncoder(ss)
            
            return (encoder, encoder_button)
        except:
            print("Could not load encoder")

            encoder = MockEncoder()
            encoder_button = MockButton()
            return (encoder, encoder_button)


    @property
    def encoder_position(self):
        return self.encoder.position

    @property
    def encoder_pressed(self):
        return self.encoder_button.value

    def get_button_value(self, idx):
        if (idx > 3): return False
        
        return self.buttons[idx].value