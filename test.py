import game

risk = game.Game(game.usa_states, players_num = 2, player_turn=1)

risk.generate_players()
risk.generate_troops()
risk.assignment(5, 0)
risk.assignment(3, 1)

print(risk.troops)
print('-------now running the simulation')

# print(risk.get_eval())
# a=risk.players[1].generateSuccessor('A','C')
print(risk.troops)
a=game.recurse(risk,1)
print(a)