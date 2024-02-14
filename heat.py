from machine import Pin
import time
led = Pin(22, Pin.OUT)
while True:
    led.value(0)
