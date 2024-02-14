from machine import Pin
import utime

key1 = Pin(5, Pin.IN, Pin.PULL_UP)
key2 = Pin(6, Pin.IN, Pin.PULL_UP)
target_temperature=25
while True:
    if key1.value() == 0:
        utime.sleep_ms(100)
        if key1.value() == 0:
            target_temperature-=1
    if key2.value() == 0:
        utime.sleep_ms(100)
        if key2.value() == 0:
            target_temperature+=1
    print (target_temperature)
    utime.sleep_ms(100)
