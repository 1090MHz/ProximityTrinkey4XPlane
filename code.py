import struct
import time

import board
import busio
import neopixel
import touchio
import usb_hid
import adafruit_apds9960.apds9960


# Sensitivity settings, matching the Trinkey's factory demo. Higher values
# detect objects from farther away, but close objects reach 255 sooner.
PROXIMITY_GAIN = 3   # 0-3 = 1x, 2x, 4x, 8x receiver gain
LED_BOOST = 3        # 0-3 = 100%, 150%, 200%, 300% LED current
PULSE_COUNT = 1      # 1-64 infrared pulses per reading
PULSE_LENGTH = 2     # 0-3 = 4, 8, 16, 32 microsecond pulses
NOISE_FLOOR = 3      # readings below this are treated as 0

_PPULSE_REGISTER = 0x8E
_CONTROL_REGISTER = 0x8F
_CONFIG2_REGISTER = 0x90

i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_apds9960.apds9960.APDS9960(i2c)


def read_register(register):
    buffer = bytearray(1)
    with sensor.i2c_device as device:
        device.write_then_readinto(bytes([register]), buffer)
    return buffer[0]


def write_register(register, value):
    with sensor.i2c_device as device:
        device.write(bytes([register, value]))


write_register(_PPULSE_REGISTER, (PULSE_LENGTH << 6) | (PULSE_COUNT - 1))
write_register(_CONTROL_REGISTER, (read_register(_CONTROL_REGISTER) & 0xF3) | (PROXIMITY_GAIN << 2))
write_register(_CONFIG2_REGISTER, (read_register(_CONFIG2_REGISTER) & 0xCF) | (LED_BOOST << 4))

sensor.enable_proximity = True

pixels = neopixel.NeoPixel(board.NEOPIXEL, 2)
gamepad = usb_hid.devices[0]
touch1 = touchio.TouchIn(board.TOUCH1)
touch2 = touchio.TouchIn(board.TOUCH2)

last_proximity = None
last_buttons = None

while True:
    proximity = sensor.proximity
    if proximity < NOISE_FLOOR:
        proximity = 0
    buttons = int(touch1.value) | (int(touch2.value) << 1)
    if proximity != last_proximity or buttons != last_buttons:
        # The APDS9960 reads higher when an object is closer.
        axis_value = proximity - 128
        report = struct.pack("<Bb", buttons, axis_value)
        gamepad.send_report(report, report_id=1)

        # Dark when nothing is near; brighter red as an object approaches.
        pixels.fill((proximity, 0, 0))

        last_proximity = proximity
        last_buttons = buttons

    time.sleep(0.02)
