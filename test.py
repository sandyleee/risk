import game,player

game1 = game.Game(game.usa_states, game.starting_troops ,player_turn=1)
player = player.Player(1)

# print(game1.troops)
print(game1.get_countries(0))
a=player.get_attackable(game1)
player.attack(game1, 'B', 'C')

# print(game1.troops)