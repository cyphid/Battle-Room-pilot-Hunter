#dont go for food you cant access
#be more agrressive
#head to head (murder!)
#





import random
import typing
import math
import numpy as np
from queue import PriorityQueue


from modules import AvoidHeadToHeadCollisionsModule
from modules import Logstuff
from modules import SmartFoodChasingModule
from modules import AvoidBackwardMoveModule
from modules import AvoidOutOfBoundsModule
from modules import AvoidOtherSnakesModule
from modules import AStarFoodChasingModule
from modules import LoopAvoidanceModule
from modules import PreferLargerSpacesModule


import heapq

class MoveRankingModule:
  def rank_moves(self, game_state: typing.Dict) -> typing.Dict:
      """
      Returns a dictionary with rankings for each direction.
      Example: {'up': 0.5, 'down': 0.2, 'left': 0.1, 'right': 0.2}
      """
      pass
#Modules go here





class HealthLoggerModule:
  def __init__(self):
      self.health_log = []

  def update_health(self, current_health: int):
      """Log the current health of the snake."""
      self.health_log.append(current_health)

  def print_health_log_as_csv(self):
      """Print the recorded health log in CSV format, horizontally."""
      health_values_csv = ",".join(map(str, self.health_log))
      print("Health")
      print(health_values_csv)urn rankings
class AvoidSelfCollisionModule(MoveRankingModule):
  def rank_moves(self, game_state: typing.Dict) -> typing.Dict:
      my_body = game_state["you"]["body"]
      my_head = my_body[0]  # The current position of the snake's head

      # Initialize rankings with a default value for all directions
      rankings = {'up': 1.0, 'down': 1.0, 'left': 1.0, 'right': 1.0}

      # Define potential next positions for the head based on each move
      potential_next_positions = {
          'up': {'x': my_head['x'], 'y': my_head['y'] + 1},
          'down': {'x': my_head['x'], 'y': my_head['y'] - 1},
          'left': {'x': my_head['x'] - 1, 'y': my_head['y']},
          'right': {'x': my_head['x'] + 1, 'y': my_head['y']}
      }

      # Check each potential move for self-collision, excluding the last segment (the tail)
      # because it will move forward on the next turn, vacating the spot.
      for direction, next_pos in potential_next_positions.items():
          # Exclude the tail from the collision check, hence my_body[:-1]
          if any(segment['x'] == next_pos['x'] and segment['y'] == next_pos['y'] for segment in my_body[:-1]):
              rankings[direction] = -100  # Penalize moves leading to self-collision with -100

      return rankings
class LoopAvoidanceModule(MoveRankingModule):
  def __init__(self, history_length=30):
      self.history = []  # History of positions as (x, y) tuples
      self.history_length = history_length

  def rank_moves(self, game_state: typing.Dict) -> typing.Dict:
      my_head = game_state["you"]["body"][0]  # The current position of the snake's head
      # Convert the head position to a tuple for easier comparison
      head_pos = (my_head['x'], my_head['y'])

      # Update history with the current head position
      if head_pos not in self.history:
          self.history.append(head_pos)
          if len(self.history) > self.history_length:
              self.history.pop(0)

      rankings = {'up': 1.0, 'down': 1.0, 'left': 1.0, 'right': 1.0}

      # Potential next positions for the head based on each move
      potential_moves = {
          'up': {'x': my_head['x'], 'y': my_head['y'] + 1},
          'down': {'x': my_head['x'], 'y': my_head['y'] - 1},
          'left': {'x': my_head['x'] - 1, 'y': my_head['y']},
          'right': {'x': my_head['x'] + 1, 'y': my_head['y']}
      }

      for direction, next_head in potential_moves.items():
          next_pos = (next_head['x'], next_head['y'])
          if next_pos in self.history:
              # Penalize moves that lead to positions recently visited
              rankings[direction] = -5

      return rankings
