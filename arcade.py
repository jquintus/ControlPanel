"""
This encapsulates all of the code and logic for the buttons, switches, and rotary encoders

Author: Josh Quintus
Date: December 2024
"""
import board
import digitalio as board_digitalio
from adafruit_seesaw import seesaw, rotaryio, digitalio


# pylint: disable=too-few-public-methods
class MockEncoder:
    """
    This class provides a stub for the Rotary Encoder provided by Adafruit.
    This lets you test code w/out having everything wired correctly.

    Ignore the too-few-public-methods error because this is being used as a stub
    """
    def __init__(self):
        pass

    @property
    def position(self):
        """
        Mocks out the position of the encoder. It will always be 0 for a mock.
        """
        return 0

class MockButton:
    """
    This class provides a stub for the Button provided by Adafruit.
    This lets you test code w/out having everything wired correctly.

    Ignore the too-few-public-methods error because this is being used as a stub
    """
    def __init__(self):
        pass

    @property
    def value(self):
        """
        Mocks out the button press. The mock button will never be pressed.
        """
        return False

class LedButton:
    """
    This class provides a wrapper for the Button and LED provided by Adafruit.
    This groups them together so that you can do things like lighting up the
    LED on button press easily.

    Ignore the too-few-public-methods error because this is being used as a stub
    """
    def __init__(self, button, led):
        self.button = button
        self.led = led

    @property
    def value(self):
        """
        Whether or not the button is pressed
        """
        return not self.button.value

class Arcade:
    """
    The Arcade class is the wrapper around the button and knob hardware.
    """
    def __init__(self):
        i2c = self.__load_board()
        (self.encoder1, self.encoder1_button) = self.__load_encoder(i2c, 0x37)
        (self.encoder2, self.encoder2_button) = self.__load_encoder(i2c, 0x38)
        self.buttons = self.__load_buttons(i2c, addr=0x3A)

    def __load_board(self):
        try:
            i2c = board.I2C()  # uses board.SCL and board.SDA
            return i2c
        except RuntimeError as e:
            print(e)
            return None

    def __load_buttons(self, i2c, addr):
        def init_button(idx, arcade_qt, button_pin, led_pin):
            print(f"Initializing button {idx}...")
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

        except (AttributeError, ValueError) as e:
            print(f"could not load buttons: {e}")
            return [
                MockButton(),
                MockButton(),
                MockButton(),
                MockButton(),
            ]


    def __load_encoder(self, i2c, addr):
        try:
            print(f"Attempting to load encoder from address {hex(addr)}")
            ss = seesaw.Seesaw(i2c, addr)

            seesaw_product = (ss.get_version() >> 16) & 0xFFFF
            print(f"Found product {seesaw_product}")
            if seesaw_product != 4991:
                print("Wrong firmware loaded?  Expected 4991")

            # Configure seesaw pin used to read knob button presses
            # The internal pull up is enabled to prevent floating input
            ss.pin_mode(24, ss.INPUT_PULLUP)
            encoder_button = digitalio.DigitalIO(ss, 24)

            encoder = rotaryio.IncrementalEncoder(ss)

            return (encoder, encoder_button)
        except (AttributeError, ValueError) as e:
            print(f"Could not load encoder {e}")

            encoder = MockEncoder()
            encoder_button = MockButton()
            return (encoder, encoder_button)

    @property
    def encoder1_position(self):
        """The position of the first rotary encoder"""
        return self.encoder1.position

    @property
    def encoder1_pressed(self):
        """Whether or not the first rotary encoder is being pressed like a button"""
        return self.encoder1_button.value

    @property
    def encoder2_position(self):
        """The position of the second rotary encoder"""
        return self.encoder2.position

    @property
    def encoder2_pressed(self):
        """Whether or not the second rotary encoder is being pressed like a button"""
        return self.encoder2_button.value

    def get_button_value(self, idx):
        """
        Returns whether or not the specified button is being pressed.
        If an ID is passed in that is out of bounds, then return false.
        It can't be pressed if it doesn't exist.

        This behavior allows for easier testing of the code w/out having
        to have all of the hardware attached.
        """
        if idx > 3 or idx < 0:
            return False

        return self.buttons[idx].value
