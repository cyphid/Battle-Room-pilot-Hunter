#dont go for food you cant access
#be more agrressive
#head to head (murder!)
#





import random
import typing
import math
import numpy as np
from queue import PriorityQueue


from modules.AvoidHeadToHeadCollisionsModule import AvoidHeadToHeadCollisionsModule

from modules.SmartFoodChasingnew import SmartFoodChasingModule
from modules.AvoidBackwardMoveModule import AvoidBackwardMoveModule
from modules.AvoidOutOfBoundsModule import AvoidOutOfBoundsModule
from modules.AvoidOtherSnakesModule import AvoidOtherSnakesModule
from modules.LoopAvoidanceModule import LoopAvoidanceModule
from modules.PreferLargerSpacesModule import PreferLargerSpacesModule
from modules.AvoidSelfCollisionModule import AvoidSelfCollisionModule


import heapq

class MoveRankingModule:
  def rank_moves(self, game_state: typing.Dict) -> typing.Dict:
      """
      Returns a dictionary with rankings for each direction.
      Example: {'up': 0.5, 'down': 0.2, 'left': 0.1, 'right': 0.2}
      """
      pass
#Modules go here







#non module stuff

# Softmax Function
def softmax(scores):
  print("Raw scores (before softmax):", scores)  # Add this line to print raw scores
  exp_scores = np.exp(scores - np.max(scores))  # Stability improvement by subtracting max
  probabilities = exp_scores / np.sum(exp_scores)
  return probabilities

# Decision Function
def decide_move(modules, game_state):
    rankings = {'up': [], 'down': [], 'left': [], 'right': []}
    for module in modules:
        module_rankings = module.rank_moves(game_state)
        for direction, ranking in module_rankings.items():
            rankings[direction].append(ranking)

    # Print the rankings dictionary before summing and averaging
    print("Weights from all modules: ")
    for direction, ranks in rankings.items():
        print(f"{direction}: {ranks}")

    # Average the rankings and apply softmax
    avg_rankings = {direction: sum(ranks) / len(ranks) for direction, ranks in rankings.items()}
    directions, scores = zip(*avg_rankings.items())
    probabilities = softmax(np.array(scores))

    # Print each direction's probability
    for direction, probability in zip(directions, probabilities):
        print(f"Probability of moving {direction}: {probability:.4f}")

    # Choose move based on probabilities
    max_prob = max(probabilities)
    best_moves = [direction for direction, prob in zip(directions, probabilities) if prob == max_prob]
    chosen_move = random.choice(best_moves)

    # Print the chosen move here
    print(f"Chosen move: {chosen_move}")

    return chosen_move


# Example of a Module
class RandomMoveModule(MoveRankingModule):
    def rank_moves(self, game_state: typing.Dict) -> typing.Dict:
        return {direction: random.random() for direction in ['up', 'down', 'left', 'right']}

# Register Modules
avoidBackwardMoveModuleInstance = AvoidBackwardMoveModule()
avoidOutOfBoundsModuleInstance = AvoidOutOfBoundsModule()
avoidSelfCollisionModuleInstance = AvoidSelfCollisionModule()
loopAvoidanceModuleInstance = LoopAvoidanceModule()
avoidOtherSnakesModuleInstance = AvoidOtherSnakesModule()
SmartFoodChasingnewInstance = SmartFoodChasingModule()
avoidHeadToHeadCollisionsModuleInstance = AvoidHeadToHeadCollisionsModule()
preferLargerSpacesModuleInstance = PreferLargerSpacesModule()

# Add the rank_moves method of each instance to the modules list
modules = [
    avoidBackwardMoveModuleInstance,
    avoidOutOfBoundsModuleInstance,
    avoidSelfCollisionModuleInstance,
    loopAvoidanceModuleInstance,
    avoidOtherSnakesModuleInstance,
    SmartFoodChasingnewInstance,
    avoidHeadToHeadCollisionsModuleInstance,
    preferLargerSpacesModuleInstance
]    


# Battlesnake Info Function
def info() -> typing.Dict:
    print("hi")
    print("INFO")
    return {
        "apiversion": "1",
        "author": "",  # Your Battlesnake Username
        "color": "#FF0000",  # Choose color
        "head": "default",  # Choose head
        "tail": "default",  # Choose tail
    }

# Start Function
def start(game_state: typing.Dict):
    print("GAME START")
    


# End Function
def end(game_state: typing.Dict):
    print("GAME OVER\n")
    
    

# Move Function
def move(game_state: typing.Dict) -> typing.Dict:
    # Your logic for preventing invalid moves
    next_move = decide_move(modules, game_state)
    
    print(f"MOVE {game_state['turn']}: {next_move}")
    return {"move": next_move}

# Main Execution
if __name__ == "__main__":
    from server import run_server
    run_server({"info": info, "start": start, "move": move, "end": end})
