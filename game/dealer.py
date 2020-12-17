from .card import Card


class Dealer:
    sum = 0
    usable_ace = False

    def __init__(self):
        self.take_card()

    def take_card(self):
        """функция взятия одной карты

        Возвращает:
            int -- числовое значение (ценность) карты
        """
        c = Card().value
        if c == 11:
            self.usable_ace = True
        self.sum += c
        return c

    def play_to_end(self):
        """Играем пока сумма очков у дилера < 17

        Возвращает:
            int -- сумму очков дилера после игры
        """
        while (self.sum < 17):
            self.take_card()
            if self.sum > 21 and self.usable_ace:
                self.usable_ace = False
                self.sum -= 10
        return self.sum
