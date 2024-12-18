import board
import terminalio
import adafruit_ili9341
import displayio
from adafruit_display_text import label
from fourwire import FourWire

class Screen:

    def __init__(self):
        # Release any resources currently in use for the displays
        displayio.release_displays()

        spi = board.SPI()
        tft_cs = board.D9
        tft_dc = board.D10

        display_bus = FourWire(spi, command=tft_dc, chip_select=tft_cs, reset=board.D6)
        self.display = adafruit_ili9341.ILI9341(display_bus, width=320, height=240)

        # Make the display context
        splash = displayio.Group()
        self.display.root_group = splash

        self.cursor = 0
        self.lines = []

    def write(self, text):
        if not(isinstance(text, str)):
            return

        print(text)
        self.lines.append(text);

        if len(self.lines) > 8:
            self.lines.pop(0)

        self.write2('\n'.join(self.lines))

    def clear(self):
        lines = []
        self.write2('\n'.join(lines))


    def write1(self, text):
        self.cursor += 25
        if self.cursor > 200:
            self.cursor = 25

        # Draw a label
        #text_group = displayio.Group(scale=2, x=10, y=cursor)
        text_area = label.Label(terminalio.FONT, 
                                text=f"{text:26}", 
                                color=0xFFFFFF,
                                background_color=0x000000)
        text_area.x = 25
        text_area.y = self.cursor

        # text_group.append(text_area)  # Subgroup for text scaling
        # splash.append(text_group)
        self.display.root_group = text_area


    def write2(self, text):
        # Set text, font, and color
        color = 0xFF00FF

        # Create the tet label
        padded = f"{text:26}"
        text_area = label.Label(terminalio.FONT, color=color)
        label.anchored_position = (120, 85)
        text_area.anchor_point = (1, 1)
        text_area.scale = 2

        # Set the location
        text_area.x = 10
        text_area.y = 10

        text_area.text = padded

        # Show it
        self.display.root_group = text_area

    def show_bmp(self, filename):
        # Setup the file as the bitmap data source
        bitmap = displayio.OnDiskBitmap(filename)
        # Create a TileGrid to hold the bitmap
        tile_grid = displayio.TileGrid(bitmap, pixel_shader=bitmap.pixel_shader)

        # Create a Group to hold the TileGrid
        group = displayio.Group()

        # Add the TileGrid to the Group
        group.append(tile_grid)

        # Add the Group to the Display
        self.display.root_group = group