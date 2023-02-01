import time
from pumpManager import counter, resetValues
from buttonManager import button, releaseButton
from lcdManager import writeToScreen, displayConnected

def test(pairList: list) -> bool:
    """Function that runs the pump(s) and stops when the flow sensor(s) has reached the desired ml amount"""
    done = 0
    start = time.time()
    writeToScreen("Testing...", "Tested: 0/" + str(len(pairList)))
    while done<len(pairList) and button.value() == 0 and time.time()-start < 10:
        for pair in pairList:
            if not pair.done:
                result = counter(pair.flowSensor, pair.count, pair.state)
                pair.count = result[0]
                pair.pumpOn()
                if result[0]/4 >= 10: #checks if 10ml have been passed through the flow sensor(s)
                    pair.pumpOff()
                    pair.done = True
                    done += 1
                    writeToScreen("", "Tested {}/{}".format(str(done), len(pairList)))
                pair.state = result[1]
    resetValues()
    return done>=len(pairList)

def askForTest(start: int) -> bool:
    while button.value() == 1 and time.time()-start < 3:
        time.sleep(0.1)
        writeToScreen("Hold {} s to".format(3-(time.time()-start)), "start testing")
    if time.time()-start >= 3:
        releaseButton()
        return True
    else:
        return False

def runTest():
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