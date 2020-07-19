from sense_hat import SenseHat
import time
import random

class electronicDie:
    def dieRoller():
        sense = SenseHat()

        sense.clear()

        # sense.show_message("Shake to roll!")

        b = [0, 0, 0]
        g = [0, 255, 0]
        r = [255, 0, 0]

        one = [
        b,b,b,b,b,b,b,b,
        b,b,b,b,b,b,b,b,
        b,b,b,b,b,b,b,b,
        b,b,b,g,g,b,b,b,
        b,b,b,g,g,b,b,b,
        b,b,b,b,b,b,b,b,
        b,b,b,b,b,b,b,b,
        b,b,b,b,b,b,b,b,
        ]

        two = [
        b,b,b,b,b,b,b,b,
        b,g,g,b,b,b,b,b,
        b,g,g,b,b,b,b,b,
        b,b,b,b,b,b,b,b,
        b,b,b,b,b,b,b,b,
        b,b,b,b,g,g,b,b,
        b,b,b,b,g,g,b,b,
        b,b,b,b,b,b,b,b,
        ]

        three = [
        g,g,b,b,b,b,b,b,
        g,g,b,b,b,b,b,b,
        b,b,b,b,b,b,b,b,
        b,b,b,g,g,b,b,b,
        b,b,b,g,g,b,b,b,
        b,b,b,b,b,b,b,b,
        b,b,b,b,b,b,g,g,
        b,b,b,b,b,b,g,g,
        ]

        four = [
        b,b,b,b,b,b,b,b,
        b,g,g,b,b,g,g,b,
        b,g,g,b,b,g,g,b,
        b,b,b,b,b,b,b,b,
        b,b,b,b,b,b,b,b,
        b,g,g,b,b,g,g,b,
        b,g,g,b,b,g,g,b,
        b,b,b,b,b,b,b,b,
        ]

        five = [
        g,g,b,b,b,b,g,g,
        g,g,b,b,b,b,g,g,
        b,b,b,b,b,b,b,b,
        b,b,b,g,g,b,b,b,
        b,b,b,g,g,b,b,b,
        b,b,b,b,b,b,b,b,
        g,g,b,b,b,b,g,g,
        g,g,b,b,b,b,g,g,
        ]

        six = [
        r,r,b,b,b,b,r,r,
        r,r,b,b,b,b,r,r,
        b,b,b,b,b,b,b,b,
        r,r,b,b,b,b,r,r,
        r,r,b,b,b,b,r,r,
        b,b,b,b,b,b,b,b,
        r,r,b,b,b,b,r,r,
        r,r,b,b,b,b,r,r,
        ]

        score=0

        def roll_dice():
            r = random.randint(1,6)
            if r == 1:
                sense.set_pixels(one)
            elif r == 2:
                sense.set_pixels(two)
            elif r == 3:
                sense.set_pixels(three)
            elif r == 4:
                sense.set_pixels(four)
            elif r == 5:
                sense.set_pixels(five)
            elif r == 6:
                sense.set_pixels(six)
            return r
        
        while score==0:
            x, y, z = sense.get_accelerometer_raw().values()

            x = abs(x)
            y = abs(y)
            z = abs(z)

            if x > 1.4 or y > 1.4 or z > 1.4:
                score=roll_dice()
                #time.sleep(1)
        return score

# e1=electronicDie
# x=e1.dieRoller()
# print(x)