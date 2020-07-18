from sense_hat import SenseHat
from time import sleep

class Emoji:
   def __init__(self, y, b, r):
      self.y = y
      self.b = b
      self.r = r
   def animateEmoji(self):
      sense = SenseHat()
      y = self.y
      b = self.b
      r = self.r
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

y = (255, 255, 0) # Yellow
b = (0, 0, 255) # Blue
r = (255, 0, 0) # Red

e1 = Emoji(y, b, r)
e1.animateEmoji()







