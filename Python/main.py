import time
import machine
from lcdManager import writeToScreen, display, clearDisplay
from pumpManager import pumpSensorPairs, runPumps, checkIfDone, resetValues, logClose
from buttonManager import releaseButton, button, holdButton
from testManager import runTest

#setup

#variables
ml = 285

#led built into the raspberry pi pico used as power indicator
onLED = machine.Pin(25, machine.Pin.OUT)
onLED.on() 

#define the pump and flow sensor pins:
mosfet1 = 19
flowSensor1 = 8

#create the pump and flow sensor pairs:
pair1 = pumpSensorPairs(mosfet1, flowSensor1)

#add the pairs into the pair list
pairList = [pair1]

for pair in pairList:
    pair.pumpOff()

def main() -> None:
    """Main fucntion that loops indefinately"""
    if button.value() == 1:
        if holdButton(time.time(), "start clearing"):
            runPumps(time.time())
        else:
            writeToScreen("Filling...", "Filled: 0/" + str(len(pairList)))
            checkIfDone()
            resetValues()
            time.sleep(1)
            display()

try:
    runTest()
    display()
    while True:
        main()
except KeyboardInterrupt:
    for pair in pairList:
        pair.pumpOff()
    clearDisplay()
    onLED.off()
    logClose()