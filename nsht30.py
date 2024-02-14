import machine
import time

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

# 解析温湿度数据
while (True):
    temperature = ((data[0] << 8) | data[1]) * 175 / 0xffff - 45
    humidity = ((data[3] << 8) | data[4]) * 100 / 0xffff

    # 打印温湿度数据
    print('Temperature: {}°C, Humidity: {}%'.format(temperature, humidity))
    time.sleep_ms(500)
