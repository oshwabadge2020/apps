import board
import busio
import microcontroller as m
import time
from analogio import AnalogIn
from digitalio import DigitalInOut, Direction, Pull

import adafruit_imageload
import adafruit_bme680
import adafruit_lsm9ds1
from adafruit_apds9960 import apds9960
from adafruit_display_shapes.rect import Rect
import displayio
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService
from _bleio import BluetoothError

# Initialize Bluetooth globals
ble = BLERadio()
uart = UARTService()
advertisement = ProvideServicesAdvertisement(uart)

# Turn on the LCD backlight and enable the display
display = board.DISPLAY
# Override brightness to save power
display.auto_brightness = False
display.brightness = 0.2

print('Hello!')


def display_image(filename):
    img, img_palette = adafruit_imageload.load(filename,
                                               bitmap=displayio.Bitmap,
                                               palette=displayio.Palette)
    tile_grid = displayio.TileGrid(img, pixel_shader=img_palette)
    group = displayio.Group(scale=4)
    group.append(tile_grid)
    display.show(group)


print('Scanning for I2C Devices..')
i2c = busio.I2C(board.SCL, board.SDA)
i2c.try_lock()
addrs = ['%02x' % (x) for x in i2c.scan()]
print(addrs)
# ['0x1e', '0x39', '0x6b', '0x76']

iicdevs = "X"
if len(addrs) == 4:
    if '1e' in addrs:
        if '39' in addrs:
            if '6b' in addrs:
                if '76' in addrs:
                    iicdevs = "V"
                    print("All devices present!")

iicdevstr = ""
for h in addrs:
    iicdevstr += h
i2c.unlock()

print('Initializing Sensors')
temp = adafruit_bme680.Adafruit_BME680_I2C(i2c, address=0x76)
print('Temperature: {} degrees C'.format(temp.temperature))
print('Gas: {} ohms'.format(temp.gas))
print('Humidity: {}%'.format(temp.humidity))
print('Pressure: {}hPa'.format(temp.pressure))
prox = apds9960.APDS9960(i2c)
prox.enable_color = True
while not prox.color_data_ready:
    time.sleep(0.005)
r, g, b, c = prox.color_data
print('Red: {0}, Green: {1}, Blue: {2}, Clear: {3}'.format(r, g, b, c))
imu = adafruit_lsm9ds1.LSM9DS1_I2C(i2c)
print('Acceleration (m/s^2): ({0:0.3f},{1:0.3f},{2:0.3f})'.format(*imu.acceleration))
print('Magnetometer (gauss): ({0:0.3f},{1:0.3f},{2:0.3f})'.format(*imu.magnetic))
print('Gyroscope (degrees/sec): ({0:0.3f},{1:0.3f},{2:0.3f})'.format(*imu.gyro))
print('Temperature: {0:0.3f}C'.format(imu.temperature))

print('Checking Charge Status Pin')
charge_status = DigitalInOut(m.pin.P0_16)
charge_status.direction = Direction.INPUT
charge_status.pull = Pull.UP
print("Charge Pin:\t%s" % (str(charge_status.value)))

SW_A = DigitalInOut(m.pin.P0_29)
SW_A.direction = Direction.INPUT
SW_A.pull = Pull.UP
SW_B = DigitalInOut(m.pin.P0_03)
SW_B.direction = Direction.INPUT
SW_B.pull = Pull.UP
SW_C = DigitalInOut(m.pin.P0_17)
SW_C.direction = Direction.INPUT
SW_C.pull = Pull.UP
SW_D = DigitalInOut(m.pin.P1_03)
SW_D.direction = Direction.INPUT
SW_D.pull = Pull.UP

print("Checking Battery Voltage")
analog_in = AnalogIn(m.pin.P0_31)
print("Voltage:\t%s" % (str(analog_in.value)))

buttons = [SW_A.value, SW_B.value, SW_C.value, SW_D.value]
_buttons = buttons

while True:
    buttons = [SW_A.value, SW_B.value, SW_C.value, SW_D.value]

    if not ble.connected:
        # First: always keep advertising if we can
        # Unfortunately ble.advertising doesn't seem to work,
        # So we'll just always try to enable advertising
        try:
            ble.start_advertising(advertisement)
        except BluetoothError:
            pass
        # **** Unconnected Behavior ****
        # Just print some stuff!
        print("Voltage:\t%s" % (str(analog_in.value * (3.3 / 2**16) * 2)))
        time.sleep(1)
        # Check the buttons
        if not buttons[0] and _buttons[0]:
            print('Button A pressed!')
        if not buttons[1] and _buttons[1]:
            print('Button B pressed!')
        if not buttons[2] and _buttons[2]:
            print('Button C pressed!')
        if not buttons[3] and _buttons[3]:
            print('Button D pressed!')
        if ble.connected:
            display_image('/bluetooth.bmp')
    else:
        # **** Connected Behavior ****
        # If any data has been sent to us, read it
        # NOTE: this assumes line-terminated messages!
        if uart.in_waiting:
            s = uart.readline()
            if s:
                s = s.strip().decode()
                print(s)
                if s == 'ok':
                    display_image('/ok.bmp')
                if s == 'cancel':
                    display_image('/cancel.bmp')
                if s == 'bluetooth':
                    display_image('/bluetooth.bmp')
                if s == 'green':
                    group = displayio.Group()
                    group.append(Rect(0, 0, 240, 240, fill=0x00FF00))
                    display.show(group)
                if s == 'red':
                    group = displayio.Group()
                    group.append(Rect(0, 0, 240, 240, fill=0xFF0000))
                    display.show(group)
                if s == 'blue':
                    group = displayio.Group()
                    group.append(Rect(0, 0, 240, 240, fill=0x0000FF))
                    display.show(group)
        # Check the buttons
        if not buttons[0] and _buttons[0]:
            uart.write(b'buttonA\n')
        if not buttons[1] and _buttons[1]:
            uart.write(b'buttonB\n')
        if not buttons[2] and _buttons[2]:
            uart.write(b'buttonC\n')
        if not buttons[3] and _buttons[3]:
            uart.write(b'buttonD\n')
    _buttons = buttons
    if not ble.connected:
        display.show(None)
