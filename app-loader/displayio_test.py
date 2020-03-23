import board
import displayio
import terminalio
from adafruit_display_text import label
from time import sleep
def main():
    display = board.DISPLAY

    # Set text, font, and color
    text = "HELLO WORLD"
    font = terminalio.FONT
    color = 0x0000FF

    # Create the test label
    text_area = label.Label(font, text=text, color=color, scale=3)

    # Set the location
    text_area.x = 40
    text_area.y = 40

    # Show it
    display.show(text_area)
    sleep(5)


