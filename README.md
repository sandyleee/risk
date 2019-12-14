# Risk game with AI
In this project, our goal was to implement a game-playing agent for the board game Risk.
Today, there are many classic games like Chess and Poker that are frequently addressed in the field of scientific computer game playing research.
On the contrary, while Risk is played all around the world, it has received much less scientific attention.
We specifically chose this topic because this lack of information makes the creation of an AI agent for Risk more interesting.
A further reason is that unlike classic board games, Risk involves each player making several decisions in a single game turn, 
and the state-space complexity is extremely large. The project is therefore all the more challenging!

There are three main files on this project: game.py, player.py and server.py.
A description of the different files and classes in our current implementation is described below:

a. game.py: In this file, we implemented the main game and define the class Game necessary for the game to run. This class is the core of our architecture, as it controls the flow of the game by generating all attributes of the game (players, countries, troops) and checking the state of the game. This class also contains the method assignment which will be used in this simplified version of the game to allocate reinforcement troops randomly. Finally, the method check_winner is used to check if the game has reached the end state or not (one of the players has conquered all the territories).

b. player.py: In this file, we defined all the necessary methods to operate the attack phase, as the reinforcement is randomized and we are not considering the fortifying phase yet. Thus, two methods are useful: get_attackable, which will return all the territories that the player can attack (all the enemy territories which are neighbors to controlled territories with strictly more than 1 troop). Secondly, we define the method attack, which specifies all the dice rules and reassign the troops to the conquered territory if the attacker wins the battle.

c. server.py: In this file, we run the game multiple times to compare the performance of the agents. This file fully controlls the game flow. Also there is a variation of this file named serverTD.py which controls the flow of the game when one of its players is a TD player.

In this project we have implemented four kinds of players:
1. Random player: which reinfoce and attack randomly and do not fortify its troops after attack
2. Aggressive player: which reinfoce and attack aggresively, i.e. reinforce the country that has a at least one enemy neighbor 
and the most number of troops, and then attack from the strongest country at each step to its weakest neghbor. This player do not forrify its troops after attack.
3. BSR player: This player which is smarter that the other two is playing based on BSR ratio. In reinforcement phase it is fining the most vulnerable enemy country, i.e. the country with the most BSR.
Then find the strongest neighbor that can attack to that country and reinforce it with all given troops. In the attack phase, it will choose origin and destination in a same manner that it implemented for reinforcement phase.
In fortify phase it will fortify the troops such that it minimizes the maximum BSR amonge its countries.
4. TD player: This player which uses TD learning algorithm in all three reinforcement, attack and fortify phases.

You may run python server.py to see the result of fighting two agents. To change the agents type you can do it in server.py.
