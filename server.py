import game
import numpy as np
import copy


#initialization
# usa_states = {"A":["B","C"],"B":["A","C"], "C":["B","A"],}



#random assign soldiers to each country

for i in range(1):
    # random game:
    risk = game.Game(game.usa_states, player_turn=1)
    
    risk.generate_players()
    risk.generate_troops()
    risk.assignment(100, 0)
    risk.assignment(100, 1)
    
    print(risk.troops)
    
    counter = 0
    while risk.check_end_state() == False and counter<1000000:
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
