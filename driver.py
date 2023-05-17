from machine import Pin, I2C
from neopixel import NeoPixel

class Light:
    buf = []
    def __init__(self):
        for i in range(10):
            row = []
            for j in range(12):
                row.append((0,0,0))
            self.buf.append(row)
        self.light = NeoPixel(Pin(13, Pin.OUT), 120)
        
    def update(self):
        for i in range(10):
            if i % 2 == 0:
                for j in range(12):
                    reverse_col = 11 - j
                    self.light[i*12 + reverse_col] = self.buf[i][j]
            else:
                for j in range(12):
                    self.light[i*12 + j] = self.buf[i][j]
        self.light.write()
    def show(self, img):
        for i in range(10):
            for j in range(12):
                self.buf[i][j] = img[i][j]
        self.update()
    def show_re(self, img):
        for i in range(10):
            for j in range(12):
                self.buf[9-i][j] = img[j][i]
        self.update()
class Touch:
    def __init__(self):
        self.touch = I2C(1, freq=100000, timeout=50)
        
    def is_touch(self, val):
        try:
            if 0 <= val and val < 8:
                buf = self.touch.readfrom_mem(0x50, 8, 1)
                if buf[0] & (1 << val):
                    return True
            if 8 <= val and val < 12:
                buf = self.touch.readfrom_mem(0x50, 9, 1)
                if buf[0] & (1 << (val-8)):
                    return True
        except Exception:
            pass
        return False

