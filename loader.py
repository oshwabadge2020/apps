import os
import board
import digitalio
import gamepad
import time
import terminalio
from displayio import Group
from adafruit_display_text import label







board.DISPLAY.brightness = 0.0



import board
import displayio

display = board.DISPLAY

# Open the file
bg = open("frame.bmp", "rb")
bg_bitmap = displayio.OnDiskBitmap(bg)

tile_grid = displayio.TileGrid(bg_bitmap, pixel_shader=displayio.ColorConverter())



COLOR = 0xFFFFFF
FONT = terminalio.FONT
TOP_OFFSET = 3
MARGIN = 3

APP_DIR = "/apps"
MENU_START = 10+TOP_OFFSET+MARGIN


pad = gamepad.GamePad(
    digitalio.DigitalInOut(board.BUTTON_SW1),
    digitalio.DigitalInOut(board.BUTTON_SW2),
    digitalio.DigitalInOut(board.BUTTON_SW3),
    digitalio.DigitalInOut(board.BUTTON_SW4)
)
def run_file(filename):
    module_name = APP_DIR+"/"+filename.strip(".py")
    print("mod name:", module_name)
    mod = __import__(module_name)
    print("mod dir:", dir(mod))
    mod.main()
    board.DISPLAY.show(None)

    print("program finished. Continue?")
    ok = False
    while not ok:

        buttons = pad.get_pressed()
        if  buttons & NEXT:
            break

def check_for_apps(appdir=APP_DIR):
    return os.listdir(appdir)

def print_list(display, programs, cur_index):
    program_menu = Group(max_size=10, scale=2)
    loader_banner = label.Label(FONT, text="Choose to Run", color=COLOR)
    loader_banner.x = 10
    loader_banner.y = TOP_OFFSET
    program_menu.append(loader_banner)
    for list_index, program_name in enumerate(programs):
        if cur_index  == list_index:
            menu_item_str = ">> %s"%'{:>5}'.format(program_name)
        else:
            menu_item_str = ">  %s"%'{:>5}'.format(program_name)

        menu_item = label.Label(FONT, text=menu_item_str, color=COLOR)
        menu_item.x = 10
        menu_item.y = MENU_START+(list_index*10)
        program_menu.append(menu_item)

    display.show(program_menu)

SELECT = 1 << 0
NEXT = 1 << 1
PREV = 1 << 2
#
#           MICRO USB
#     BUTTON_SW3  BUTTON_SW4
#     _____________________
#     |                    |
#     |                    |
#     |                    |
#     |                    |
#     |                    |
#     |                    |
#     |____________________|
#     BUTTON_SW2, BUTTON_SW1
#

# Create a Group to hold the TileGrid
group = displayio.Group()

group.append(tile_grid)
cursor_index = 0
display.show(group)
prev_file_count = 0

while True:
    files_available = check_for_apps()
    file_count = len(files_available)
    if file_count != prev_file_count:
        prev_file_count = file_count
        print("avial:", files_available)

    buttons = pad.get_pressed()
    if buttons & NEXT:
        cursor_index += 1
        if cursor_index >= file_count:
            cursor_index = 0
    if buttons & PREV:
        cursor_index -= 1
        if cursor_index < 0:
            cursor_index = file_count -1
    elif buttons & SELECT:
        print("trying to run ", files_available[cursor_index])
        run_file(files_available[cursor_index])
    while buttons:
        # Wait for all buttons to be released.
        buttons = pad.get_pressed()
    print_list(board.DISPLAY, files_available, cursor_index)
