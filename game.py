# import numpy as np
# from player import Player
# from territory import Territory
# from troop import Troop
# import random
# from enum import Enum

starting_troops = 25
usa_states = {"A":["B","C"],"B":["A","C"], "C":["B","A"],}

#starting troop: country:(number of troops, player)
starting_troops = {"A":[5,1],"B":[8,1],"C":[1,0]}

class Game:

    def __init__(self, map, starting_troops ,player_turn=0):
        self.map = map
        self.troops = starting_troops
        self.game_over = None
        self.player_turn = player_turn

    def get_countries(self,player):
        countries = []
        for country in self.troops.keys():
            if self.troops[country][1] == player:
                countries.append(country)
        return countries

    def assignment(self,num_assignments, player):
        return 0