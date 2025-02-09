import time
import machine
from lcdManager import writeToScreen, display, clearDisplay
from pumpManager import pumpSensorPairs, runPumps, checkIfDone, resetValues, logClose, pumpsOff
from buttonManager import button, holdButton
from testManager import runTest

#setup

#variables
ml1 = 285
ml2 = 300
percentToStartSlowing = 75 #variable set between 0 and 90 that controls when the pump(s) start slowing down

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

pumpsOff()

def main() -> None:
    """Main fucntion that loops indefinately"""
    if button.value() == 1:
        if holdButton(time.time(), "start clearing"):
            runPumps(time.time())
        else:
            writeToScreen("Filling...", "Filled: 0/" + str(len(pairList)))
            checkIfDone()
            display()

def chooseML(ml1: int, ml2: int) -> int:
    """Function that allows the user to choose at the beginning of the session between ml1 and ml2"""
    writeToScreen("Click = mL1:{}".format(ml1), "Hold = mL2:{}".format(ml2))
    while button.value() == 0:
        pass
    if holdButton(time.time(), "select ml2:{}".format(ml2)):
        return ml2
    return ml1

try:
    runTest()
    ml = chooseML(ml1, ml2)
    display()
    while True:
        main()
except KeyboardInterrupt:
    pumpsOff()
    clearDisplay()
    onLED.off()
    logClose()