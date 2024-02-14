import uos
import test.st7789 as st7789
from test.fonts import vga2_8x8 as font1
from test.fonts import vga1_16x32 as font2
import random
import framebuf
from machine import Pin, SPI, ADC,PWM
import time, math,array
from utime import sleep_ms
import struct

pwm = PWM(Pin(19))
pwm.freq(50)

#image_file0 = "/logo.bin" #图片文件地址

st7789_res = 0
st7789_dc  = 1
disp_width = 240
disp_height = 240
CENTER_Y = int(disp_width/2)
CENTER_X = int(disp_height/2)
spi_sck=Pin(2)
spi_tx=Pin(3)
spi0=SPI(0,baudrate=4000000, phase=1, polarity=1, sck=spi_sck, mosi=spi_tx)

display = st7789.ST7789(spi0, disp_width, disp_width,
                          reset=machine.Pin(st7789_res, machine.Pin.OUT),
                          dc=machine.Pin(st7789_dc, machine.Pin.OUT),
                          xstart=0, ystart=0, rotation=0)
display.fill(st7789.BLACK)
display.text(font2, "EETREE", 10, 10)
display.text(font2, "www.eetree.cn", 10, 40)


# xAxis = ADC(Pin(28))
# yAxis = ADC(Pin(29))

buttonM = Pin(5,Pin.IN, Pin.PULL_UP) #B
buttonS = Pin(6,Pin.IN, Pin.PULL_UP) #A
buttonL = Pin(7,Pin.IN, Pin.PULL_UP) #A
buttonPRESS = Pin(8,Pin.IN, Pin.PULL_UP) #A
buttonR = Pin(9,Pin.IN, Pin.PULL_UP) #A
'''
f_image = open(image_file0, 'rb')
 
for column in range(1,240):
                buf=f_image.read(480)
                display.blit_buffer(buf, 1, column, 240, 1)
'''

while True:

#     xValue = xAxis.read_u16()
#     yValue = yAxis.read_u16()
    
    buttonValueM = buttonM.value()
    buttonValueS = buttonS.value()
    buttonValueL = buttonL.value()
    buttonValuePRESS = buttonPRESS.value()
    buttonValueR = buttonR.value()
    
#     display.text(font1, "xVaule="+"%05d" %(xValue) , 10, 70)
#     display.text(font1, "yVaule="+"%05d" %(yValue), 120, 70)
    
    display.text(font1, "buttonValueM="+str(buttonValueM), 10, 90)
    display.text(font1, "buttonValueS="+str(buttonValueS), 10, 110)
    display.text(font1,"buttonValueL="+str(buttonValueL) , 10, 130)
    display.text(font1, "buttonValuePRESS="+str(buttonValuePRESS), 10, 150)
    display.text(font1, "buttonValueR="+str(buttonValueR), 10, 170)


