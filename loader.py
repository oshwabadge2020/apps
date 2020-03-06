import os
import board
import digitalio
import gamepad
import time
import terminalio
from displayio import Group
from adafruit_display_text import label
COLOR = 0xFFFFFF
FONT = terminalio.FONT
TOP_OFFSET = 3
MARGIN = 3
MENU_START = 10+TOP_OFFSET+MARGIN
def run_file(filename):
    module_name = filename.strip(".py")
    mod = __import__(module_name)
    mod.main()

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

NEXT = 1 << 0
SELECT = 1 << 1


pad = gamepad.GamePad(
    digitalio.DigitalInOut(board.BUTTON_A),
    digitalio.DigitalInOut(board.BUTTON_B)
)

cursor_index = 0

PROGRAMS_DIR = "/sketches"
while True:
    files_available = os.listdir(PROGRAMS_DIR)
    program_count = len(files_available)
    print("avial:", files_available)
    buttons = pad.get_pressed()
    if buttons & NEXT:
        cursor_index += 1
        if cursor_index >= program_count:
            cursor_index = 0
    elif buttons & SELECT:
        print("trying to run ", files_available[cursor_index])
        run_file(files_available[cursor_index])
    while buttons:
        # Wait for all buttons to be released.
        buttons = pad.get_pressed()
    print_list(board.DISPLAY, files_available, cursor_index)
