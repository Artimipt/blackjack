from random import randint


class Card:

    """
    	Создание карты и сохранение ее числового значения
    """
    
    value = 0

    def __init__(self):
        number = randint(1, 13)
        if number == 1:
            self.value = 11
        elif number > 10:
            self.value = 10
        else:
            self.value = number
