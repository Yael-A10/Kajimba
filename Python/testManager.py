import time
from machine import Pin
from pumpManager import resetValues, pumpsOn
from buttonManager import button, holdButton
from lcdManager import writeToScreen, displayConnected

def test(pairList: list) -> bool:
    """Function that runs the pump(s) and stops when the flow sensor(s) has reached 10 ml"""
    done = 0
    start = time.time()
    writeToScreen("Testing...", "Tested: 0/" + str(len(pairList)))
    pumpsOn()
    while done<len(pairList) and button.value() == 0 and time.time()-start < 10:
        for pair in pairList:
            pair.flowSensor.irq(trigger = Pin.IRQ_RISING, handler = pair.countPulse) #activate interrupt handler
            if not pair.done:
                if pair.count/4 >= 10: #checks if 10ml have been passed through the flow sensor(s)
                    pair.pumpOff()
                    pair.done = True
                    done += 1
                    writeToScreen("", "Tested {}/{}".format(str(done), len(pairList)))
    for pair in pairList:
        pair.flowSensor.irq(trigger = Pin.IRQ_RISING, handler = None) # type: ignore #deactivate interrupt handler
    resetValues()
    return done>=len(pairList)

def askForTest(start: int) -> bool:
    """Function that returns True if button was held and False if it wasn't"""
    return holdButton(time.time(), "start testing")

def runTest() -> None:
    if displayConnected:
        passed = False
        from main import pairList
        while not passed:
            writeToScreen("Click btn = skip", "Hold 3 s = test")
            while button.value() == 0:
                pass
            if askForTest(time.time()):
                if not test(pairList):
                    writeToScreen("Please check", "pump/flow sensor")
                    print("There might be a problem with the pump/flow sensor pairs, please ensure they are both connected and function correctly.")
                    time.sleep(2)
                else:
                    passed = True
            else:
                passed = True