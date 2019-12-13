import game
import numpy as np
import copy



counter0 = 0 #how many times player 0 win
counter1 = 0 #how many times player 1 win

risk = game.Game(game.usa_states, player_turn=1)
risk.generate_players()
risk.generate_troops()
risk.initialize_w()
W= risk.w

for i in range(10):
    print('i',i)
    first_player = i%2 #half the time player 1 is first half the time player 0

    #initialization of the game
    risk = game.Game(game.usa_states, player_turn=first_player)
    risk.w = W

    # print('start game W',risk.w.values())



    # if not w:
    #     for country, owner in risk.troops.keys():
    #         risk.w['troops in'+str(country)] = 0
    #         risk.w['bsr of'+str(country)] = 0
    #     risk.w['player 1 num countries'] = 0
    #     risk.w['player 0 num countries'] = 0
    #
    #
    # risk.w = w

    #generating players
    risk.generate_players()

    #generating troops: give randomly a country to player 1 or 0 with prob 50% and give each country 1 troop at first
    risk.generate_troops() #Todo: make a better initialization for country assignment



    risk.players[1].set_type('TD')
    risk.players[0].set_type('BSR') # other options may be BSR, random, aggressive, etc.

    # initial reinforcement
    n=25
    risk.players[risk.player_turn].reinforce(n)
    risk.change_player()
    risk.players[risk.player_turn].reinforce(n)



    counter = 0 #counting the number of change turns
    while risk.check_end_state() == False and counter<10000:
        # print('counter', counter)
        counter += 1

        if not(risk.check_troops()):
            raise ('error in 1')

        # reinforcement phase
        risk.phase = 'reinforce'
        # check sum
        temp_troops3 = sum(x[0] for x in risk.troops.values())
        reinforce_num = max(3,int(risk.country_count(risk.player_turn)/3.0))
        risk.players[risk.player_turn].reinforce(reinforce_num) #Todo: This should be dynamic based on the number of countries
        temp_troops4 = sum(x[0] for x in risk.troops.values())

        if temp_troops4 != temp_troops3+reinforce_num:
            raise('reinforcement error')


        if not(risk.check_troops()):
            raise ('error in 2')

        W=risk.w
        # print('start attack phase')
        #attack phase
        risk.phase = 'attack'
        risk.players[risk.player_turn].attack()

        if not(risk.check_troops()):
            raise ('error in 3')

        #check if the game is finished
        if risk.check_end_state():
            winner = risk.check_winner()
            if winner == 1:
                counter1 += 1
                # print('w after 1 win',risk.w.values())
                # print('Player 1 won')
            else:
                counter0 += 1
                # print('w after 0 win', risk.w.values())
                # print('Player 0 won')
            break
        W = risk.w
        # print('start fortify phase')
        #fortify phase
        risk.phase = 'fortify'


        #check sum
        temp_troops1 = sum(x[0] for x in risk.troops.values())

        risk.players[risk.player_turn].fortify()
        # print('fortify itself finished')

        W = risk.w

        #check sum
        temp_troops2 = sum(x[0] for x in risk.troops.values())
        if temp_troops1 != temp_troops2:
            raise('fortify error')

        if not(risk.check_troops()):
            raise ('error in 4')

        # print('change turn')
        #change turn
        risk.change_player()
        if counter == 10000:
            print('game not finished in 10000 round')


print(W)
print("Player 1 wins:", counter1)
print("Player 0 wins:", counter0)
