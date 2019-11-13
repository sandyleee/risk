import game, player


#initialization
usa_states = {"A":["B","C"],"B":["A","C"], "C":["B","A"],}

#starting troop: country:(number of troops, player)
starting_troops = {"A":[0,1],"B":[0,1],"C":[0,0]}


#random game:
game = game.Game(game.usa_states, game.starting_troops ,player_turn=1)
player = player.Player(1)
player = player.Player(2)
#random assign soldiers to each country
game.assignment(10,1)
game.assignment(10,0)

# while game.check_end_state()==False:
# 
