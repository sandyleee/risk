import game,player

game1 = game.Game(game.usa_states, game.starting_troops, player_turn=0)


game1.generate_players()

a = game1.players[0].get_attackable()
print(game1.get_countries(0))
print(a)


# player = player.Player(1)
# 
# print(game1.troops)
# print(game1.get_countries(0))
# # a=player.get_attackable(game1)
# player.attack(game1, 'B', 'C')
# 
# # game1.assignment(500,1)
# 
# print(game1.troops)
# # print(player)
# game