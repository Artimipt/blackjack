class State:
    player_sum = 0  # между 12 и 21
    player_usable_ace = False

    dealer_card = 0  # между 2 и 11

    def __init__(self, player_sum, player_usable_ace, dealer_card):
        """Инициализация состояния

        Arguments:
            player_sum {int} -- сумма руки игрока
            player_usable_ace {bool} -- есть или нет у игрока полезный туз 
            dealer_card {int} -- значение карты дилера (11 если туз)
        """
        self.player_sum = player_sum
        self.player_usable_ace = player_usable_ace
        self.dealer_card = dealer_card

    def __eq__(self, other):
        return (self.player_sum, self.player_usable_ace, self.dealer_card) == (other.player_sum, other.player_usable_ace, other.dealer_card)

    def __hash__(self):
        return hash((self.player_sum, self.player_usable_ace, self.dealer_card))

    def __ne__(self, other):
        return not(self == other)

    def __repr__(self):
        return f"{self.dealer_card} {self.player_sum} {self.player_usable_ace}"


states = []

for player_usable_ace in [False, True]:
    for player_sum in range(12, 22):
        for dealer_card in range(2, 12):
            states.append(State(player_sum, player_usable_ace, dealer_card))
