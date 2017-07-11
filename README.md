# Isolation, agents and tournament
## by Philipp Bechhaus & udacity-pa


### Install
1. install _Anaconda_ environment
2. copy _.yml_ file from project to folder of choice
3. open Terminal of choice
4. run _conda env create -f isol-environment-osx.yml_ to create necessary environment for tournament code
5. run _source activate isol_ to enter the environment

To run the tournament, open project folder from Terminal of choice and run _python tournament.py_ to start calculations.
Disclaimer: isol environment needs to be activated!

### Analysis sample

Following analysis shows a performance excerpt of available evaluation heuristics. The analysis is based on 210 fair games, letting the agent play against itself or an opponent embodying one out of seven different playing behaviors.

As a starter, the most obvious heuristic – especially early in game – seems to count the available moves for each active_player. For a conservative approach, we penalize the number of available moves to the active player. The corresponding heuristic is AB_Custom_3.

```python
own_moves = len(game.get_legal_moves(player))
opp_moves = len(game.get_legal_moves(game.get_opponent(player)))

return float(own_moves - opp_moves * 1.5)
```

AB_Custom is similar to AB_Custom_3, but additionally forecasts moves down the tree by a depth of 2, summarizing the available moves on each level and penalizing their score against the available moves of the opponent player.

```python
own_moves = len(game.get_legal_moves(player))
opp_moves = len(game.get_legal_moves(game.get_opponent(player)))

for move in game.get_legal_moves(player):
    new_board = game.forecast_move(move)
    own_moves += len(new_board.get_legal_moves(player))
    for move2 in new_board.get_legal_moves(player):
        new_board2 = new_board.forecast_move(move2)
        own_moves += len(new_board2.get_legal_moves(player))

for move in game.get_legal_moves(game.get_opponent(player)):
    new_board = game.forecast_move(move)
    own_moves += len(new_board.get_legal_moves(game.get_opponent(player)))
    for move2 in new_board.get_legal_moves(game.get_opponent(player)):
        new_board2 = new_board.forecast_move(move2)
        opp_moves += len(new_board2.get_legal_moves(new_board2.get_opponent(player)))

return float(own_moves - opp_moves * 1.5)
```

AB_Custom_2 adds the Manhattan Distance between the two players as an additional caveat and penalizes moves in proximity to the opponent.

```python
own_moves = len(game.get_legal_moves(player))
opp_moves = len(game.get_legal_moves(game.get_opponent(player)))

penalized_move_diff = float(own_moves - 1.5 * opp_moves)
own_pos = game.get_player_location(player)
opp_pos = game.get_player_location(game.get_opponent(player))
manhattan_distance = float(abs(own_pos[0]-opp_pos[0]) + \
abs(own_pos[1]-opp_pos[1]))

return float((penalized_move_diff/manhattan_distance**(-1)))
```

Test results below:
~~~~
                        *************************                         
                             Playing Matches                              
                        *************************                         

 Match #   Opponent    AB_Improved   AB_Custom   AB_Custom_2  AB_Custom_3 
                        Won | Lost   Won | Lost   Won | Lost   Won | Lost 
    1       Random       8  |   2     8  |   2     8  |   2     7  |   3  
    2       MM_Open      6  |   4     7  |   3     5  |   5     7  |   3  
    3      MM_Center     6  |   4     8  |   2     7  |   3     7  |   3  
    4     MM_Improved    6  |   4     9  |   1     6  |   4     8  |   2  
    5       AB_Open      5  |   5     5  |   5     5  |   5     5  |   5  
    6      AB_Center     5  |   5     5  |   5     6  |   4     6  |   4  
    7     AB_Improved    6  |   4     4  |   6     6  |   4     4  |   6  
--------------------------------------------------------------------------
           Win Rate:      60.0%        65.7%        61.4%        62.9%  
Fig. 1: Test run 1

                        *************************                         
                             Playing Matches                              
                        *************************                         

 Match #   Opponent    AB_Improved   AB_Custom   AB_Custom_2  AB_Custom_3 
                        Won | Lost   Won | Lost   Won | Lost   Won | Lost 
    1       Random       6  |   4     9  |   1     9  |   1     7  |   3  
    2       MM_Open      5  |   5     8  |   2     5  |   5     7  |   3  
    3      MM_Center     6  |   4     9  |   1     7  |   3     5  |   5  
    4     MM_Improved    6  |   4     6  |   4     8  |   2     5  |   5  
    5       AB_Open      5  |   5     4  |   6     6  |   4     7  |   3  
    6      AB_Center     5  |   5     4  |   6     7  |   3     7  |   3  
    7     AB_Improved    6  |   4     3  |   7     4  |   6     6  |   4  
--------------------------------------------------------------------------
           Win Rate:      55.7%        61.4%        65.7%        62.9%    
Fig. 2: Test run 2

                        *************************                         
                             Playing Matches                              
                        *************************                         

 Match #   Opponent    AB_Improved   AB_Custom   AB_Custom_2  AB_Custom_3 
                        Won | Lost   Won | Lost   Won | Lost   Won | Lost 
    1       Random       9  |   1     8  |   2    10  |   0     9  |   1  
    2       MM_Open      8  |   2     9  |   1     7  |   3     8  |   2  
    3      MM_Center     7  |   3     6  |   4     8  |   2     6  |   4  
    4     MM_Improved    5  |   5     8  |   2     8  |   2     7  |   3  
    5       AB_Open      5  |   5     5  |   5     4  |   6     4  |   6  
    6      AB_Center     6  |   4     7  |   3     8  |   2     5  |   5  
    7     AB_Improved    4  |   6     3  |   7     5  |   5     4  |   6  
--------------------------------------------------------------------------
           Win Rate:      62.9%        65.7%        71.4%        61.4%   
Fig. 3: Test run 3
~~~~

A salient finding is the very steady performance of AB_Custom_3, a very simple and conservative heuristic, circling between 61.4% and 62.9%, also resulting in a relatively low standard deviation of ~1.4. The highest volatility in percentage is carried by AB_Custom_2, bottoming at 61.4%, but reaching a 71.4% win rate in test 3, which results in a delta of 10 percentage points.

### Recommendation

My personal recommendation would be the preference of AB_Custom_2. Reasons are as follows:
*	AB_Custom_2 embodies the highest win rate of 66% on average
*	The next best heuristic (AB_Custom) needs to loop through 2 additional children and hence has more computational hunger
*	AB_Custom_2 has a lower standard deviation than the next best choice (AB_Custom), which could lead to the hypothesis that AB_Custom_2 is more generally applicable and more independent from the individual playing behavior of its opponent than AB_Custom
