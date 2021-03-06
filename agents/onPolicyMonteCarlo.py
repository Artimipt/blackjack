from game.dealer import Dealer
from game.player import Player
import numpy as np
from statistics import mean
from utils.state import State, states
from .agent import Agent
from game.action import Action
import random


class OnPolicyMonteCarlo(Agent):
    policy = {k: {} for k in states}
    returns = {(k, a): [] for k in states for a in list(Action)}
    Q = {k: {} for k in states}

    DELTA = 0.05
    TIMES_TESTED_SAME_STATE = 1000


    def __init__(self, epsilon=0.2, improve = True,  *_, **__):
        self.IMPROVE = improve
        self.EPSILON = epsilon

        for k in states:
            last = 1
            for a in list(Action):
                self.Q[k][a] = 0
                self.policy[k][a] = random.random() if last == 1 else 1 - last
                last = self.policy[k][a]

    def get_best_action(self, state):
        return max(self.Q[state], key=self.Q[state].get)

    def calculate(self, number=10000):
        """Оценка серии эпизодов

        Основные аргументы:
            number {int} -- количество оцениваемых эпизодов (по умолчанию: {1000000})

        Возвращает:
            Dictionary -- сформированную (определенную, оцененную) политику
	"""
	
        for i in range(0, number):
            self.estimate_one()

        if self.IMPROVE:
            for k, v in self.Q.items():
                if abs(v[Action.HIT] - v[Action.STAND]) < self.DELTA:
                    for i in range(0, self.TIMES_TESTED_SAME_STATE):
                        self.estimate_one(k)


        return_policy = {}
        for state in self.policy.keys():
            best_action = self.get_best_action(state)
            return_policy[state] = best_action

        return return_policy

    def estimate_one(self, starting_state = None):
        episode, reward = self.generate_episode()
        for state, action in episode:
            self.returns[(state, action)].append(reward)
            self.Q[state][action] = mean(self.returns[(state, action)])

        for state, _ in episode:
            best_action = self.get_best_action(state)
            for action in list(Action):
                if action == best_action:
                    self.policy[state][action] = 1 - \
                        self.EPSILON + (self.EPSILON / len(list(Action)))
                else:
                    self.policy[state][action] = self.EPSILON / \
                        len(list(Action))

    def get_action(self, state):
        action_with_probabilities = self.policy[state]
        actions = list(action_with_probabilities.keys())
        probabilities = list(action_with_probabilities.values())

        current_action = np.random.choice(a=actions, size=1, p=probabilities)
        return current_action[0]

    def generate_episode(self, starting_state = None):
        """Создается один эпизод согласно определнной политике

        Функция возвращает:
            list(state, action) -- список пар <состояние, действие> 
            int -- награду (1 или 0)
        """
        
        player = Player()
        dealer = Dealer()
        current_state = starting_state if starting_state is not None else random.choice(
            states)
        current_action = self.get_action(current_state)

        player.sum = current_state.player_sum
        player.usable_ace = current_state.player_usable_ace
        dealer.sum = current_state.dealer_card

        episode = [(current_state, current_action)]
        reward = 0

        while True:
            if current_action == Action.HIT:
                player.hit()
                if player.sum > 21:
                    reward = -1
                    break
                else:
                    current_state = State(
                        player.sum, player.usable_ace, dealer.sum)
                    current_action = self.get_action(current_state)
                    episode.append((current_state, current_action))
            else:
                dealer.play_to_end()
                if dealer.sum > 21 or dealer.sum < player.sum:
                    reward = 1
                elif dealer.sum == player.sum:
                    reward = 0
                else:
                    reward = -1
                break

        return episode, reward
