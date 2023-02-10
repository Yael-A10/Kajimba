from machine import I2C, Pin
from pico_i2c_lcd import I2cLcd

#lcd screen setup
I2C_ADDR     = 0x27
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)

#test if diplay is connected
try:
    lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)
    displayConnected = True
except OSError:
    print('Display is not connected')
    displayConnected = False

def addBlankSpace(string: str) -> str:
    """Function that adds spaces to a string being printed to the lcd screen so that there is no overlap"""
    if string == "":
        return string
    stringLen = len(string)
    if not stringLen > 16:
        string = string + " "*(16-stringLen)
        return string
    return string

def writeToScreen(str1: str, str2:str) -> None:
    """Function that allows text to be written on the lcd screen"""
    if displayConnected:
        str1 = addBlankSpace(str1)
        str2 = addBlankSpace(str2)
        if str1 != "":
            lcd.move_to(0,0)
            lcd.putstr(str1)
        if str2 != "":
            lcd.move_to(0,1)
            lcd.putstr(str2)

def display() -> None:
    """Function that displays the total and session fill counts to the lcd screen"""
    from pumpManager import session_fill_count, total_fill_count
    writeToScreen("Filled: " + str(session_fill_count),"Total: " + str(total_fill_count))

def clearDisplay() -> None:
    """Function that clears the lcd screen"""
    if displayConnected:
        lcd.clear()