import numpy as np
from copy import deepcopy
# from troop import Troop
# starting_troops = 25
# from agent import Agent
# import random
# import copy
# import game
# from game import Game
import random

lost_soldiers ={(1,1):{(0,1):15./36,(1,0):21./36},(2,1):{(0,1):125./216,(1,0):91./216},(3,1):{(0,1):855./1296,(1,0):441./1296},(1,2):{(0,1):55./216,(1,0):161./216},(2,2):{(0,2):295./1296,(2,0):581./1296,(1,1):420./1296},(3,2):{(0,2):2890./7776,(2,0):2275./7776,(1,1):2611./7776}}



class Player:
    def __init__(self, id, game):
        self.id = id
        self.game = game#from game class

    def set_type(self,type):
        self.type = type

    def get_type(self):
        return self.type

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
                            # print(neighbor, 'is neighbort to', country)
                            if self.game.troops[neighbor][1] != self.id:
                                enemy_neighbors.append(neighbor)
                                # print(neighbor, 'is enemy neighbor to', country)
                            # else:
                            #     print(neighbor, 'is Nooooooot enemy neighbour to', country)
                        if enemy_neighbors:
                            attackable[country]=enemy_neighbors
        return attackable

    def reinforce(self,num_assignments):

        self.game.initialize_phi()
        vsw = self.game.v()
        grad = self.game.phi

        if self.get_type()=='random':
            countries = self.game.get_countries(self.id)
            for i in range(num_assignments):
                country = random.choice(countries)
                self.game.troops[country][0] += 1
        if self.get_type()=='aggressive':
            country, destination = self.get_strongest_country()
            self.game.troops[country][0] += num_assignments
        if self.get_type() == 'BSR':
            country, destination = self.get_BSR_attackable()
            self.game.troops[country][0] += num_assignments
        if self.get_type() == 'TD':
            for i in range(num_assignments):
                country = self.get_next_reinforcement_action()
                if country==None:
                    break
                self.game.troops[country][0] += 1

        self.game.initialize_phi()
        vshatw = self.game.v()
        update = self.game.eta * (vsw - self.game.gama*vshatw)
        # print('self.game.w',self.game.w)
        for key in self.game.phi.keys():
            try:
                self.game.w[key] -= update * grad[key]
            except:
                self.game.w[key] = -update * grad[key]


    def attack(self): #Todo: If the attacker wins a country it will move all the troops overther now, which needs to be changed
        self.game.initialize_phi()
        vsw = self.game.v()
        grad = self.game.phi

        if self.get_type() == 'random': #semi_smart random
            self.semi_smart_random_attack()

        if self.get_type() == 'aggressive':
            self.infinit_semi_smart_aggresive_attack()

        if self.get_type() == 'BSR':
            self.infinit_BSR_attack()

        if self.get_type() == 'TD': #Todo: teach when to stop attacking more inteligent
            while True:
                if self.get_next_attack_action():
                    try:
                        orig, dist = self.get_next_attack_action()
                        self.one_time_attack(orig, dist)
                    except:
                        print('break attack')
                        break
                else:
                    break

        self.game.initialize_phi()
        vshatw = self.game.v()
        if self.game.check_end_state():
            if self.game.check_winner() == 1:
                r = 10000
            else:
                r = - 10000
        else:
            r = 0
        update = self.game.eta * (vsw - r - self.game.gama*vshatw)
        if self.game.check_end_state():
            print('update after endstate', update)
        for key in self.game.phi.keys():
            # print(update*grad[key])
            try:
                self.game.w[key] -= update * grad[key]
            except:
                self.game.w[key] = -update * grad[key]


    def fortify(self):
        self.game.initialize_phi()
        vsw = self.game.v()
        grad = self.game.phi
        if self.get_type() == 'random':
            pass
        if self.get_type() == 'aggressive':
            pass
        if self.get_type() == 'BSR':
            self.BSR_fortify()
        if self.get_type() == 'TD':
            counter = 0
            while counter<20:
                counter += 1
                if self.get_next_fortify_action():
                    try:
                        orig, dist = self.get_next_fortify_action()
                        self.game.troops[orig][0] -= 1
                        self.game.troops[dist][0] += 1
                        # print(self.game.troops)
                    except:
                        print('break fortify')
                        break
                else:
                    break
        self.game.initialize_phi()
        vshatw = self.game.v()
        update = self.game.eta * (vsw - self.game.gama*vshatw)
        for key in self.game.phi.keys():
            self.game.w[key] -= update * grad[key]

    def one_time_attack(self, attacking_country, destination_country):
        #check if we are allowed to attack
        if attacking_country in set(self.get_attackable().keys()):
            # print('It is possible to attack from:', attacking_country,'to these countries:', self.get_attackable()[attacking_country])
            if destination_country in self.get_attackable()[attacking_country]:
                # print(self.game.troops)
                attacker_troops = min(self.game.troops[attacking_country][0]-1,3)
                defender_troops = min(self.game.troops[destination_country][0],2)
                battle_troops = min(attacker_troops,defender_troops)
                attacker_dice = np.sort(np.random.randint(1,7,attacker_troops))[::-1][:battle_troops]
                defender_dice = np.sort(np.random.randint(1, 7, defender_troops))[::-1][:battle_troops]

                #number of killings in both side
                attacker_causalities = 0
                defender_causalities = 0

                #comparing the dices
                # print('battle_troops', battle_troops)
                for soldier in range(int(battle_troops)):
                    if attacker_dice[soldier]>defender_dice[soldier]:
                        defender_causalities += 1
                    else:
                        attacker_causalities += 1
                #update the board
                # print('Attacking Player:',self.id ,'  Loss:',attacker_causalities)
                # print('Defending Player:',1-self.id,'  Loss:',defender_causalities)
                self.game.troops[attacking_country][0] -= attacker_causalities
                self.game.troops[destination_country][0] -= defender_causalities
                if self.game.troops[destination_country][0] < 0:
                    raise ('eror')
                elif self.game.troops[destination_country][0] == 0:
                    
                    #re-assign the winner to the destination country
                    self.game.troops[destination_country][1] = self.id#.id
                    
                    #move the troops to the destinaiton country
                    self.game.troops[destination_country][0] = self.game.troops[attacking_country][0]-1
                    self.game.troops[attacking_country][0] = 1
                return defender_causalities-attacker_causalities
                
            else:
                print(self.game.troops)
                print('turn',self.game.player_turn)
                print('origin', attacking_country)
                print('desitnation', destination_country)
                raise ('error: you can not attack to this country')
        else:
            print(self.game.troops)
            print('turn', self.game.player_turn)
            print('origin',attacking_country)
            raise ('error: you can not attack from this country')
        
    def get_strongest_country(self):
        atacking_countries = self.get_attackable()
        if atacking_countries:
            origins = atacking_countries.keys()
            origin = None
            troops = 0
            # get the country with maximum troops
            for country in origins:
                if self.game.troops[country][0] > troops:
                    origin = country
                    troops = self.game.troops[country][0]
            return origin , atacking_countries[origin]
        else:
            troop = 0
            origin = None
            for country in self.game.get_counties(self.id):
                if self.game.troops[country][0]>troop:
                    troop=self.game.troops[country][0]
                    origin = country
            return origin, None

    def get_aggresive_attackable(self):
        # atacking_countries = self.get_attackable()
        # if atacking_countries:
        #     origins = atacking_countries.keys()
        #     origin = None
        #     troops = 0
        #     #get the country with maximum troops
        #     for country in origins:
        #         if self.game.troops[country][0]>troops:
        #             origin = country
        #             troops = self.game.troops[country][0]
        destination = None
        troops = 100000
        origin, dest_countries = self.get_strongest_country()
        if origin:
            for country in dest_countries:
                if self.game.troops[country][0] < troops:
                    destination = country
                    troops = self.game.troops[country][0]
            return origin, destination

        else:
            return None
        
    def infinit_aggresive_attack(self):
        temp = self.get_aggresive_attackable()
        if temp:
            origin , destination = temp
            self.one_time_attack(origin, destination)
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
            self.one_time_attack(origin, destination)
            self.infinit_random_attack()

    def semi_smart_random_attack(self):
        temp = self.get_one_attackable() 
        if temp:
            origin, destination = temp
            otroops = self.game.troops[origin][0]
            dtroops = self.game.troops[destination][0]
            if not((otroops==3 and dtroops>1) or otroops<=2):
                self.one_time_attack(origin, destination)
                self.semi_smart_random_attack()

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
            self.one_time_attack(origin, destination)
            self.infinit_semi_smart_aggresive_attack()

    def get_BSR_attackable(self):
        bsr = 0
        destination = None
        for country in self.game.troops.keys():
            if self.game.troops[country][1] != self.id:
                if self.game.get_bsr(country) >= bsr:
                    destination = country
                    bsr = self.game.get_bsr(country)

        if bsr == 0:
            # print('troops',self.game.troops)
            # print('turn', self.game.player_turn)
            # print('Cant find any destination country')
            return None
        origin = -1
        troop = 0
        # print('enemy neighbors of', destination,':',self.game.get_neighbor_enemies(destination))
        for neighbor in self.game.get_neighbor_enemies(destination):
            if self.game.troops[neighbor][0]> troop:
                troop = self.game.troops[neighbor][0]
                origin = neighbor

        return origin,destination

    def infinit_BSR_attack(self):
        temp = self.get_BSR_attackable()
        if self.get_BSR_attackable():
            origin, destination = temp
            otroops = self.game.troops[origin][0]
            dtroops = self.game.troops[origin][0]
            if not ((otroops == 3 and dtroops > 1) or otroops <= 2):
                # print('bsr orig dest',origin,destination)
                self.one_time_attack(origin, destination)
                self.infinit_BSR_attack()

    def BSR_fortify(self):
        components = self.game.connectedComponents(self.id)
        for component in components:
            enemy_troops = {}
            country_troops = {}
            for country in component:
                country_troops[country] = self.game.troops[country][0]
                enemy_troops[country] = self.game.sum_neighbor_enemy_troops(country)
            country_troops_sum = sum(country_troops.values())
            enemy_troops_sum = sum(enemy_troops.values())
            if not (self.game.check_troops()):
                raise ('error in 6')

            if enemy_troops_sum != 0:
                country_troops_float = {}
                for country in component:
                    country_troops_float[country] = enemy_troops[country]*country_troops_sum/float(enemy_troops_sum)
                rest = 0.00
                country_troops_new ={}

                # print('float troops', country_troops_float)
                # print('troops3', self.game.troops)
                for country in country_troops_float.keys():
                    troop_new = round(country_troops_float[country]-rest)
                    if troop_new<= 1:
                        troop_new =1
                    rest += troop_new-country_troops_float[country]
                    country_troops_new[country] = troop_new
                    if troop_new<1:
                        print('country','troop_new',country,troop_new)
                        raise ('error in 7')
                    self.game.troops[country] = [troop_new, self.id]
                # print('rest',rest)
                while rest>0.2:
                    for country in country_troops_new.keys():
                        if country_troops_new[country]>1:
                            country_troops_new[country] -= 1
                            self.game.troops[country] = [country_troops_new[country], self.id]
                            # print('rest used to be', rest)
                            rest = rest-1
                            if rest<=0.01:
                                # print('rest now is equal to:', rest)
                                break
                if sum(country_troops_new.values()) != country_troops_sum:
                    print('difference',country_troops_sum-sum(country_troops_new.values()))
                    raise('error in 8')

            if not (self.game.check_troops()):

                raise ('error in 5')

    def minimax_attack(self):
        if self.id == 1 and self.get_attackable():
            (origin, destination, change_player) = recurse(self.game,1)[1]
            self.one_time_attack(origin, destination)
            self.minimax_attack()

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

    def get_actions_reinforce_one_troop(self):
        return self.game.get_counties(self.id)

    def td_reinforce_one_value(self, country):
        new_game = deepcopy(self.game)
        new_game.troops[country][0] += 1
        new_game.initialize_phi()
        new_game.w = self.game.w
        return new_game.v()

    def get_next_reinforcement_action(self):
        temp = None
        result = None
        for country in self.get_actions_reinforce_one_troop():
            if temp!=None:
                if self.td_reinforce_one_value(country) > temp:
                    temp = self.td_reinforce_one_value(country)
                    result = country
            else:
                temp = self.td_reinforce_one_value(country)
                result = country
        return result

    def get_action_attack_one(self):
        result = []
        for orig in  self.get_attackable().keys():
            for dist in self.get_attackable()[orig]:
                result.append([orig,dist])
        return result


    def td_attack_one_value(self,orig, dist):
        new_game = deepcopy(self.game)
        new_game.players[self.id].one_time_attack(orig,dist)
        new_game.initialize_phi()
        new_game.w = self.game.w
        return new_game.v()

    def get_next_attack_action(self):
        temp = -100 #todo: self.game.v()
        result = None
        # print('beeeeeeer',self.get_action_attack_one())
        for orig, dist in self.get_action_attack_one():
            if self.td_attack_one_value(orig,dist) > temp:
                temp = self.td_attack_one_value(orig,dist)
                result = [orig, dist]
        return result

    def get_action_fortify(self):#return a list of [[orig1,dist1], [orig2,dist2], ...]
        list = []
        components = self.game.connectedComponents(self.id)
        for component in components:
            for orig in component:
                for dist in component:
                    if dist !=orig:
                        if self.game.troops[orig][0]>1:
                            list.append([orig,dist])
        return list

    def td_fortify_one_value(self,orig,dist):
        new_game = deepcopy(self.game)
        new_game.troops[orig][0] -= 1
        new_game.troops[dist][0] += 1
        new_game.initialize_phi()
        new_game.w = self.game.w

        return new_game.v()

    def get_next_fortify_action(self):
        temp = self.game.v()
        # print('fortify value first', self.game.v())
        # print('troops',self.game.troops)
        result = None
        for orig, dist in self.get_action_fortify():
            if self.td_fortify_one_value(orig, dist)>temp:
                temp = self.td_fortify_one_value(orig, dist)
                # print('fortify value last', temp)
                result = [orig,dist]
        return result


