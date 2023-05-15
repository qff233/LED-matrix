from machine import Pin
from neopixel import NeoPixel
import time

class Light:
    buf = []
    def __init__(self):
        for i in range(120):
            self.buf.append((0,0,0))
        self.light = NeoPixel(Pin(13, Pin.OUT), 120)
        
    def update(self):
        for i in range(120):
            row = int(i/12)
            col = i % 12
            if row % 2 == 0:
                reverse_col = 11 - col
                self.light[row*12 + reverse_col] = self.buf[row*12 + col]
            else:
                self.light[i] = self.buf[i]
        self.light.write()

light = Light()
    
for i in range(120):
    light.buf[i] = (255, 255, 0)
    light.update()
time.sleep(0.2)


    