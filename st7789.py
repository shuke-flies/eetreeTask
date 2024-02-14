from machine import SPI, Pin
import st7789
import time
import math
import vga1_8x8 as font

spi = SPI(0, baudrate=40_000_000, polarity=1, phase=0, sck=Pin(18,Pin.OUT), mosi=Pin(19,Pin.OUT))
display = st7789.ST7789(spi, 240, 320, 
                        reset=Pin(0, Pin.OUT),
                        dc=Pin(1, Pin.OUT),
                        cs=Pin(4, Pin.OUT),
                        backlight=Pin(16, Pin.OUT),
                        color_order = st7789.RGB,
                        inversion = False,
                        rotation = 2)
display.init()

COLORS = [
    0xFFE0, # yellow
    0x0000, # black
    st7789.BLUE,
    st7789.RED,
    st7789.GREEN,
    st7789.CYAN,
    st7789.MAGENTA,
    st7789.YELLOW,
    st7789.WHITE,
    st7789.BLACK]

for color in COLORS:
    display.fill(color)
    time.sleep_ms(400)

display.text(font, "Hello world", 0, 0, st7789.WHITE)
display.circle(120, 160, 50, st7789.WHITE)
display.vline(120, 160, 50, st7789.BLUE)
display.hline(120, 160, 50, st7789.RED)
display.rect(10, 20, 10, 20, st7789.YELLOW)
display.fill_rect(10, 50, 10, 20, st7789.GREEN)
display.fill_circle(120, 160, 5, st7789.WHITE)

pointlist=((0,0),(20,0),(30,30),(0,20),(0,0))
display.polygon(pointlist, 120, 50, st7789.WHITE, 0, 120, 50)
display.polygon(pointlist, 120, 50, st7789.GREEN, math.pi/2, 0, 0)

display.fill_polygon(((0,0),(10,0),(5,7),(0,0)), 115, 40, st7789.RED)

time.sleep_ms(200)
for x in range(240):
    y = int(80*math.sin(0.125664*x)) + 160
    display.pixel(x, y, st7789.MAGENTA)
    
    
for d in range(-90,-185,-5):
    a = d * math.pi / 180
    x1 = int(50*math.cos(a)+120)
    y1 = int(50*math.sin(a)+160)
    display.line(120, 160, x1, y1, st7789.CYAN)
    time.sleep_ms(50)
 
 
time.sleep(5)

display.off() # Turn off the backlight pin if one was defined during init.

time.sleep(2)
display.on()