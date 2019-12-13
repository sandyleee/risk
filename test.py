import game
import player

risk = game.Game(game.usa_states, players_num = 2, player_turn=1)

risk.generate_players()
# risk.generate_troops()
# risk.assignment(5, 0)
# risk.assignment(5, 1)
risk.troops = {'C': [4, 1], 'Z': [5, 0], 'D': [1, 0], 'Y': [2, 0], 'B': [3, 0], 'A': [1, 1]}

# print(sum(x[0] for x in risk.troops.values()))

# print(risk.country_count(1))

# print(risk.players[0].get_strongest_country())

# print(risk.players[1].get_next_fortify_action())
print(risk.players[1].get_next_reinforcement_action())


# print(risk.troops)
# print('-------now running the simulation')
#
# print(risk.get_eval())
# # a=risk.players[1].generateSuccessor('A','C')
# print(risk.troops)
# # print(risk.)
# print(risk.players[1].get_BSR_attackable())
# # a=player.recurse(risk,1)
# # print(a)
# print(risk.get_neighbor_enemies('A'))
# print(risk.map)
# print(risk.connectedComponents(0))