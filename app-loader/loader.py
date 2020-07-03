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

# TODO:
"""
# default app to run; override by holding buttons
# set screen and button rotation
# auto dim/shut off screen by looking for significant motion via accel
# battery gauge






###
SELECT = 1 << 0
NEXT = 1 << 1
PREV = 1 << 2
COLOR = 0xFFFFFF
FONT = terminalio.FONT
TOP_OFFSET = 3
MARGIN = 3
APP_DIR = "/apps"
MENU_START = 10+TOP_OFFSET+MARGIN
FRAME_FILENAME = "/apps/loader/frame2.bmp"
SPLASH_FILENAME = "/apps/loader/10yrs_240.bmp"
CURSOR_FILENAME = "/apps/loader/8px_cursors.bmp"
# load rotation config; hardcoded for now
board.DISPLAY.rotation = 90
class Loader:
    def __init__(self):
        self.sw1 = None
        self.sw2 = None
        self.sw3 = None
        self.sw4 = None

        self.display = board.DISPLAY
        self.display.brightness = 1.0
        self.cursor_index = 0
        self.init_cursor()

        self.files_available = self.check_for_apps()
        self.file_count = len(self.files_available)

        self.init_buttons()
        self.init_menu()

        self.display.show(self.program_menu)

    def init_cursor(self):
        self.cursor_group = displayio.Group()
        cursor_bmp, cursor_pal = adafruit_imageload.load(
            CURSOR_FILENAME,
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
        frame_bmp, frame_pal = adafruit_imageload.load(FRAME_FILENAME, bitmap=displayio.Bitmap, palette=displayio.Palette)
        print("Frame palette", frame_pal[0])
        print("Frame palette", frame_pal[1])
        frame_pal.make_transparent(0)
        frame_pal[1] = 0xffffff
        frame_pal[0] = 0x0
        frame_pal.make_transparent(1)
        self.program_menu = displayio.Group(max_size=10, scale=2)
        loader_banner = label.Label(FONT, text="Choose to Run", color=COLOR)
        loader_banner.x = 10
        loader_banner.y = TOP_OFFSET
        self.program_menu.append(loader_banner)
        frame = displayio.TileGrid(frame_bmp, pixel_shader=frame_pal)

        for list_index, program_name in enumerate(self.files_available):
            menu_item_str = "%s"%'{:>5}'.format(program_name)

            menu_item = label.Label(FONT, text=menu_item_str, color=COLOR)
            menu_item.x = 10
            menu_item.y = MENU_START+(list_index*10)
            self.program_menu.append(menu_item)


        self.program_menu.append(self.cursor)

        self.program_menu.append(frame)
    def init_buttons(self):
        self.sw1 = digitalio.DigitalInOut(board.BUTTON_SW1)
        self.sw2 = digitalio.DigitalInOut(board.BUTTON_SW2)
        self.sw3 = digitalio.DigitalInOut(board.BUTTON_SW3)
        self.sw4 = digitalio.DigitalInOut(board.BUTTON_SW4)
        self.pad = gamepad.GamePad(self.sw1, self.sw2, self.sw3, self.sw4)


    def release_buttons(self):
        self.sw1.deinit()
        self.sw2.deinit()
        self.sw3.deinit()
        self.sw4.deinit()

    def run_file(self, filename):
        module_name = APP_DIR+"/"+filename.strip(".py")
        mod = __import__(module_name)
        self.release_buttons()
        mod.main()
        self.display.show(None)
        self.init_buttons()
        ok = False
        while not ok:
            buttons = self.pad.get_pressed()
            if  buttons & NEXT:
                break

    def check_for_apps(self, appdir=APP_DIR):
        file_list = []
        try:
            file_list = os.listdir(appdir)
        except:
            os.mkdir(appdir)

        return file_list

    def run(self):
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
    splash_bmp, splash_pal = adafruit_imageload.load(SPLASH_FILENAME, bitmap=displayio.Bitmap, palette=displayio.Palette)

    # Create a Group to hold the TileGrid
    splash_group = displayio.Group()
    splash = displayio.TileGrid(splash_bmp, pixel_shader=splash_pal)
    splash_group.append(splash)
    splash_group.scale = 1
    display.show(splash_group)
    sleep(0.5)
    del(splash_bmp)
    del(splash_pal)


    loader = Loader()
    loader.run()
