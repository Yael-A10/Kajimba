import time
import machine

from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd

I2C_ADDR     = 0x27
I2C_NUM_ROWS = 4
I2C_NUM_COLS = 20
i2c = machine.I2C(0, sda=machine.Pin(0), scl=machine.Pin(1), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)

flow_meter = machine.Pin(17, machine.Pin.IN, machine.Pin.PULL_UP)
relay = machine.Pin(16, machine.Pin.OUT)

count = 0

def countPulse(pin):
    global count
    count += 1

flow_meter.irq(trigger = machine.Pin.IRQ_RISING, handler = countPulse)

lcd.clear()
flow = 0
relay.value(1)

while flow<1000:
    time.sleep(0.3)
    lcd.clear()
    flow = count
    print(flow)
    lcd.putstr(str(flow))
    
relay.value(0)
lcd.clear()