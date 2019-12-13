import numpy as np
from player import Player
# from territory import Territory
# from troop import Troop
import random
# from enum import Enum

usa_states = {"Alabama":["Mississippi","Tennessee","Florida","Georgia"],
  "Alaska":["Hawaii","California"],
  "Arizona":["California","Nevada","New Mexico","Colorado"],
  "Arkansas":["Tennessee","Missouri","Oklahoma","Mississippi","Louisiana","Texas"],
  "California":["Nevada","Arizona","Alaska","Oregon"],
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
  "Missouri":["Kansas","Arkansas","Iowa","Illinois","Kentucky","Tennessee","Oklahoma","Nebraska"],
  "Montana":["Idaho","Wyoming","North Dakota","South Dakota"],
  "Nebraska":["Iowa","South Dakota","Wyoming","Colorado","Kansas","Missouri"],
  "Nevada":["Idaho","Utah","Arizona","California","Oregon"],
  "New Hampshire":["Maine","Vermont","Massachusetts"],
  "New Jersey":["Delaware","New York","Pennsylvania"],
  "New Mexico":["Oklahoma","Texas","Colorado","Utah","Arizona"],
  "New York":["Vermont","New Jersey","Pennsylvania","Massachusetts","Connecticut"],
  "North Carolina":["South Carolina","Virginia","Tennessee","Georgia"],
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
usa_states = {"A":["B","C","Z"],"B":["A","C"], "C":["B","A","D"],"D":["C"],"Z":["A","Y"],
              "Y":["Z"]}
# usa_states = {"A":["B","C","Z","D","Y"],"B":["A","C","Z","D","Y"], "C":["B","A","D","Y","Z"],
#               "D":["B","A","C","Y","Z"],"Z":["B","A","C","D","Y"], "Y":["B","A","C","D","Z"]}



class Game:

    def __init__(self, map, players_num = 2 ,player_turn=0):
        self.map = map
        self.game_over = None
        self.player_turn = player_turn
        self.players_num = players_num
        self.phi = {}
        self.w = {}
        self.phase = None
        self.eta = 0.001
        self.gama = 0.9

    def generate_players(self):
        self.players = []
        for i in range(0,self.players_num):
            self.players.append(Player(i,self))
    
    def generate_troops(self): #{1:[2,1],2:[5,1], 3:[3,1], 4:[10,0]}
        self.troops = {}
        check = False
        old_player = None
        for i in usa_states.keys():
            player = random.randint(0,1)
            if old_player and old_player != player:
                check = True
            self.troops[i] = [1,player]
            old_player = player
            
        if check == False:#if all countries got belonge to one player, run again
            self.generate_troops()
        

    def get_countries(self,player):
        countries = []
        for country in self.troops.keys():

            # print('hhhhey',self.troops[country])
            if self.troops[country][1] == player:
                countries.append(country)
        return countries


    def reinforce(self, country):
        self.troops[country] += 1

    #random reinforce
    def random_reinforce(self, num_assignments, player):
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
                # print('Game is over and player 0 won!')
                return 0
            else:
                # print('Game is over and player 1 won!')
                return 1
        else:
            raise('game has not been finished')
    
    def get_counties(self, playerID):
        countries = []
        for country in self.troops:
            if self.troops[country][1] == playerID:
                countries.append(country)
        return countries

    def country_count(self, playerID):
        return len(self.get_counties(playerID))
    
    def get_neighbor_enemies(self,country):
        enemy_neghbor = []
        counyry_owner_id = self.troops[country][1]
        for neighbor in self.map[country]:
            if self.troops[neighbor][1] != counyry_owner_id:
                enemy_neghbor.append(neighbor)
        return enemy_neghbor

    def get_neighbor_friends(self,country):
        friend_neighbor = []
        # print('country',country)
        # print('self.troops[country][1]',self.troops[country][1])
        counyry_owner_id = self.troops[country][1]
        for neighbor in self.map[country]:
            if self.troops[neighbor][1] == counyry_owner_id:
                friend_neighbor.append(neighbor)
        return friend_neighbor

    def get_toops_num(self, list_of_countries):
        counter = 0
        for country in list_of_countries:
            counter += self.troops[country][0]
        return counter

    def get_all_troops(self,player_ID):
        counter = 0
        for country in self.troops.keys():
            if self.troops[country][1] == player_ID:
                counter += self.troops[country][0]
        return counter

    def DFSUtil(self, temp, v, visited):
        #Mark the current vertex as visited
        visited[v] = True

        #Store the vertex to the list
        temp.append(v)

        #Repeat for all vetices adjacent to this vertex v
        # print('v',v)
        # print('self.get_neighbor_friends(v)',self.get_neighbor_friends(v))
        for v in self.get_neighbor_friends(v):
            if visited[v] == False:
                temp = self.DFSUtil(temp, v , visited)
        return temp

    def connectedComponents(self, player_ID):
        visited = {}
        cc= []
        friend_countries = self.get_counties(player_ID)
        # print('fffriend countries',friend_countries)
        for v in friend_countries:
            visited[v] = False
        # print(visited)
        for v in friend_countries:
            if visited[v] == False:
                temp = []
                cc.append(self.DFSUtil(temp, v, visited))
        return cc




    #this evaluation is for player 1 which we are going to maximize its utility
    def sum_neighbor_enemy_troops(self, country):
        enemy_neighbors = self.get_neighbor_enemies(country)
        enemy_troops = self.get_toops_num(enemy_neighbors)
        return enemy_troops

    def get_bsr(self, country):
        enemy_troops = self.sum_neighbor_enemy_troops(country)
        bsr = (enemy_troops / float(self.troops[country][0]))
        return bsr


    def get_eval(self):
        sum_BSR = 0
        for country in self.get_counties(1):
            sum_BSR += self.get_bsr(country)
        for country in self.get_counties(0):
            sum_BSR -= self.get_bsr(country)
        return -sum_BSR
    def change_player(self):
        self.player_turn = 1- self.player_turn

    def check_troops(self):
        for troop in self.troops.keys():
            # print('trooooops',troops)
            if self.troops[troop][0] <1:
                return False
        return True

# ######################################################################################################################
# #TD learning
    def initialize_phi(self):

        for country in self.troops.keys():
            self.phi[('troops in'+str(country),self.troops[country][1])] = self.troops[country][0]
            # self.phi['which country controls country '+ str(country)] = self.troops[country][1]*2-1
            self.phi['bsr of'+str(country)] = self.get_bsr(country)
            self.phi['number of enemy neighbor of', str(country)] = len(self.get_neighbor_enemies(country))
            self.phi['number of friend neghbor of', str(country)] = len(self.get_neighbor_enemies(country))
        self.phi['100* percent of player 1 troops'] = 100*float(self.get_all_troops(1))/float(self.get_all_troops(1)+float(self.get_all_troops(0)))
        self.phi['player 1 num countries'] = self.country_count(1)
        self.phi['player 0 num countries'] = self.country_count(0)
        return self.phi


    def initialize_w(self):
        self.w={}
        phi = self.initialize_phi()
        for key in self.phi.keys():
            self.w[key]=0

        return self.w

    def v(self):
        result = 0
        for key in self.phi.keys():
            try:
                result += self.phi[key]*self.w[key]
            except:
                pass
        return result

    def grad(self):
        return self.phi

