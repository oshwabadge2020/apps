import displayio
import adafruit_miniqr
import board
import pulseio
import busio
import microcontroller as m
import time
from analogio import AnalogIn
import array

from digitalio import DigitalInOut, Direction, Pull
#backlight = DigitalInOut(board.TFT_BACKLIGHT)
#backlight.direction = Direction.OUTPUT
#backlight.value = False

pwm = pulseio.PWMOut(board.TFT_BACKLIGHT)
pwm.duty_cycle = 0#65535-16000

display = board.DISPLAY

def bitmap_qr(matrix):
	"""The QR code bitmap."""
	border_pixels = 2
	bitmap = displayio.Bitmap(matrix.width + 2 * border_pixels,matrix.height + 2 * border_pixels, 2)
	for y in range(matrix.height):
		for x in range(matrix.width):
			if matrix[x, y]:
				bitmap[x + border_pixels, y + border_pixels] = 1
			else:
				bitmap[x + border_pixels, y + border_pixels] = 0
	return bitmap

print('Hello World!')

print('Scanning for I2C Devices..')
i2c = busio.I2C(board.SCL, board.SDA)
i2c.try_lock()
addrs = [hex(x) for x in i2c.scan()]
print(addrs)
# ['0x1e', '0x39', '0x6b', '0x76']

if len(addrs)==4:
	if '0x1e' in addrs:
		if '0x39' in addrs:
			if '0x6b' in addrs:
				if '0x76' in addrs:
					print("All devices present!") 


print('Checking Charge Status Pin')
charge_status = DigitalInOut(m.pin.P0_16)
charge_status.direction = Direction.INPUT
charge_status.pull = Pull.UP
print("Charge Pin:\t%s"%(str(charge_status.value)))

print("Checking Battery Voltage")
analog_in = AnalogIn(m.pin.P0_31)
print("Voltage:\t%s"%(str(analog_in.value)))




qrstring = bytes("{'iic':"+str(addrs)+",'adc':"+str(analog_in.value)+",'post':1}".replace("'","\""),'utf-8')
print(qrstring)
qr = adafruit_miniqr.QRCode()
qr.add_data(qrstring)
qr.make()

palette = displayio.Palette(2)
palette[1] = 0x000000
palette[0] = 0xffffff

bitmap = bitmap_qr(qr.matrix)
tile_grid = displayio.TileGrid(bitmap, pixel_shader=palette)
tile_grid.flip_y=True
# Create a Group to hold the TileGrid
group = displayio.Group(scale=6, x=0, y=0)
group.append(tile_grid)
display.show(group)
while True:
	print("Voltage:\t%s"%(str(analog_in.value*(3.3/2**16)*2)))
	time.sleep(1)
	pass
