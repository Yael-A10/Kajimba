import time
import machine

from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd

I2C_ADDR     = 0x27
I2C_NUM_ROWS = 4
I2C_NUM_COLS = 20
i2c = machine.I2C(0, sda=machine.Pin(0), scl=machine.Pin(1), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)

button = machine.Pin(18, machine.Pin.IN, machine.Pin.PULL_DOWN)
log = open("logs.txt", "r")
total_fill_count = int(log.read())
log.close()

#flow meter and pump pairs
flow_meter = machine.Pin(17, machine.Pin.IN, machine.Pin.PULL_UP)
relay = machine.Pin(16, machine.Pin.OUT)

groups = [[relay, flow_meter, 0, False, True]]

"""count = 0
def countPulse(pin):
    global count
    count += 1
flow_meter.irq(trigger = machine.Pin.IRQ_RISING, handler = countPulse)"""

def counter(fm, counter, state):
    if not fm.value() and state:
        counter += 1
        state = False
        #print(counter, count)
    if fm.value():
        state = True
    return counter, state

ml = 300
session_fill_count = 0
lcd.clear()
lcd.move_to(0,0)
lcd.putstr("Filled: " + str(session_fill_count))
lcd.move_to(0,1)
lcd.putstr("Total: " + str(total_fill_count))

try:
    while True:
        if button.value() == 1:
            lcd.move_to(0,0)
            lcd.putstr("Filling...")
            lcd.move_to(0,1)
            lcd.putstr("Filled: 0/" + str(len(groups)))
            for x in groups:
                x[0].value(1)
                x[2] = 0
                x[3] = False
                x[4] = True
            done = 0
            while done<len(groups):
                for x in groups:
                    if x[4]:
                        result = counter(x[1], x[2], x[3])
                        x[2] = result[0]
                        if result[0]/4 >= ml:
                            x[0].value(0)
                            x[4] = False
                            done += 1
                            lcd.move_to(8,1)
                            lcd.putstr(str(done))
                            session_fill_count+=1
                            total_fill_count+=1
                        x[3] = result[1]
            log = open("logs.txt", "w")
            log.write(str(total_fill_count))
            log.close()
            time.sleep(1)
            lcd.clear()
            lcd.move_to(0,0)
            lcd.putstr("Filled: " + str(session_fill_count))
            lcd.move_to(0,1)
            lcd.putstr("Total: " + str(total_fill_count))
except KeyboardInterrupt:
    for x in groups:
        x[0].value(0)
    lcd.clear()
    log.close()