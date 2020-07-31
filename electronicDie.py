from sense_hat import SenseHat
import time
import random

class electronicDie:

    def dieRoller():
        sense = SenseHat()

        sense.clear()

        b = [0, 0, 0]
        w = [255,255,255]

        one = [
        w,w,w,w,w,w,w,w,
        w,w,w,w,w,w,w,w,
        w,w,w,w,w,w,w,w,
        w,w,w,b,b,w,w,w,
        w,w,w,b,b,w,w,w,
        w,w,w,w,w,w,w,w,
        w,w,w,w,w,w,w,w,
        w,w,w,w,w,w,w,w
        ]

        two = [
        b,b,w,w,w,w,w,w,
        b,b,w,w,w,w,w,w,
        w,w,w,w,w,w,w,w,
        w,w,w,w,w,w,w,w,
        w,w,w,w,w,w,w,w,
        w,w,w,w,w,w,w,w,
        w,w,w,w,w,w,b,b,
        w,w,w,w,w,w,b,b
        ]

        three = [
        b,b,w,w,w,w,w,w,
        b,b,w,w,w,w,w,w,
        w,w,w,w,w,w,w,w,
        w,w,w,b,b,w,w,w,
        w,w,w,b,b,w,w,w,
        w,w,w,w,w,w,w,w,
        w,w,w,w,w,w,b,b,
        w,w,w,w,w,w,b,b
        ]

        four = [
        b,b,w,w,w,w,b,b,
        b,b,w,w,w,w,b,b,
        w,w,w,w,w,w,w,w,
        w,w,w,w,w,w,w,w,
        w,w,w,w,w,w,w,w,
        w,w,w,w,w,w,w,w,
        b,b,w,w,w,w,b,b,
        b,b,w,w,w,w,b,b,
        ]

        five = [
        b,b,w,w,w,w,b,b,
        b,b,w,w,w,w,b,b,
        w,w,w,w,w,w,w,w,
        w,w,w,b,b,w,w,w,
        w,w,w,b,b,w,w,w,
        w,w,w,w,w,w,w,w,
        b,b,w,w,w,w,b,b,
        b,b,w,w,w,w,b,b,
        ]

        six = [
        b,b,w,w,w,w,b,b,
        b,b,w,w,w,w,b,b,
        w,w,w,w,w,w,w,w,
        b,b,w,w,w,w,b,b,
        b,b,w,w,w,w,b,b,
        w,w,w,w,w,w,w,w,
        b,b,w,w,w,w,b,b,
        b,b,w,w,w,w,b,b,
        ]

        die = [one,two,three,four,five,six]

        score=0

        def roll_dice():
            r = random.randint(1,6)
            sense.set_pixels(die[r-1])
            return r
        
        while score==0:
            x, y, z = sense.get_accelerometer_raw().values()

            x = abs(x)
            y = abs(y)
            z = abs(z)

            if x > 1.4 or y > 1.4 or z > 1.4:
                score=roll_dice()
        return score