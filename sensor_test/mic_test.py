import time
import array
import math
import board
import audiobusio
import microcontroller
from digitalio import DigitalInOut, Direction, Pull
     
     
# Remove DC bias before computing RMS.
def mean(values):
    return sum(values) / len(values)
     
 
def normalized_rms(values):
    minbuf = int(mean(values))
    samples_sum = sum(
        float(sample - minbuf) * (sample - minbuf)
        for sample in values
    )
 
    return math.sqrt(samples_sum / len(values))
 
     
# Main program

ws = DigitalInOut(microcontroller.pin.P0_27)
ws.direction = Direction.OUTPUT
ws.value = False

ms = DigitalInOut(microcontroller.pin.P0_26)
ms.direction = Direction.OUTPUT
ms.value = False


mic = audiobusio.PDMIn(board.MICROPHONE_CLOCK, board.MICROPHONE_DATA, sample_rate=16000, bit_depth=16)
samples = array.array('H', [0] * 160)
     
     
while True:
    mic.record(samples, len(samples))
    magnitude = normalized_rms(samples)
    print((magnitude,))
    time.sleep(0.1)
