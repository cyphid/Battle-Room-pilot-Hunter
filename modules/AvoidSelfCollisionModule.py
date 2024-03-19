import heapq
import typing

class MoveRankingModule:
  def rank_moves(self, game_state: typing.Dict) -> typing.Dict:
      """
      Returns a dictionary with rankings for each direction.
      Example: {'up': 0.5, 'down': 0.2, 'left': 0.1, 'right': 0.2}
      """
      pass
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