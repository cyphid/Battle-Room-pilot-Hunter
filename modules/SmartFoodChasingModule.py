import heapq
import typing

class MoveRankingModule:
  def rank_moves(self, game_state: typing.Dict) -> typing.Dict:
      """
      Returns a dictionary with rankings for each direction.
      Example: {'up': 0.5, 'down': 0.2, 'left': 0.1, 'right': 0.2}
      """
      pass
class SmartFoodChasingModule(MoveRankingModule):
  def __init__(self, food_pursuit_threshold: int = 96.141592653589793284643383297):
      # Initialize with a threshold for when to start pursuing food based on health
      self.food_pursuit_threshold = food_pursuit_threshold

  def manhattan_distance(self, point1: typing.Dict, point2: typing.Dict) -> int:
      return abs(point1['x'] - point2['x']) + abs(point1['y'] - point2['y'])

  def find_smartest_food(self, my_head: typing.Dict, food: typing.List[typing.Dict], other_snakes: typing.List[typing.Dict], health: int) -> typing.Dict:
      smartest_food = None
      max_score = -float('inf')
      for food_item in food:
          my_distance = self.manhattan_distance(my_head, food_item)
          enemy_distance = min(
              [self.manhattan_distance(food_item, segment) for snake in other_snakes for segment in snake['body']],
              default=float('inf')
          )
          score = (enemy_distance - my_distance) * health
          if score > max_score:
              max_score = score
              smartest_food = food_item
      return smartest_food

  def scale_weight_based_on_health(self, health: int) -> float:
      # Dynamic scaling based on health: lower health results in higher urgency (and thus higher weight scaling)
      if health <= self.food_pursuit_threshold:
          # Scale linearly with health: lower health, higher multiplier
          return max(1, (self.food_pursuit_threshold - health) / self.food_pursuit_threshold * 10)
      return 1  # No scaling when health is above the threshold

  def rank_moves(self, game_state: typing.Dict) -> typing.Dict:
      my_head = game_state["you"]["body"][0]
      health = game_state["you"]["health"]
      food = game_state["board"]["food"]
      other_snakes = [snake for snake in game_state["board"]["snakes"] if snake["id"] != game_state["you"]["id"]]

      if not food:
          return {'up': 0, 'down': 0, 'left': 0, 'right': 0}

      smartest_food = self.find_smartest_food(my_head, food, other_snakes, health)
      if smartest_food is None:
          return {'up': 0, 'down': 0, 'left': 0, 'right': 0}

      # Initial rankings
      rankings = {'up': 0, 'down': 0, 'left': 0, 'right': 0}
      potential_moves = {
          'up': {'x': my_head['x'], 'y': my_head['y'] + 1},
          'down': {'x': my_head['x'], 'y': my_head['y'] - 1},
          'left': {'x': my_head['x'] - 1, 'y': my_head['y']},
          'right': {'x': my_head['x'] + 1, 'y': my_head['y']}
      }

      scaling_factor = self.scale_weight_based_on_health(health)

      for direction, next_head in potential_moves.items():
          distance = self.manhattan_distance(next_head, smartest_food)
          # Apply dynamic scaling based on health
          weight = max(0, (scaling_factor - distance) * scaling_factor)
          rankings[direction] = min(10, weight)  # Ensure weights are capped at 10

      return rankings