from utils.state import State, states
from game.player import Player
from game.dealer import Dealer
from game.action import Action
from agents.monteCarloExploringStarts import MonteCarloExploringStarts
from agents.onPolicyMonteCarlo import OnPolicyMonteCarlo
from agents.qLearning import QLearning
from agents.deterministic import Deterministic
from agents.sarsa import Sarsa


def play(policy, win=1, tie=0, lose=-1): # розыгрыш одной игры (раунда)
    player = Player()
    dealer = Dealer()

    # играем согласно полученной политике, полученной алгоритмом
    state = State(player.sum, player.usable_ace, dealer.sum)
    current_action = policy[state]

    while True:
        if current_action == Action.HIT:
            player.hit()
            if player.sum > 21:
                return lose
                break
            else:
                current_state = State(
                    player.sum, player.usable_ace, dealer.sum)
                current_action = policy[current_state]
        else:
            dealer.play_to_end()
            if dealer.sum > 21 or dealer.sum < player.sum:
                return win
            elif dealer.sum == player.sum:
                return tie
            else:
                return lose
            break


def play_many_times(policy, times=30000):
    times_won = 0
    times_draw = 0
    times_lost = 0
    all = 0
    for i in range(0, times):
        result = play(policy)
        # если result != 0:
        all += 1
        if result == 1:
            times_won += 1
        elif result == 0:
            times_draw += 1
        else:
            times_lost += 1
    return times_won / all * 100, times_draw / all * 100, times_lost / all * 100


def print_differences(first_policy, second_policy, algo):
# различия в политике выбранного алгоритма и детерминированного 
    number = 0
    print()
    print("Различия в политиках", algo, "и детерминированного алгоритма:")
    print()
    for k, v in first_policy.items():
        if second_policy[k] != v:
            number += 1
            print(k)
            print("Действие детерминированного: ", v)
            print("Действие алгоритма ", algo,": ", second_policy[k], sep = '')
            print()

    print("Число различий =", number)
    return number
