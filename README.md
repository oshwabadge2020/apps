# apps
The circuitpython application code that will run on the badge.

## sensor_test
* initial test code from Michael Welling (@mwelling)
* prints i2c sensor data to LCD and serial
```Temperature: 27.8 C
Gas: 38599 ohm
Humidity: 21.9 %
Pressure: 1020.566 hPa
Altitude = -60.73 meters
Acceleration (m/s^2): (0.738,0.323,-9.606)
Magnetometer (gauss): (-0.029,0.030,0.450)
Gyroscope (degrees/sec): (0.114,0.936,-0.674)
Temperature: 23.500C
```
* note: on early prototype versions of the badge, the i2c bus was shorted so this code would get stuck as it can not access i2c bus

## loader_proto
*  @siddacious attempt to make an apps menu

## factory_test
* factory test by @acamilo that displays QR
