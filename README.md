# Kajimba Pump

## Installation

---

1. Install [MicroPython](https://micropython.org/) on the **Raspberry Pi Pico**: [*Instructions*](https://www.raspberrypi.com/documentation/microcontrollers/micropython.html)
2. Move all the python files from the [`Python` folder](https://github.com/Yael-A10/Kajimba/tree/main/Python) onto the **Raspberry Pi Pico**, including the `logs.txt` file. To do this:
    - Install [Thonny](https://thonny.org/)
    - Once it's installed open it and plug in the **Raspberry Pi Pico** to your computer
    - Select `Raspberry Pi Pico` as your device in the bottom right corner of the [Thonny](https://thonny.org/) software.
    - Next click `file>open` and select `This computer` as the device to open from. Then open all the files you want to upload to the **Raspberry Pi Pico**.
    - For each file click `file>Save as...` and select `Raspberry Pi Pico` as the device to save to.

If all was done correctly the program should start running as soon as the **Raspberry Pi Pico** is powered.

## User guide

---

1. In the `main.py` file, change/add `mosfet` and `flowSensor` pins depending on how many pump/flowSensor pairs you have. These are the default pins:

    ```python
    #define the pump and flow sensor pins:
    mosfet1 = 19
    flowSensor1 = 8
    ```

2. If you added more pump/flowSensor pairs, create a new `pair` variable with your new `mosfet` and `flowSensor` pins and add it to `pairList`. This is the default pair:

    ```python
    #create the pump and flow sensor pairs:
    pair1 = pumpSensorPairs(mosfet1, flowSensor1)

    #add the pairs into the pair list
    pairList = [pair1]
    ```

3. Change the `ml1` and `ml2` values depending on the values needed, these are the default values:

    ```python
    #variables
    ml1 = 285
    ml2 = 300
    ```

4. Change the `percentToStartSlowing` value to a value between 0 and 90. This variable represents the percentage of the bottle that is filled and the pump(s) will start slowing down after that percent is reached. This is the default value:

    ```python
    percentToStartSlowing = 75 #variable set between 0 and 90 that controls when the pump(s) start slowing down
    ```

Once the **Raspberry Pi Pico** is powered it will automatically run `main.py`. If the display is connected it will:

- Ask the user if they want to run a test (which will run the **pump(s)** for 10 seconds and test if the **flow sensor(s)** gets any output (10 ml))

    - If you want to run the test, hold down the button for 3 seconds.
    - If not, press the button once and it will skip the test.

If the display is not connected, it will skip this test and move on directly to the next part:

- To choose between the preset `ml1` and `ml2` amounts to fill:
    - Press the button once to choose `ml1`
    - Hold down the button for 3 seconds to choose `ml2`
- To run the pump(s) you have two options:
    - To run the pump(s) indefinately hold down the button for 3 seconds. Press it again to stop.
    - To run the pump(s) for the set amount of `ml`, press the button once. The pump(s) will slow down incrementally as the bottle gets filled.

    > Note that you can press the button again at anytime to make the pump(s) stop running.

When the display is connected, it will display the amount of times a bottle was filled during the session (top value) and the total amount of times a bottle was filled (bottom value):

```
Filled: ()
Total: ()
```

The total amount of times a bottle was filled is stored on `logs.txt`, you can edit this value if you want to edit/reset the total amount of bottles filled.

## KiCad

---

Here is the unpopulated **PCB**:
![Unpopulated PCB Image](/KiCad/Images/unpopulatedPCB.png)
Here is the populated **PCB**:
![Populated PCB Image](/KiCad/Images/populatedPCB.png)