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
        self.flowSensor.irq(trigger = Pin.IRQ_RISING, handler = self.countPulse) #interrupt handler
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
    """Function that switches on the pumps with a 0.5 s time delay so that the power supply doesn't get overloaded"""
    from main import pairList
    for pair in pairList:
        pair.pumpOn()
        time.sleep(0.5)

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

def slowPumps(pair: pumpSensorPairs, percentFilled: int, percentToStartSlowing: int) -> None:
    """Function that slows the pump(s) ater the bottle is (percentToStartSlowing)% full"""
    speed = int(65000-(25000*((percentFilled - percentToStartSlowing)/(100-percentToStartSlowing)))) #slow down the pump(s) as the bottle fills
    pair.mosfet.duty_u16(speed)

def checkIfDone() -> None:
    """Function that runs the pump(s) and stops when the flow sensor(s) has reached the desired ml amount"""
    from main import ml, pairList, percentToStartSlowing
    global session_fill_count
    global total_fill_count
    done = 0
    resetValues()
    pumpsOn()
    while done<len(pairList) and button.value() == 0:
        for pair in pairList:
            if not pair.done:
                percentFilled = round((pair.count/4/ml)*100)
                if percentFilled > percentToStartSlowing: #if the bottle is more than (percentToStartSlowing)% filled, then it will start slowing down the pump(s)
                    slowPumps(pair, percentFilled, percentToStartSlowing)
                writeToScreen("Filling... " + str(percentFilled) + "%", "")
                if pair.count/4 >= ml:
                    pair.pumpOff()
                    pair.done = True
                    done += 1
                    writeToScreen("", "Filled {}/{}".format(str(done), len(pairList)))
                    session_fill_count+=1
                    total_fill_count+=1
                    writeToLog()
    if done>=len(pairList):
        time.sleep(1) #give user enough time to read the display if all the bottles were filled
    pumpsOff()

def resetValues() -> None:
        """Function that switches the pump(s) off and resets the values of count and done"""
        from main import pairList
        for pair in pairList:
            pair.count = 0
            pair.done = False