import numpy as np
# from troop import Troop
# starting_troops = 25
# from agent import Agent
# import random
# import copy
# import game
# from game import Game

class Player:

    def __init__(self, id, ):
        self.id = id

    def get_attackable(self, game):

        #to ckeck if it is the player's turn
        if game.player_turn != self.id:
            raise('not player turn')
        else:
            attackable = {}
            for country in game.troops.keys():

                #check if the country belongs to player
                if game.troops[country][1] == self.id:
                    enemy_neighbors = []


                    if game.troops[country][0]>1:#check if there are more than 1 troops to attack

                        #check if the neighbor country belongs to enemy
                        for neighbor in game.map[country]:
                            if game.troops[neighbor][1] != self.id:
                                enemy_neighbors.append(neighbor)
                        if enemy_neighbors: attackable[country]=enemy_neighbors
        return attackable

    def attack(self, game, attacking_country, destination_country):
        #check if we are allowed to attack
        if attacking_country in set(self.get_attackable(game).keys()):
            if destination_country in self.get_attackable(game)[attacking_country]:
                attacker_troops = min(game.troops[attacking_country][0]-1,3)
                defender_troops = min(game.troops[destination_country][0],2)
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
                game.troops[attacking_country][0] -= attacker_causalities
                game.troops[destination_country][0] -= defender_causalities
                if game.troops[destination_country][0] < 0:
                    raise ('eroor')
                elif game.troops[destination_country][0] == 0:
                    
                    #re-assign the winner to the destination country
                    game.troops[destination_country][1] = self.id#.id
                    
                    #move the troops to the destinaiton country
                    game.troops[destination_country][0] = game.troops[attacking_country][0]-1
                    game.troops[attacking_country][0] = 1
                
            else:
                raise ('error: you can not attack to this country')
        else:
            raise ('error: you can not attack from this country')