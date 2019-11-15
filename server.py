import game
import numpy as np
import copy


#initialization
# usa_states = {"A":["B","C"],"B":["A","C"], "C":["B","A"],}



#random assign soldiers to each country
counter0 = 0
counter1 = 0
for i in range(1000):
    # random game:
    # print(i)
    risk = game.Game(game.usa_states, player_turn=1)
    
    risk.generate_players()
    risk.generate_troops()
    risk.assignment(5, 0)
    risk.assignment(5, 1)    
    counter = 0
    while risk.check_end_state() == False and counter<10000:
        risk.assignment(3, risk.player_turn)
        turn = risk.player_turn
        player = risk.players[turn]
        
        #player 0:semi_smart_aggressive, player 1:random
        if risk.player_turn:
            player.infinit_semi_smart_aggresive_attack()
            # player.semi_smart_random_attack(0)
            # player.infinit_random_attack()
        else:
            # player.infinit_semi_smart_aggresive_attack()
            player.semi_smart_random_attack(0)
            # player.infinit_random_attack()
            
        risk.player_turn = 1 - risk.player_turn
        counter += 1
    if risk.check_end_state():
        winner = risk.check_winner()
        if winner == 1:
            counter1 += 1
        else:
            counter0 += 1
    else:
        print('game not finished in 1000 round')
# while game.check_end_state()==False:
# 
print("Player 0 wins:", counter0)
print("Player 1 wins:", counter1)