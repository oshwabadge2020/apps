import board
import time
import displayio
import busio
import adafruit_bme680
import adafruit_lsm9ds1

from adafruit_apds9960.apds9960 import APDS9960
from digitalio import DigitalInOut, Direction, Pull


backlight = DigitalInOut(board.TFT_BACKLIGHT)
backlight.direction = Direction.OUTPUT
backlight.value = False

i2c = busio.I2C(board.SCL, board.SDA)

apds = APDS9960(i2c)
apds.enable_proximity = True
apds.enable_gesture = True

bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c, address=118, debug=False)

# change this to match the location's pressure (hPa) at sea level
bme680.sea_level_pressure = 1013.25

sensor = adafruit_lsm9ds1.LSM9DS1_I2C(i2c)

while True:
    gesture = apds.gesture()

    if gesture == 0x01:
        print("up")
    elif gesture == 0x02:
        print("down")
    elif gesture == 0x03:
        print("left")
    elif gesture == 0x04:
        print("right")

    print("\nTemperature: %0.1f C" % bme680.temperature)
    print("Gas: %d ohm" % bme680.gas)
    print("Humidity: %0.1f %%" % bme680.humidity)
    print("Pressure: %0.3f hPa" % bme680.pressure)
    print("Altitude = %0.2f meters" % bme680.altitude)

    accel_x, accel_y, accel_z = sensor.acceleration
    mag_x, mag_y, mag_z = sensor.magnetic
    gyro_x, gyro_y, gyro_z = sensor.gyro
    temp = sensor.temperature
    # Print values.
    print('Acceleration (m/s^2): ({0:0.3f},{1:0.3f},{2:0.3f})'.format(accel_x, accel_y, accel_z))
    print('Magnetometer (gauss): ({0:0.3f},{1:0.3f},{2:0.3f})'.format(mag_x, mag_y, mag_z))
    print('Gyroscope (degrees/sec): ({0:0.3f},{1:0.3f},{2:0.3f})'.format(gyro_x, gyro_y, gyro_z))
    print('Temperature: {0:0.3f}C'.format(temp))

    time.sleep(.1)

