import machine
from machine import SPI, Pin
import time
import st7789
import vga2_8x16 as font

# 设置I2C总线
i2c = machine.I2C(0, scl=machine.Pin(21), sda=machine.Pin(20))

# nsht30传感器的地址
nsht30_addr = 0x44

# 发送命令以获取温湿度数据
i2c.writeto(nsht30_addr, bytes([0xf3]))

# 等待传感器准备好数据
time.sleep(0.1)

# 读取温湿度数据
data = i2c.readfrom(nsht30_addr, 6)
time.sleep(0.1)

spi = SPI(0, baudrate=40_000_000, polarity=1, phase=0, sck=Pin(18,Pin.OUT), mosi=Pin(19,Pin.OUT))
display = st7789.ST7789(spi, 240, 320, 
                        reset=Pin(0, Pin.OUT),
                        dc=Pin(1, Pin.OUT),
                        cs=Pin(4, Pin.OUT),
                        backlight=Pin(16, Pin.OUT),
                        color_order = st7789.RGB,
                        inversion = False,
                        rotation = 0)
display.init()
key1 = Pin(5, Pin.IN, Pin.PULL_UP)
key2 = Pin(6, Pin.IN, Pin.PULL_UP)
target_temperature=25
heat = Pin(22, Pin.OUT)

class PID():
    def __init__(self, dt, max, min, Kp, Ki, Kd):
        self.dt = dt  # 循环时长
        self.max = max  # 操作变量最大值
        self.min = min  # 操作变量最小值
        self.Kp = Kp  # 比例增益
        self.Ki = Ki  # 微分增益
        self.Kd = Kd  # 积分增益
        self.integral = 0  # 直到上一次的误差值
        self.pre_error = 0  # 上一次的误差值

    def calculate(self, setPoint, pv):
        # 其中 pv:process value 即过程值，
        error = setPoint - pv  # 误差（设定值与实际值的差值）
        Pout = self.Kp * error  # 比例项 Kp * e(t)
        self.integral += error * self.dt  #∑e(t)*△t
        Iout = self.Ki * self.integral  # 积分项 Ki * ∑e(t)*△t
        derivative = (error - self.pre_error) / self.dt  #(e(t)-e(t-1))/△t
        Dout = self.Kd * derivative  # 微分项 Kd * (e(t)-e(t-1))/△t

        output = Pout + Iout + Dout  # 新的目标值  位置式PID：u(t) = Kp*e(t) + Ki * ∑e(t)*△t + Kd * (e(t)-e(t-1))/△t

        if (output > self.max):
            output = self.max
        elif (output < self.min):
            output = self.min

        self.pre_error = error  # 保存本次误差，以供下次计算  e(k-1) = e(k)
        return output
pid = PID(0.1, 100, 0, 0.1, 0.5, 0.01)
while (True):
    temperature = round(((data[0] << 8) | data[1]) * 175 / 0xffff - 45,1)
    humidity = round(((data[3] << 8) | data[4]) * 100 / 0xffff,1)
    if key1.value() == 0:
        time.sleep_ms(100)
    if key1.value() == 0:
        target_temperature-=1
    if key2.value() == 0:
        time.sleep_ms(100)
        if key2.value() == 0:
            target_temperature+=1
    display.text(font, "present humidity:",10, 25, st7789.WHITE)
    display.text(font, str(humidity),200, 25, st7789.WHITE)
    display.text(font, "present temperature:",10, 75, st7789.WHITE)
    display.text(font, str(temperature),200, 75, st7789.WHITE)
    display.text(font, "target temperature:",10, 125, st7789.WHITE)
    display.text(font, str(target_temperature),200, 125, st7789.WHITE)
    display.text(font, "target humidity:",10, 175, st7789.WHITE)
    if temperature<target_temperature:
        heat.value(1)
        time.sleep_ms(calculate(target_temperature,temperature))
    else:
        heat.value(0)
    
