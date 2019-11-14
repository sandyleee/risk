import game

risk = game.Game(game.usa_states, players_num = 2, player_turn=1)

risk.generate_players()
risk.generate_troops()
risk.assignment(50, 0)
risk.assignment(10, 1)

print(risk.troops)
print('-------now running the simulation')

# print(risk.get_eval())
a=risk.players[1].generateSuccessor('A','C')
for suc in a.keys():
    print(suc.troops)
    print(a[suc])
    print('-------')

# lost_soldiers ={(1,1):{(0,1):15./36,(1,0):21./36},(2,1):{(0,1):125./216,(1,0):91./216},(3,1):{(0,1):855./1296,(1,0):441./1296},(1,2):{(0,1):55./216,(1,0):161./216},(2,2):{(0,2):295./1296,(2,0):581./1296,(1,1):420./1296},(3,2):{(0,2):2890./7776,(2,0):2275./7776,(1,1):2611./7776}}
# print(float(lost_soldiers[(1,1)][(0,1)]))