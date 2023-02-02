# Kajimba Pump

## Installation

---

1. Install [MicroPython](https://micropython.org/) on the **Raspberry Pi Pico**: [*Instructions*](https://www.raspberrypi.com/documentation/microcontrollers/micropython.html)
2. Install all [python files](https://github.com/Yael-A10/Kajimba/tree/main/Python) from the `Python` folder onto the **Raspberry Pi Pico**.

## User guide

---

1. In the `main.py` file, change/add `mosfet` and `flowSensor` pins depending on how many pump/flowSensor pairs you have. These are the default pins:

    ```python![image](https://user-images.githubusercontent.com/112374055/216338277-969c9c25-4de8-40c9-8e30-9a85490654c8.png)

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

3. Change the `ml` value to the value needed, this is the default value:

    ```python
    #variables
    ml = 285
    ```

Once the **Raspberry Pi Pico** is plugged in it will automatically run `main.py`. If the display is connected it will:

- Ask the user if they want to run a test (which will run the **pump(s)** for 10 seconds and test if the **flow sensor(s)** gets any output)

    - If you want to run the test, hold down the button for 3 seconds.
    - If not, press the button once and it will skip the test.

If the display is not connected, it will skip this test and move on directly to the next part:

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