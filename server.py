import game
import numpy as np


#initialization
usa_states = {"A":["B","C"],"B":["A","C"], "C":["B","A"],}

#starting troop: country:(number of troops, player)
starting_troops = {"A":[0,1],"B":[0,1],"C":[0,0]}


#random game:
game = game.Game(game.usa_states, starting_troops ,player_turn=1)
game.generate_players()

print(game.troops)
game.assignment(30,0)
game.assignment(30,1)

#random assign soldiers to each country
while game.check_end_state() == False:
    turn = game.player_turn
    player = game.players[turn]
    atacking_countries = player.get_attackable()
    if atacking_countries:
        choice = np.random.choice(list(atacking_countries))
        atacking_country = choice
        destination = np.random.choice(atacking_countries[choice])
        player.attack(atacking_country,destination)
    print(game.troops)
game.check_winner()

# while game.check_end_state()==False:
# 