class AStarFoodChasingModule(MoveRankingModule):
  def __init__(self):
      super().__init__()

  def heuristic(self, a, b):
      """Calculate the Manhattan distance between two points, represented as tuples."""
      return abs(a[0] - b[0]) + abs(a[1] - b[1])

  def get_neighbors(self, node, game_state):
      """Generate neighbors for a given node, excluding obstacles, using tuples for points."""
      directions = [(0, 1), (0, -1), (-1, 0), (1, 0)]  # Up, Down, Left, Right
      neighbors = []
      x, y = node
      for dx, dy in directions:
          nx, ny = x + dx, y + dy
          if 0 <= nx < game_state['board']['width'] and 0 <= ny < game_state['board']['height']:
              if not any(part['x'] == nx and part['y'] == ny for part in game_state['you']['body']):
                  neighbors.append((nx, ny))
      return neighbors

  def a_star_search(self, start, goal, game_state):
      """Perform the A* search algorithm using tuples for points."""
      frontier = []
      heapq.heappush(frontier, (0, start))
      came_from = {start: None}
      cost_so_far = {start: 0}

      while frontier:
          current_priority, current = heapq.heappop(frontier)

          if current == goal:
              break

          for next in self.get_neighbors(current, game_state):
              new_cost = cost_so_far[current] + 1
              if next not in cost_so_far or new_cost < cost_so_far[next]:
                  cost_so_far[next] = new_cost
                  priority = new_cost + self.heuristic(next, goal)
                  heapq.heappush(frontier, (priority, next))
                  came_from[next] = current

      return came_from

  def reconstruct_path(self, came_from, start, goal):
      """Reconstruct the path from start to goal using tuples for points."""
      current = goal
      path = []
      while current != start:
          path.append(current)
          current = came_from.get(current)
          if current is None:
              return []  # Return an empty path if we can't reach the goal from start
      path.reverse()
      return path

  def find_closest_food(self, my_head, food):
      """Find the closest piece of food, converting points to tuples."""
      head_tuple = (my_head['x'], my_head['y'])
      food_tuples = [(f['x'], f['y']) for f in food]
      closest_food = min(food_tuples, key=lambda f: self.heuristic(head_tuple, f))
      return closest_food

  def rank_moves(self, game_state: typing.Dict) -> typing.Dict:
      my_head = game_state["you"]["body"][0]
      food_items = game_state["board"]["food"]
      if not food_items:
          return {'up': 0, 'down': 0, 'left': 0, 'right': 0}

      head_tuple = (my_head['x'], my_head['y'])
      closest_food = self.find_closest_food(my_head, food_items)
      came_from = self.a_star_search(head_tuple, closest_food, game_state)

      path = self.reconstruct_path(came_from, head_tuple, closest_food)
      if path:
          first_step = path[0]
          move_rankings = {'up': 0, 'down': 0, 'left': 0, 'right': 0}
          if first_step[0] < head_tuple[0]:
              move_rankings['left'] = 1
          elif first_step[0] > head_tuple[0]:
              move_rankings['right'] = 1
          if first_step[1] > head_tuple[1]:
              move_rankings['up'] = 1
          elif first_step[1] < head_tuple[1]:
              move_rankings['down'] = 1
          return move_rankings

      # If no path is found, default to neutral rankings
      return {'up': 0, 'down': 0, 'left': 0, 'right': 0}
class PreferLargerSpacesModule(MoveRankingModule):
  def initialize_occupied(self, game_state):
      board_width = game_state['board']['width']
      board_height = game_state['board']['height']
      snakes = game_state['board']['snakes']
      my_id = game_state['you']['id']

      # Create a set of all occupied positions by snakes
      occupied = {(segment['x'], segment['y']) for snake in snakes for segment in snake['body']}

      # Mark areas around other snake heads as occupied to simulate potential movement, including diagonals
      for snake in snakes:
          if snake['id'] != my_id:  # Exclude the player's own snake
              head = snake['body'][0]
              for dx in range(-1, 2):  # -1, 0, 1
                  for dy in range(-1, 2):  # -1, 0, 1
                      x, y = head['x'] + dx, head['y'] + dy
                      if 0 <= x < board_width and 0 <= y < board_height:
                          occupied.add((x, y))

      return occupied

  def flood_fill_count(self, start, occupied, board_width, board_height):
      # Initialize flood fill stack with start position and visited set
      stack = [start]
      visited = set()

      # Perform flood fill and count accessible spaces
      while stack:
          x, y = stack.pop()
          if (x, y) in visited or (x, y) in occupied or x < 0 or y < 0 or x >= board_width or y >= board_height:
              continue
          visited.add((x, y))
          # Add adjacent positions
          stack.extend([(x + dx, y + dy) for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]])

      return len(visited)

  def rank_moves(self, game_state: typing.Dict) -> typing.Dict:
      my_head = game_state["you"]["body"][0]
      board_width = game_state['board']['width']
      board_height = game_state['board']['height']
      snake_size = len(game_state["you"]["body"])  # Total size of the snake
      occupied = self.initialize_occupied(game_state)  # Call the new method here

      potential_next_positions = {
          'up': (my_head['x'], my_head['y'] + 1),
          'down': (my_head['x'], my_head['y'] - 1),
          'left': (my_head['x'] - 1, my_head['y']),
          'right': (my_head['x'] + 1, my_head['y'])
      }

      # Adjust rankings for potential moves based on accessible area
      rankings = {}
      for direction, next_pos in potential_next_positions.items():
          if next_pos in occupied:
              rankings[direction] = -100  # Mark as invalid move
              continue

          accessible_area = self.flood_fill_count(next_pos, occupied, board_width, board_height)
          if accessible_area < snake_size:
              deficit = snake_size - accessible_area
              rankings[direction] = -30 * (deficit / snake_size)
          else:
              rankings[direction] = accessible_area

      # Normalize positive scores to the range of 0 to 10
      max_accessible_area = max(rankings.values(), default=1)
      for direction, score in rankings.items():
          if score > 0:
              rankings[direction] = (score / max_accessible_area) * 10

      return rankings








#non module stuff
health_logger = HealthLoggerModule()
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
modules = [AvoidBackwardMoveModule(), modules.AvoidOutOfBoundsModule(), AvoidSelfCollisionModule(),LoopAvoidanceModule(), AvoidOtherSnakesModule(), SmartFoodChasingModule(),  AvoidHeadToHeadCollisionsModule(), PreferLargerSpacesModule()
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
    
    health_logger.print_health_log_as_csv()


# Move Function
def move(game_state: typing.Dict) -> typing.Dict:
    # Your logic for preventing invalid moves

    next_move = decide_move(modules, game_state)
    current_health = game_state["you"]["health"]
    health_logger.update_health(current_health)
    print(f"MOVE {game_state['turn']}: {next_move}")
    return {"move": next_move}

# Main Execution
if __name__ == "__main__":
    from server import run_server
    run_server({"info": info, "start": start, "move": move, "end": end})
