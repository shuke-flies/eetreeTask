from machine import SPI, Pin
import st7789
import time
import vga2_8x16 as font

spi = SPI(0, baudrate=40_000_000, polarity=1, phase=0, sck=Pin(2,Pin.OUT), mosi=Pin(3,Pin.OUT))
display = st7789.ST7789(spi, 240, 320, 
                        reset=Pin(0, Pin.OUT),
                        dc=Pin(1, Pin.OUT),
                        cs=Pin(4, Pin.OUT),
                        backlight=Pin(16, Pin.OUT),
                        color_order = st7789.RGB,
                        inversion = False,
                        rotation = 0)
display.init()


display.text(font, "present humidity:",10, 25, st7789.WHITE)
display.text(font, "present temperature:",10, 75, st7789.WHITE)
display.text(font, "target temperature:",10, 125, st7789.WHITE)
display.text(font, "present humidity:",10, 175, st7789.WHITE)
