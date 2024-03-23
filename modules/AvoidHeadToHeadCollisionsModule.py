import heapq
import typing

class MoveRankingModule:
  def rank_moves(self, game_state: typing.Dict) -> typing.Dict:
      """
      Returns a dictionary with rankings for each direction.
      Example: {'up': 0.5, 'down': 0.2, 'left': 0.1, 'right': 0.2}
      """
      pass

class AvoidHeadToHeadCollisionsModule(MoveRankingModule):
  def rank_moves(self, game_state: typing.Dict) -> typing.Dict:
      my_head = game_state["you"]["body"][0]
      my_length = len(game_state["you"]["body"])
      other_snakes = game_state["board"]["snakes"]
      my_snake_id = game_state["you"]["id"]

      # Default rankings for all directions
      rankings = {'up': 1.0, 'down': 1.0, 'left': 1.0, 'right': 1.0}

      # Potential next positions for the head based on each move
      potential_moves = {
          'up': {'x': my_head['x'], 'y': my_head['y'] + 1},
          'down': {'x': my_head['x'], 'y': my_head['y'] - 1},
          'left': {'x': my_head['x'] - 1, 'y': my_head['y']},
          'right': {'x': my_head['x'] + 1, 'y': my_head['y']}
      }

      # Check each potential move for head-to-head collision risks
      for direction, next_head in potential_moves.items():
          for snake in other_snakes:
              if snake["id"] != my_snake_id:
                  enemy_head = snake["body"][0]
                  enemy_length = len(snake["body"])
                  if abs(next_head['x'] - enemy_head['x']) + abs(next_head['y'] - enemy_head['y']) == 1:
                      if enemy_length >= my_length:
                          # Penalize moves that lead to head-to-head with longer or equal-length snakes
                          rankings[direction] = -50
                      else:
                          # Reward moves that lead to head-to-head with smaller snakes
                          rankings[direction] += 10  # Or any other value that you deem appropriate

      return rankings
