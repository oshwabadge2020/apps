import os
import board
import digitalio
import gamepad
import adafruit_imageload
import time
from time import sleep
import terminalio
from adafruit_display_text import label
import displayio
import json

# TODO:
"""
# auto dim/shut off screen by looking for significant motion via accel
# battery gauge
"""
default_app = None
# load rotation config; hardcoded for now
board.DISPLAY.rotation = 0

###
SELECT = 1 << 0
NEXT = 1 << 1
PREV = 1 << 2
COLOR = 0xFFFFFF
TOP_OFFSET = 3
MARGIN = 3
# "/apps" = "/apps"
MENU_START = 10+TOP_OFFSET+MARGIN

apps_list = os.listdir("/apps")
root_files = os.listdir("/")
if "config.json" in root_files:
    with open("/config.json", "r") as f:
        config = json.load(f)
        if "rotation" in config:
            board.DISPLAY.rotation = config['rotation']
        if "default_app" in config:
            default_app = config['default_app']
        if "splash_filename" in config:
            
            splash_filename = config['splash_filename']
class Loader:
    def __init__(self):
        self.buttons = []

        self.display = board.DISPLAY
        self.display.brightness = 1.0
        self.cursor_index = 0

        self.files_available = self.check_for_apps()
        self.file_count = len(self.files_available)
        self.loader_initialized = False

    def _initialize(self):
        self.init_cursor()
        self.init_buttons()
        self.init_menu()
        self.display.show(self.program_menu)
        self.loader_initialized = True

    def init_cursor(self):
        self.cursor_group = displayio.Group()
        cursor_bmp, cursor_pal = adafruit_imageload.load(
            "/apps/loader/8px_cursors.bmp",
            bitmap=displayio.Bitmap,
            palette=displayio.Palette
        )
        self.cursor = displayio.TileGrid(
            cursor_bmp,
            pixel_shader=cursor_pal,
            width=1,
            height=1,
            tile_width=8,
            tile_height=8
        )
        self.cursor[0] = 0
        self.cursor.x = 0
        self.cursor.y = MENU_START+(self.cursor_index*8)

    def init_menu(self):
        self.program_menu = displayio.Group(max_size=10, scale=2)
        loader_banner = label.Label(terminalio.FONT, text="Choose to Run", color=COLOR)
        loader_banner.x = 10
        loader_banner.y = TOP_OFFSET
        self.program_menu.append(loader_banner)

        for list_index, program_name in enumerate(self.files_available):
            menu_item_str = "%s"%'{:>5}'.format(program_name)

            menu_item = label.Label(terminalio.FONT, text=menu_item_str, color=COLOR)
            menu_item.x = 10
            menu_item.y = MENU_START+(list_index*10)
            self.program_menu.append(menu_item)


        self.program_menu.append(self.cursor)

    def init_buttons(self):
        for butt in [board.BUTTON_SW1 ,board.BUTTON_SW2 ,board.BUTTON_SW3 ,board.BUTTON_SW4]:
            self.buttons.append(digitalio.DigitalInOut(butt))
        self.pad = gamepad.GamePad(*self.buttons)


    def release_buttons(self):
       for button in self.buttons:
           button.deinit()

    def run_file(self, filename):
        module_name = "/apps"+"/"+filename.strip(".py")
        mod = __import__(module_name)
        # self.release_buttons()
        mod.main()
        self.display.show(None)
        self.init_buttons()
        ok = False
        while not ok:
            buttons = self.pad.get_pressed()
            if  buttons & NEXT:
                break

    def check_for_apps(self, appdir="/apps"):
        file_list = []
        try:
            file_list = os.listdir(appdir)
        except:
            os.mkdir(appdir)

        return file_list

    def run(self, file=None):
        if file:
            self.run_file(file)
        if not self.loader_initialized:
            self._initialize()
        last_update = time.monotonic()
        i = 0
        current_time = time.monotonic()
        while True:
            current_time = time.monotonic()
            if current_time - last_update > 0.2:
                last_update = current_time
                i +=1
                self.cursor[0] = i%3

            self.cursor.y = MENU_START+(self.cursor_index*10)-2

            buttons = self.pad.get_pressed()
            if buttons & NEXT:
                self.cursor_index += 1
                if self.cursor_index >= self.file_count:
                    self.cursor_index = 0
            if buttons & PREV:
                self.cursor_index -= 1
                if self.cursor_index < 0:
                    self.cursor_index = self.file_count -1
            elif buttons & SELECT:
                self.run_file(self.files_available[self.cursor_index])
            while buttons:
                # Wait for all buttons to be released.
                buttons = self.pad.get_pressed()


if __name__ == "__main__":

    display = board.DISPLAY
    # Open the file
    # if splash_filename in root_files:
    #     splash_bmp, splash_pal = adafruit_imageload.load(splash_filename, bitmap=displayio.Bitmap, palette=displayio.Palette)

    #     # Create a Group to hold the TileGrid
    #     splash_group = displayio.Group()
    #     splash = displayio.TileGrid(splash_bmp, pixel_shader=splash_pal)
    #     splash_group.append(splash)
    #     splash_group.scale = 1
    #     display.show(splash_group)
    #     sleep(0.5)
    #     del(splash_bmp)
    #     del(splash_pal)


    loader = Loader()
    if default_app and default_app in  os.listdir("/apps/"):
        loader.run(default_app)
    loader.run()
