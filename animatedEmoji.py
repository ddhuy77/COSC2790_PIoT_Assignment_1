from sense_hat import SenseHat
from time import sleep
from emojis.smile import Smile
from emojis.frown import Frown
from emojis.neutral import Neutral

class AnimatedEmoji:
    
    def __init__(self, color1, color2, color3):
        self.__color1 = color1
        self.__color2 = color2
        self.__color3 = color3

    def aEmoji(self):
        sense = SenseHat()

        color1 = self.__color1
        color2 = self.__color2
        color3 = self.__color3

        emojis = [
            Smile(color1),
            Neutral(color2),
            Frown(color3)
        ]

        while True:
            for emoji in emojis:
                sense.set_pixels(emoji.face())
                sleep(3)

r = (255, 0, 0)
y = (255, 255, 0)
g = (0, 255, 0)

e1 = AnimatedEmoji(g, y, r)
e1.aEmoji() 