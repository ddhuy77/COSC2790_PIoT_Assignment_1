from sense_hat import SenseHat
from time import sleep

sense = SenseHat()

y = (255, 255, 0) # Yellow
b = (0, 0, 255) # Blue
r = (255, 0, 0) # Red

smile = [
   y, y, y, y, y, y, y, y,
   y, y, r, y, y, r, y, y,
   y, y, r, y, y, r, y, y,
   y, y, r, y, y, r, y, y,
   y, y, y, y, y, y, y, y,
   y, b, y, y, y, y, b, y,
   y, b, b, b, b, b, b, y,
   y, y, y, y, y, y, y, y
]

frown = [
   y, y, y, y, y, y, y, y,
   y, y, r, y, y, r, y, y,
   y, y, r, y, y, r, y, y,
   y, y, r, y, y, r, y, y,
   y, y, y, y, y, y, y, y,
   y, b, b, b, b, b, b, y,
   y, b, y, y, y, y, b, y,
   y, y, y, y, y, y, y, y
]

surprised = [
   y, r, r, y, y, r, r, y,
   y, r, r, y, y, r, r, y,
   y, r, r, y, y, r, r, y,
   y, y, y, y, y, y, y, y,
   y, y, b, b, b, b, y, y,
   y, y, b, y, y, b, y, y,
   y, y, b, y, y, b, y, y,
   y, y, b, b, b, b, y, y
]

while True:
   sense.set_pixels(smile)
   sleep(3)
   sense.set_pixels(frown)
   sleep(3)
   sense.set_pixels(surprised)
   sleep(3)