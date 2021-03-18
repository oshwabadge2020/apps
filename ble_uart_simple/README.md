# BLE UART Simple

This is a sample / demo application that makes the OHS 2020 badge appear as a Bluetooth Low Energy device. It will advertise the Nordic Uart Service (NUS), and will communicate using simple line-terminated ('\n') messages. This could be a starting point for more advanced communication with a PC, phone, or other devices.

Also included is a google chrome extension that can be used to mute/unmute a google Meet window using the badge. See [theterg/google-meet-BLE-NUS-remote](https://github.com/theterg/google-meet-BLE-NUS-remote) for more information. For some browsers you may need to enable the `#experimental-web-platform-features` flag in `chrome://flags`. See [this](https://web.dev/bluetooth/) for more information.

## How to install

* (Optional) Hold down the SW1 button while connecting the OHS2020 badge to your PC. Download [the latest version of circuitPython](https://circuitpython.org/board/ohs2020_badge/) and copy it onto the drive. Wait for the device to reboot.
    * This code was tested on 6.1.0.
* Plug your OHS 2020 Badge into a PC via the USB connection. The badge should show up as a flash drive
* Copy this folder (MINUS the crx file) onto the flash drive
* (Optional) navigate to `about://extensions` and drag the included CRX file into the window to install the Google Meet plugin

## Protocol

Pretty simple, not much to be mentioned here:
* Any button presses will cause the device to emit `buttonA`, `buttonB`, `buttonC`, or `buttonD` over NUS depending on which button was pressed
* Send the command `red`, `green`, or `blue`, to make the screen display a solid color
* Send the command `ok` to display a green checkmark
* Send the command `cancel` to display a red cancel icon
* Send the command `bluetooth` to display the bluetooth logo

As of this writing, the various sensors have been initialized but not exposed over this interface. More to come, i'm sure!
