from random import randint
from .card import Card

class Player:
    sum = 0
    usable_ace = False

    def __init__(self):
        while self.sum < 12:
            self.hit()

    def hit(self):
        """Беру одну карту

        Возвращает:
            int -- сумму руки после взятия карты
        """
        c = Card().value
        if c == 11 and self.sum >= 11:
            self.sum += 1
        else:
            if c == 11 and self.sum < 11:
                self.usable_ace = True
            self.sum += c
            if self.sum > 21 and self.usable_ace:
                self.usable_ace = False
                self.sum -= 10
        return self.sum
