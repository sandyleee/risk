# import numpy as np
from player import Player
# from territory import Territory
# from troop import Troop
import random
# from enum import Enum

# usa_states = {"A":["B","C"],"B":["A","C"], "C":["B","A"],}
usa_states = {"Alabama":["Mississippi","Tennessee","Florida","Georgia"],
  "Alaska":["Hawaii","California","Arizona"],
  "Arizona":["California","Nevada","Utah","New Mexico","Colorado"],
  "Arkansas":["Tennessee","Missouri","Oklahoma","Mississippi","Louisiana","Texas"],
  "California":["Nevada","Arizona","Alaska"],
  "Colorado":["Utah","Wyoming","Arizona","New Mexico","Nebraska","Kansas","Oklahoma"],
  "Connecticut":["New York","Rhode Island","Massachusetts"],
  "Delaware":["New Jersey","Maryland","Pennsylvania"],
  "Florida":["Alabama","Georgia"],
  "Georgia":["Florida","Alabama","South Carolina","Tennessee","North Carolina"],
  "Hawaii":["Alaska","Texas"],
  "Idaho":["Wyoming","Montana","Washington","Utah","Nevada","Oregon"],
  "Illinois":["Wisconsin","Iowa","Missouri","Indiana","Kentucky"],
  "Indiana":["Illinois","Michigan","Ohio","Kentucky"],
  "Iowa":["Wisconsin","Minnesota","Nebraska","South Dakota","Missouri","Illinois"],
  "Kansas":["Nebraska","Oklahoma","Colorado","Missouri"],
  "Kentucky":["Indiana","Illinois","Virginia","Ohio","West Virginia","Tennessee","Missouri"],
  "Louisiana":["Arkansas","Texas","Mississippi"],
  "Maine":["New Hampshire"],
  "Maryland":["Delaware","Virginia","Pennsylvania","West Virginia"],
  "Massachusetts":["Vermont","New Hampshire","New York","Rhode Island","Connecticut"],
  "Michigan":["Indiana","Ohio","Wisconsin"],
  "Minnesota":["North Dakota","South Dakota","Iowa","Wisconsin"],
  "Mississippi":["Alabama","Arkansas","Louisiana","Tennessee"],
  "Missouri":["Kansas","Arkansas","Iowa","Illinois","Kentucky","Tennessee","Oklahoma"],
  "Montana":["Idaho","Wyoming","North Dakota","South Dakota"],
  "Nebraska":["Iowa","South Dakota","Wyoming","Colorado","Kansas","Missouri"],
  "Nevada":["Idaho","Utah","Arizona","California","Oregon"],
  "New Hampshire":["Maine","Vermont","Massachusetts"],
  "New Jersey":["Delaware","New York","Pennsylvania"],
  "New Mexico":["Oklahoma","Texas","Colorado","Utah","Arizona"],
  "New York":["Vermont","New Jersey","Pennsylvania","Massachusetts","Connecticut"],
  "North Carolina":["South Carolina","Virginia","Tennessee"],
  "North Dakota":["Montana","South Dakota","Minnesota"],
  "Ohio":["West Virginia","Indiana","Michigan","Kentucky","Pennsylvania"],
  "Oklahoma":["Texas","Kansas","Colorado","New Mexico","Arkansas","Missouri"],
  "Oregon":["Idaho","Washington","Nevada","California"],
  "Pennsylvania":["New York","Delaware","New Jersey","Maryland","Ohio","West Virginia"],
  "Rhode Island":["Massachusetts","Connecticut"],
  "South Carolina":["North Carolina","Georgia"],
  "South Dakota":["North Dakota","Wyoming","Montana","Nebraska","Iowa","Minnesota"],
  "Tennessee":["North Carolina","Alabama","Mississippi","Georgia","Arkansas","Kentucky","Missouri"],
  "Texas":["New Mexico","Oklahoma","Arkansas","Louisiana","Hawaii"],
  "Utah":["Idaho","Nevada","Wyoming","Nevada","Colorado","New Mexico"],
  "Vermont":["New York","New Hampshire","Massachusetts"],
  "Virginia":["West Virginia","Maryland","North Carolina","Kentucky"],
  "Washington":["Oregon","Idaho"],
  "West Virginia":["Ohio","Virginia","Pennsylvania","Kentucky","Maryland"],
  "Wisconsin":["Michigan","Minnesota","Illinois","Iowa"],
  "Wyoming":["Montana","Idaho","Nebraska","Utah","Colorado","South Dakota"]}

class Game:

    def __init__(self, map, players_num = 2 ,player_turn=0):
        self.map = map
        self.game_over = None
        self.player_turn = player_turn
        self.players_num = players_num

    def generate_players(self):
        self.players = []
        for i in range(0,self.players_num):
            self.players.append(Player(i,self))
    
    def generate_troops(self):
        self.troops = {}
        check = False
        old_player = None
        for i in usa_states.keys():
            player = random.randint(0,1)
            if old_player and old_player != player:
                check = True
            self.troops[i] = [0,player]
            old_player = player
            
        if check == False:#if all countries got belonge to one player, run again
            self.generate_troops()
        

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