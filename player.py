import numpy as np
from copy import deepcopy
# from troop import Troop
# starting_troops = 25
# from agent import Agent
# import random
# import copy
# import game
# from game import Game

lost_soldiers ={(1,1):{(0,1):15./36,(1,0):21./36},(2,1):{(0,1):125./216,(1,0):91./216},(3,1):{(0,1):855./1296,(1,0):441./1296},(1,2):{(0,1):55./216,(1,0):161./216},(2,2):{(0,2):295./1296,(2,0):581./1296,(1,1):420./1296},(3,2):{(0,2):2890./7776,(2,0):2275./7776,(1,1):2611./7776}}
class Player:
    def __init__(self, id, game):
        self.id = id
        self.game = game#from game class

    def get_attackable(self):
        #to ckeck if it is the player's turn
        if self.game.player_turn != self.id:
            raise('not player turn')
        else:
            attackable = {}
            for country in self.game.troops.keys():

                #check if the country belongs to player
                if self.game.troops[country][1] == self.id:
                    enemy_neighbors = []


                    if self.game.troops[country][0]>1:#check if there are more than 1 troops to attack

                        #check if the neighbor country belongs to enemy
                        for neighbor in self.game.map[country]:
                            if self.game.troops[neighbor][1] != self.id:
                                enemy_neighbors.append(neighbor)
                        if enemy_neighbors: attackable[country]=enemy_neighbors
        return attackable

    def attack(self, attacking_country, destination_country):
        #check if we are allowed to attack
        if attacking_country in set(self.get_attackable().keys()):
            if destination_country in self.get_attackable()[attacking_country]:
                attacker_troops = min(self.game.troops[attacking_country][0]-1,3)
                defender_troops = min(self.game.troops[destination_country][0],2)
                battle_troops = min(attacker_troops,defender_troops)
                attacker_dice = np.sort(np.random.randint(1,7,attacker_troops))[::-1][:battle_troops]
                defender_dice = np.sort(np.random.randint(1, 7, defender_troops))[::-1][:battle_troops]

                #number of killings in both side
                attacker_causalities = 0
                defender_causalities = 0

                #comparing the dices
                for soldier in range(battle_troops):
                    if attacker_dice[soldier]>defender_dice[soldier]:
                        defender_causalities += 1
                    else:
                        attacker_causalities += 1
                #update the board
                self.game.troops[attacking_country][0] -= attacker_causalities
                self.game.troops[destination_country][0] -= defender_causalities
                if self.game.troops[destination_country][0] < 0:
                    raise ('eroor')
                elif self.game.troops[destination_country][0] == 0:
                    
                    #re-assign the winner to the destination country
                    self.game.troops[destination_country][1] = self.id#.id
                    
                    #move the troops to the destinaiton country
                    self.game.troops[destination_country][0] = self.game.troops[attacking_country][0]-1
                    self.game.troops[attacking_country][0] = 1
                
            else:
                raise ('error: you can not attack to this country')
        else:
            raise ('error: you can not attack from this country')
        
    def get_aggresive_attackable(self):
        atacking_countries = self.get_attackable()
        if atacking_countries:
            origins = atacking_countries.keys()
            origin = None
            troops = 0
            #get the country with maximum troops
            for country in origins:
                if self.game.troops[country][0]>troops:
                    origin = country
                    troops = self.game.troops[country][0]
            destination = None
            troops = 100000
            for country in atacking_countries[origin]:
                if self.game.troops[country][0]<troops:
                    destination = country
                    troops = self.game.troops[country][0]
            return origin, destination
        else:
            return None
        
    def infinit_aggresive_attack(self):
        temp = self.get_aggresive_attackable()
        if temp:
            origin , destination = temp
            self.attack(origin, destination)
            self.infinit_aggresive_attack()

    def get_one_attackable(self):
        atacking_countries = self.get_attackable()
        if atacking_countries:
            choice = np.random.choice(list(atacking_countries))
            atacking_country = choice
            destination = np.random.choice(atacking_countries[choice])
            return atacking_country, destination
        else:
            return None
              
    def infinit_random_attack(self):
        temp = self.get_one_attackable() 
        if temp:
            origin, destination = temp        
            self.attack(origin, destination)
            self.infinit_random_attack()
            
            
    def semi_smart_random_attack(self, count):
        temp = self.get_one_attackable() 
        if temp:
            origin, destination = temp
            otroops = self.game.troops[origin][0]
            dtroops = self.game.troops[destination][0]
            if not((otroops==3 and dtroops>1) or otroops==2):
                self.attack(origin, destination)
                self.semi_smart_random_attack(0)

                

    def get_semi_smart_aggresive_attackable(self):
        atacking_countries = self.get_attackable()
        if atacking_countries:
            origins = atacking_countries.keys()
            origin = None
            otroops = 0
            # get the country with maximum troops
            for country in origins:
                if self.game.troops[country][0] > otroops:
                    origin = country
                    otroops = self.game.troops[country][0]
            destination = None
            dtroops = 100000
            for country in atacking_countries[origin]:
                if self.game.troops[country][0] < dtroops:
                    destination = country
                    dtroops = self.game.troops[country][0]
            # if the number of attacking dice is less than defending not to attack
            if not((otroops==3 and dtroops>1) or otroops==2):
                return origin, destination
            else:
                return None
        else:
            return None

    def infinit_semi_smart_aggresive_attack(self):
        temp = self.get_semi_smart_aggresive_attackable()
        if temp:
            origin, destination = temp
            self.attack(origin, destination)
            self.infinit_semi_smart_aggresive_attack()

    def generateSuccessor(self,attacking_country,destination_country, change_turn):
        if attacking_country in set(self.get_attackable().keys()):
            if destination_country in self.get_attackable()[attacking_country]:
                attacker_troops = min(self.game.troops[attacking_country][0] - 1, 3)
                defender_troops = min(self.game.troops[destination_country][0], 2)
                outcomes = lost_soldiers[(attacker_troops,defender_troops)]
                successor = {}
                for attacker_causalities, defender_causalities in outcomes.keys():
                    new_game = deepcopy(self.game)
                    new_game.troops[attacking_country][0] -= attacker_causalities
                    new_game.troops[destination_country][0] -= defender_causalities
                    if new_game.troops[destination_country][0] < 0:
                        raise ('error')
                    elif new_game.troops[destination_country][0] == 0:
                        # re-assign the winner to the destination country
                        new_game.troops[destination_country][1] = self.id  # 
                        # move the troops to the destinaiton country
                        new_game.troops[destination_country][0] = new_game.troops[attacking_country][0] - 1
                        new_game.troops[attacking_country][0] = 1
                    new_game.change_player(change_turn)
                    successor[new_game]=outcomes[(attacker_causalities, defender_causalities)]
                return(successor)
            else:
                raise ('error: you can not attack to this country')
        else:
            raise ('error: you can not attack from this country')





    #
    
        
        
    #     
    # 
    # print(recurse(gameState, self.index, self.depth))
    # return recurse(gameState, self.index, self.depth)[1]