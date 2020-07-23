from sense_hat import SenseHat
from time import sleep
from emojis.smile import Smile
from emojis.frown import Frown
from emojis.neutral import Neutral

class AnimatedEmoji:
    def animatedEmoji():
        red = (255, 0, 0)
        yellow = (255, 255, 0)
        green = (0, 255, 0)

        emojis = [
            Smile(green),
            Neutral(yellow),
            Frown(red)
        ]

    while True:
        for emoji in emojis:
            sense.set_pixels(emoji.face())
            sleep(3)

AnimatedEmoji.animatedEmoji()