def recurse(game, depth): #return reward, action
    # print(game.troops)
    if game.check_end_state():# or state.getLegalActions(index) == []:
        return ((game.check_winner())*1000, None)
    elif depth == 0:
        # print('hey this is evaluationFunction for depth=zero', self.evaluationFunction(state))
        return (game.get_eval(), None)  # however it is better not to use "self", but I don't know how
    if game.player_turn == 1:
        attackable = game.players[1].get_attackable()
        candidates = {}
        for origin in attackable.keys():
            for destination in attackable[origin]:
                #last argument is chang_turn action
                candidates[(origin,destination, True)]= game.players[1].generateSuccessor(origin,destination,True)
                candidates[(origin, destination, False)] = game.players[1].generateSuccessor(origin, destination, False)
        reward = 0
        optimal_action = None
        for action in candidates.keys():
            action_reward = 0
            for outcome in candidates[action].keys():
                action_reward += candidates[action][outcome]*recurse(outcome,depth)[0]
            if reward < action_reward:
                reward = action_reward
                optimal_action = action
        return reward, optimal_action
    elif game.player_turn == 0:
        attackable = game.players[0].get_attackable()
        candidates = {}
        for origin in attackable.keys():
            for destination in attackable[origin]:
                candidates[(origin,destination, True)]= game.players[0].generateSuccessor(origin,destination, True)
                candidates[(origin, destination, False)] = game.players[0].generateSuccessor(origin, destination, False)
        reward = 10000
        optimal_action = None
        for action in candidates.keys():
            action_reward = 0
            for outcome in candidates[action].keys():
                action_reward += candidates[action][outcome]*recurse(outcome,depth-1)[0]
            if reward > action_reward:
                reward = action_reward
                optimal_action = action
        return reward, optimal_action



