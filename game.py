# import numpy as np
from player import Player
# from territory import Territory
# from troop import Troop
import random
# from enum import Enum

usa_states = {"A":["B","C"],"B":["A","C"], "C":["B","A"],}

#starting troop: country:(number of troops, player)
starting_troops = {"A":[5,1],"B":[8,1],"C":[1,0]}

class Game:

    def __init__(self, map, starting_troops, players_num = 2 ,player_turn=0):
        self.map = map
        self.troops = starting_troops
        self.game_over = None
        self.player_turn = player_turn
        self.players_num = players_num

    def generate_players(self):
        self.players = []
        for i in range(0,self.players_num):
            # type = self.player_types[i]
            self.players.append(Player(i))

    def get_countries(self,player):
        countries = []
        for country in self.troops.keys():
            if self.troops[country][1] == player:
                countries.append(country)
        return countries

    def assignment(self,num_assignments, player):
        countries = self.get_countries(player)
        for i in range(num_assignments):
            country = random.choice(countries)
            self.troops[country][0] += 1

    def check_end_state(self):
        if len(self.get_countries(1)) == 0 or len(self.get_countries(0))==0:
            return True
        else:
            return False

    def check_winner(self):
        if self.check_end_state()==True:
            if len(self.get_countries(1)) == 0:
                print('Game is over and player 0 won!')
                return 0
            else:
                print('Game is over and player 1 won!')
                return 1
        else:
            raise('game has not been finished')