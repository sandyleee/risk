import numpy as np
# from troop import Troop
# starting_troops = 25
# from agent import Agent
# import random
# import copy
# import game
# from game import Game

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