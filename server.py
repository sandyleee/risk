import game
import numpy as np
import copy


#initialization
usa_states = {"A":["B","C"],"B":["A","C"], "C":["B","A"],}

#starting troop: country:(number of troops, player)
initial_troops = {"A":[0,1],"B":[0,1],"C":[0,0]}




#random assign soldiers to each country

for i in range(100):
    # random game:
    troops = copy.deepcopy(initial_troops)
    risk = game.Game(usa_states, starting_troops=troops, player_turn=1)
    risk.generate_players()

    risk.assignment(30, 0)
    risk.assignment(30, 1)
    counter = 0
    while risk.check_end_state() == False and counter<10000:
        turn = risk.player_turn
        player = risk.players[turn]
        atacking_countries = player.get_attackable()
        if atacking_countries:
            choice = np.random.choice(list(atacking_countries))
            atacking_country = choice
            destination = np.random.choice(atacking_countries[choice])
            player.attack(atacking_country,destination)
        risk.player_turn = 1 - risk.player_turn
        counter += 1
    if risk.check_end_state():
        risk.check_winner()
    else:
        print('game not finished in 10000 round')
# while game.check_end_state()==False:
# 
