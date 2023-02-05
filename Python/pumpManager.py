import time
from machine import PWM, Pin
from lcdManager import writeToScreen, display
from buttonManager import releaseButton, button

session_fill_count = 0

#opens logs.txt to be able to read the total number of times filled
log = open("logs.txt", "r")
total_fill_count = int(log.read())
log.close()

class pumpSensorPairs:

    """Class that defines the pump and flow sensor pairs and manages them"""

    def __init__(self, mosfet: int, flowSensor: int, count: int = 0, done: bool = False) -> None:
        """Function that initialises class variables"""
        #initialise mosfet variables
        self.mosfet = PWM(Pin(mosfet))
        self.mosfet.freq(100000) #sets the mosfet frequency to 100k hz
        self.mosfetPin = mosfet
        #initialise flow sensor variables
        self.flowSensor = Pin(flowSensor, Pin.IN, Pin.PULL_UP)
        self.flowSensorPin = flowSensor
        #initialise other variables
        self.count = count
        self.done = done

    def pumpOn(self) -> None:
        """Switch pump on"""
        self.mosfet.duty_u16(65535)

    def pumpOff(self) -> None:
        """Switch pump off"""
        self.mosfet.duty_u16(0)

    def countPulse(self, none:None = None) -> None:
        """Function that counts the amount of times the flow sensor(s) trigger(s) using an interrupt handler"""
        self.count += 1

    def __str__(self) -> str:
        """Returns the pump and flow sensor pins"""
        return "This pump is on pin {} and has a flow sensor on pin {}.".format(self.mosfetPin, self.flowSensorPin)

def pumpsOn() -> None:
    """Function that switches on the pumps with a 0.1 s time delay so that the power supply doesn't get overloaded"""
    from main import pairList
    for pair in pairList:
        pair.pumpOn()
        time.sleep(0.1)

def pumpsOff() -> None:
    """Function that switches off the pumps"""
    from main import pairList
    for pair in pairList:
        pair.pumpOff()

def runPumps(start: int) -> None:
    """Function that runs the pump(s) for an indefinite amount of time and dispays the run time on the screen"""
    pumpsOn()
    writeToScreen("Clearing...", "Run time:")
    while button.value() == 0:
        writeToScreen("", "Run time: {}".format(time.time()-(start)) + "s")
    pumpsOff()
    releaseButton()
    display()

def writeToLog() -> None:
    """Function that writes the total number of fills to logs.txt"""
    log = open("logs.txt", "w")
    log.write(str(total_fill_count))
    log.close()

def logClose() -> None:
    """Function that closes logs.txt when stopping program incase that it is open"""
    log.close()

def slowPumps(pair: pumpSensorPairs, percentFilled: int) -> None:
    """Function that slows the pump(s) ater the bottle is 75% full"""
    speed = int(65000-(25000*((percentFilled - 75)/25))) #slow down the pump(s) as the bottle fills
    print(speed)
    pair.mosfet.duty_u16(speed)

def checkIfDone() -> None:
    """Function that runs the pump(s) and stops when the flow sensor(s) has reached the desired ml amount"""
    from main import ml, pairList
    global session_fill_count
    global total_fill_count
    done = 0
    pumpsOn()
    while done<len(pairList) and button.value() == 0:
        for pair in pairList:
            pair.flowSensor.irq(trigger = Pin.IRQ_RISING, handler = pair.countPulse) #activate interrupt handler
            if not pair.done:
                percentFilled = round((pair.count/4/ml)*100)
                if percentFilled > 75: #if the bottle is more than 75% filled, then it will start slowing down the pump(s)
                    slowPumps(pair, percentFilled)
                writeToScreen("Filling... " + str(percentFilled) + "%", "")
                if pair.count/4 >= ml:
                    pair.pumpOff()
                    pair.done = True
                    done += 1
                    writeToScreen("", "Filled {}/{}".format(str(done), len(pairList)))
                    session_fill_count+=1
                    total_fill_count+=1
                    writeToLog()
    for pair in pairList:
        pair.flowSensor.irq(trigger = Pin.IRQ_RISING, handler = None) # type: ignore #deactivate interrupt handler

def resetValues() -> None:
        """Function that switches the pump(s) off and resets the values of count and done"""
        from main import pairList
        for pair in pairList:
            pair.pumpOff()
            pair.count = 0
            pair.done = False