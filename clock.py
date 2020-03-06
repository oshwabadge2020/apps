import board
import displayio
import terminalio
from adafruit_display_text import label
import time
import rtc
from adafruit_bitmap_font import bitmap_font

#               Year, Month, doM    Hour, Mins, Secs, doY, isDST?
CURRENT_TIME = (2020, 3, 6, 8, 53, 9, 3, -1, 0)
clock = rtc.RTC()
clock.datetime = CURRENT_TIME
BLUE = 0x0000FF
RED = 0xFF0000
R2 = 0xFF8888
BLUE = 0x00FF00
PURPLE = 0xFF00FF
Y_OFFSET = 120
# kourier = bitmap_font.load_font("/kourier.bdf")
helv = bitmap_font.load_font("/Helvetica-Bold-16.bdf")
def main():
    display = board.DISPLAY

    font = terminalio.FONT

    #struct_time(tm_year=2000, tm_mon=1, tm_mday=1, tm_hour=0, tm_min=6, tm_sec=30, tm_wday=5, tm_yday=1, tm_isdst=-1)
    for i in range(0, 20):
        #normally we'll do this as close to display as possible, add offset if needed
        current_time = time.localtime()

        # Create the test label
        hours = label.Label(helv, text=str(current_time.tm_hour)+":", color=RED, scale=4)
        minutes = label.Label(helv, text=str(current_time.tm_min)+":", color=RED, scale=4)
        seconds = label.Label(helv, text=str(current_time.tm_sec), color=RED, scale=4)
        t_group = displayio.Group()

        # TODO: # fix spacing for double digits
        # Set the location
        hours.x = 5
        hours.y = Y_OFFSET
        minutes.x = hours.x+70
        minutes.y = Y_OFFSET
        seconds.x = minutes.x+90
        seconds.y = Y_OFFSET
        t_group.append(hours)
        t_group.append(minutes)
        t_group.append(seconds)
        # Show it
        display.show(t_group)
        time.sleep(1)


