from machine import Pin
from lcdManager import writeToScreen

button = Pin(10, Pin.IN, Pin.PULL_DOWN)

def releaseButton():
    writeToScreen("Release the", "button")
    while button.value() == 1:
        pass