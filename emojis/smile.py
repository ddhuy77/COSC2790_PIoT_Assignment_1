from emojis.emoji import Emoji

class Smile(Emoji):
    def __innit__(self, color)
        super().__innit__(color)

    def face(self):
        c = self.getColor()
        b = (0, 0, 0)
        faceArr = [
            c, c, c, c, c, c, c, c,
            c, b, b, c, c, b, b, c,
            c, b, b, c, c, b, b, c,
            c, c, c, c, c, c, c, c,
            c, b, b, c, c, b, b, c,
            c, b, b, b, b, b, b, c,
            c, c, b, b, b, b, c, c,
            c, c, c, c, c, c, c, c
        ]
        return faceArr