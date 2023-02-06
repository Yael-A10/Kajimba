import time
from machine import Pin
from lcdManager import writeToScreen

#button pin setup
button = Pin(10, Pin.IN, Pin.PULL_DOWN)

def releaseButton() -> None:
    """Function that makes sure user releases the button"""
    writeToScreen("Release the", "button")
    while button.value() == 1:
        pass

def holdButton(start: int, string: str) -> bool:
    """Function that checks if the button is being held"""
    start = time.time()
    while button.value() == 1 and time.time()-start < 3:
        time.sleep(0.1)
        writeToScreen("Hold {} s to".format(3-(time.time()-start)), string)
    if time.time()-start >= 3:
        releaseButton()
        return True
    else:
        return False