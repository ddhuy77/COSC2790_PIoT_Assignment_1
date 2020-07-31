from sense_hat import SenseHat
import time
import random

class electronicDie:

    def dieRoller():
        sense = SenseHat()

        sense.clear()

        r = [255, 0, 0]
        b = [0, 0, 255]
        n = [0, 0, 0]

        one = [
        n,n,n,n,n,n,n,n,
        n,n,n,n,n,n,n,n,
        n,n,n,n,n,n,n,n,
        n,n,n,r,r,n,n,n,
        n,n,n,r,r,n,n,n,
        n,n,n,n,n,n,n,n,
        n,n,n,n,n,n,n,n,
        n,n,n,n,n,n,n,n
        ]

        two = [
        b,b,n,n,n,n,n,n,
        b,b,n,n,n,n,n,n,
        n,n,n,n,n,n,n,n,
        n,n,n,n,n,n,n,n,
        n,n,n,n,n,n,n,n,
        n,n,n,n,n,n,n,n,
        n,n,n,n,n,n,b,b,
        n,n,n,n,n,n,b,b
        ]

        three = [
        b,b,n,n,n,n,n,n,
        b,b,n,n,n,n,n,n,
        n,n,n,n,n,n,n,n,
        n,n,n,b,b,n,n,n,
        n,n,n,b,b,n,n,n,
        n,n,n,n,n,n,n,n,
        n,n,n,n,n,n,b,b,
        n,n,n,n,n,n,b,b
        ]

        four = [
        b,b,n,n,n,n,b,b,
        b,b,n,n,n,n,b,b,
        n,n,n,n,n,n,n,n,
        n,n,n,n,n,n,n,n,
        n,n,n,n,n,n,n,n,
        n,n,n,n,n,n,n,n,
        b,b,n,n,n,n,b,b,
        b,b,n,n,n,n,b,b
        ]

        five = [
        b,b,n,n,n,n,b,b,
        b,b,n,n,n,n,b,b,
        n,n,n,n,n,n,n,n,
        n,n,n,b,b,n,n,n,
        n,n,n,b,b,n,n,n,
        n,n,n,n,n,n,n,n,
        b,b,n,n,n,n,b,b,
        b,b,n,n,n,n,b,b
        ]

        six = [
        b,b,n,n,n,n,b,b,
        b,b,n,n,n,n,b,b,
        n,n,n,n,n,n,n,n,
        b,b,n,n,n,n,b,b,
        b,b,n,n,n,n,b,b,
        n,n,n,n,n,n,n,n,
        b,b,n,n,n,n,b,b,
        b,b,n,n,n,n,b,b
        ]

        die = [one,two,three,four,five,six]

        score=0

        def roll():
            r = random.randint(1,6)
            sense.set_pixels(die[r-1])
            return r
        
        while score==0:
            x, y, z = sense.get_accelerometer_raw().values()

            x = abs(x)
            y = abs(y)
            z = abs(z)

            if x > 1.4 or y > 1.4 or z > 1.4:
                score=roll()
        return score