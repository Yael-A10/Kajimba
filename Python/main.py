import time
import machine
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd

#variables
ml = 285
session_fill_count = 0

#led built into the raspberry pi pico used as power indicator
onLED = machine.Pin(25, machine.Pin.OUT)
timer = machine.Timer()
onLED.on() 

#setup
I2C_ADDR     = 0x27
I2C_NUM_ROWS = 4
I2C_NUM_COLS = 20
i2c = machine.I2C(0, sda=machine.Pin(0), scl=machine.Pin(1), freq=400000)

#test if diplay is connected
try:
    lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)
    displayConnected = True
except OSError:
    print('Display is not connected')
    displayConnected = False

button = machine.Pin(10, machine.Pin.IN, machine.Pin.PULL_DOWN)
log = open("logs.txt", "r")
total_fill_count = int(log.read())
log.close()

#flow meter and pump pairs
flow_meter = machine.Pin(8, machine.Pin.IN, machine.Pin.PULL_UP)
mosfet = machine.PWM(machine.Pin(19))
mosfet.freq(100000)

pumpGroups = {"mosfet": [mosfet], "flowSensor": [flow_meter], "count": [0], "state":[False], "done": [False]}

def counter(fm, counter, state):
    if not fm.value() and state:
        counter += 1
        state = False
        #print(counter, count)
    if fm.value():
        state = True
    return counter, state

#this function adds spaces to a string being printed to the screen so that there is no overlap
def addBlankSpace(string):
    if string == "":
        return string
    stringLen = len(string)
    if stringLen > 16:
        return string
    else:
        string = string + " "*(16-stringLen)
        return string

def writeToScreen(str1, str2):
    str1 = addBlankSpace(str1)
    str2 = addBlankSpace(str2)
    if displayConnected:
        if str1 != "":
            lcd.move_to(0,0)
            lcd.putstr(str1)
        if str2 != "":
            lcd.move_to(0,1)
            lcd.putstr(str2)

def releaseButton():
    writeToScreen("Release the", "button")
    while button.value() == 1:
        pass

def runPumps(start):
    for group in range(0,len(pumpGroups["mosfet"])):
        pumpGroups["mosfet"][group].duty_u16(65000)
    writeToScreen("Clearing...", "Run time:")
    while button.value() == 0:
        writeToScreen("", "Run time: {}".format(time.time()-(start)) + "s")
    for group in range(0,len(pumpGroups["mosfet"])):
        pumpGroups["mosfet"][group].duty_u16(0)
    releaseButton()
    display()

def resetPumpValues():
    for group in range(0,len(pumpGroups["mosfet"])):
        pumpGroups["mosfet"][group].duty_u16(0)
        pumpGroups["count"][group] = 0
        pumpGroups["state"][group] = False
        pumpGroups["done"][group] = False

def checkIfDone():
    global session_fill_count
    global total_fill_count
    done = 0
    while done<len(pumpGroups["mosfet"]) and button.value() == 0:
        for group in range(0,len(pumpGroups["mosfet"])):
            if not pumpGroups["done"][group]:
                result = counter(pumpGroups["flowSensor"][group], pumpGroups["count"][group], pumpGroups["state"][group])
                pumpGroups["count"][group] = result[0]
                pumpGroups["mosfet"][group].duty_u16(int(65000-25000*((result[0]/4)/ml))) #slow down the pump as the bottle fills
                if result[0]/4 >= ml:
                    pumpGroups["mosfet"][group].duty_u16(0)
                    pumpGroups["done"][group] = True
                    done += 1
                    if displayConnected:
                        lcd.move_to(8,1)
                        lcd.putstr(str(done))
                    session_fill_count+=1
                    total_fill_count+=1
                pumpGroups["state"][group] = result[1]

def writeToLog():
    log = open("logs.txt", "w")
    log.write(str(total_fill_count))
    log.close()

def display():
    writeToScreen("Filled: " + str(session_fill_count),"Total: " + str(total_fill_count))

def main():
    if button.value() == 1:
        start = time.time()
        while button.value() == 1 and time.time()-start < 3:
            time.sleep(0.1)
            writeToScreen("Hold {} s to".format(3-(time.time()-start)), "start clearing")
        if time.time()-start >= 3:
            releaseButton()
            runPumps(time.time())
        else:
            writeToScreen("Filling...", "Filled: 0/" + str(len(pumpGroups["mosfet"])))
            checkIfDone()
            resetPumpValues()
            writeToLog()
            time.sleep(1)
            display()

def test():
    start = time.time()
    writeToScreen("Testing...", "Tested: 0/" + str(len(pumpGroups["mosfet"])))
    done = 0
    while done<len(pumpGroups["mosfet"]) and button.value() == 0 and time.time()-start < 10:
        for group in range(0,len(pumpGroups["mosfet"])):
            if not pumpGroups["done"][group]:
                result = counter(pumpGroups["flowSensor"][group], pumpGroups["count"][group], pumpGroups["state"][group])
                pumpGroups["count"][group] = result[0]
                pumpGroups["mosfet"][group].duty_u16(65000)
                if result[0]/4 >= 10: #checks if 10ml have been passed through the flow sensor
                    pumpGroups["mosfet"][group].duty_u16(0)
                    pumpGroups["done"][group] = True
                    done += 1
                    if displayConnected:
                        lcd.move_to(8,1)
                        lcd.putstr(str(done))
                pumpGroups["state"][group] = result[1]
    resetPumpValues()
    return done>=len(pumpGroups["mosfet"])

def askForTest(start):
    while button.value() == 1 and time.time()-start < 3:
        time.sleep(0.1)
        writeToScreen("Hold {} s to".format(3-(time.time()-start)), "start testing")
    if time.time()-start >= 3:
        releaseButton()
        return True
    else:
        return False

try:
    if displayConnected:
        passed = False
        while not passed:
            writeToScreen("Click btn = skip", "Hold 3 s = test")
            while button.value() == 0:
                pass
            if askForTest(time.time()):
                if not test():
                    writeToScreen("Please check", "pump/flow sensor")
                    print("There might be a problem with the pump/flow sensor pairs, please ensure they are both connected and function correctly.")
                    time.sleep(2)
                else:
                    passed = True
    display()
    while True:
        main()
except KeyboardInterrupt:
    for group in range(0,len(pumpGroups["mosfet"])):
        pumpGroups["mosfet"][group].duty_u16(0)
    if displayConnected:
        lcd.clear()
    log.close()