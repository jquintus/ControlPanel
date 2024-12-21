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
    def __init__(self, idx):
        self.idx = idx

    @property
    def value(self):
        """
        Mocks out the button press. The mock button will never be pressed.
        """
        return False

class MockLed:
    """
    A stubbed out LED so we can create an LED Button w/out an LED
    """
    def __init__(self):
        self._value = False

    @property
    def value(self):
        """
        Get the value of the LED
        """
        return self._value

    @value.setter
    def value(self, value):
        """
        Set the value of the LED
        """
        self._value = value

class LedButton:
    """
    This class provides a wrapper for the Button and LED provided by Adafruit.
    This groups them together so that you can do things like lighting up the
    LED on button press easily.

    Ignore the too-few-public-methods error because this is being used as a stub
    """
    def __init__(self, button, led, idx):
        self.button = button
        self.led = led
        self.idx = idx

    @property
    def value(self):
        """
        Whether or not the button is pressed
        """
        value = not self.button.value
        self.led.value = value
        if value:
            print (f"Button {self.idx} pressed")
        return value

class Arcade:
    """
    The Arcade class is the wrapper around the button and knob hardware.
    """
    _LEFT_ENCODER_ADDR = 0x37
    _RIGHT_ENCODER_ADDR = 0x38

    _BUTTONS_1_ADDR = 0x42
    _BUTTONS_2_ADDR = 0x3D
    _BUTTONS_3_ADDR = 0x3C
    _BUTTONS_4_ADDR = 0x3A # Red buttons

    def __init__(self):
        def __load_board():
            try:
                i2c = board.I2C()  # uses board.SCL and board.SDA
                return i2c
            except RuntimeError as e:
                print(e)
                return None

        def __load_encoder(i2c, addr):
            try:
                print(f"Attempting to load encoder from address {hex(addr)}")
                ss = seesaw.Seesaw(i2c, addr)

                seesaw_product = (ss.get_version() >> 16) & 0xFFFF
                if seesaw_product != 4991:
                    print(
                        "Problem loading rotary encoder. Wrong firmware loaded? " +
                        f"Expected 4991; got {seesaw_product}"
                    )

                # Configure seesaw pin used to read knob button presses
                # The internal pull up is enabled to prevent floating input
                ss.pin_mode(24, ss.INPUT_PULLUP)
                encoder_button = digitalio.DigitalIO(ss, 24)

                encoder = rotaryio.IncrementalEncoder(ss)

                button = LedButton(encoder_button, MockLed, 0)
                return (encoder, button)
            except (AttributeError, ValueError, OSError) as e:
                print(f"Could not load encoder {e}")
                encoder = MockEncoder()
                encoder_button = MockButton(0)
                return (encoder, encoder_button)

        i2c = __load_board()
        (self.encoder1, self.encoder1_button) = __load_encoder(i2c, self._LEFT_ENCODER_ADDR)
        (self.encoder2, self.encoder2_button) = __load_encoder(i2c, self._RIGHT_ENCODER_ADDR)
        self.buttons = self.__load_all_buttons(i2c)

    def __load_all_buttons(self, i2c):
        def __load_button_breakout(i2c, addr):
            try:
                print(f"Attempting to button breakout from address {hex(addr)}")
                ss = seesaw.Seesaw(i2c, addr)
                seesaw_product = (ss.get_version() >> 16) & 0xFFFF
                if seesaw_product != 5296:
                    print(
                        "Problem loading button breakout. Wrong firmware loaded? " +
                        f"Expected 5296; got {seesaw_product}"
                    )

                return ss

            except (AttributeError, ValueError) as e:
                print(f"could not load breakout at {hex(addr)}: {e}")
                return None

        def init_button(idx, ss, pin_tuple):
            (button_pin, led_pin) = pin_tuple
            # pylint: disable=no-else-return
            if ss:
                print(f"Initializing LED Button {idx}...")

                # Initialize Button
                button = digitalio.DigitalIO(ss, button_pin)
                button.direction = board_digitalio.Direction.INPUT
                button.pull = board_digitalio.Pull.UP

                # Initialize LED
                led = digitalio.DigitalIO(ss, led_pin)
                return LedButton(button, led, idx)
            else:
                return MockButton(idx)

        ss1 = __load_button_breakout(i2c, self._BUTTONS_1_ADDR)
        ss2 = __load_button_breakout(i2c, self._BUTTONS_2_ADDR)
        ss3 = __load_button_breakout(i2c, self._BUTTONS_3_ADDR)
        ss4 = __load_button_breakout(i2c, self._BUTTONS_4_ADDR)

        pin_tuples = [ (18, 12), (19, 13), (20, 0), (2,  1), ]

        buttons = [
            # Row 1
            init_button( 1, ss4, pin_tuples[3]),
            init_button( 2, ss1, pin_tuples[0]),
            init_button( 3, ss1, pin_tuples[1]),
            init_button( 4, ss1, pin_tuples[2]),
            init_button( 5, ss1, pin_tuples[3]),

            # Row 2
            init_button( 6, ss4, pin_tuples[2]),
            init_button( 7, ss2, pin_tuples[0]),
            init_button( 8, ss2, pin_tuples[1]),
            init_button( 9, ss2, pin_tuples[2]),
            init_button(10, ss2, pin_tuples[3]),

            # Row 3
            init_button(11, ss4, pin_tuples[1]),
            init_button(12, ss3, pin_tuples[0]),
            init_button(13, ss3, pin_tuples[1]),
            init_button(14, ss3, pin_tuples[2]),
            init_button(15, ss3, pin_tuples[3]),
        ]

        return buttons

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
        if idx >= len(self.buttons) or idx < 0:
            print(f"Button {idx} does not exist")
            return False

        return self.buttons[idx].value
