import time
import terminalio
import displayio
import board
from adafruit_display_text import label

Y_OFFSET=100
X_INDENT=10
def main():
  display = board.DISPLAY
  i2c = board.I2C()
  
  
  display = board.DISPLAY
  font = terminalio.FONT
  t_group = displayio.Group()
  while True:
      while not i2c.try_lock():
          time.sleep(0.010)
      while len(t_group) > 0:
          t_group.pop()
      things = i2c.scan()
  
      if len(things) == 0:
          print("No I2C Devices responded to scan")
          # Create the test label
          not_found = label.Label(terminalio.FONT, text="No I2C Devices \nresponded to scan", color=0xFFFFFF, scale=2)
          not_found.x = X_INDENT
          not_found.y = Y_OFFSET+80
          t_group.append(not_found)
  
      else:
          found_str = ""
          for index, thing in enumerate(things):
              found_str +="Found %d (%s)\n"%(thing, hex(thing))
          found = label.Label(terminalio.FONT, text=found_str, color=0xFFFFFF, scale=2)
          found.x = X_INDENT
          found.y = Y_OFFSET+20
          t_group.append(found)
          print(found_str)
      i2c.unlock()
      display.show(t_group)
  
      print("*************** Done! *************")
  
      time.sleep(1)
  
