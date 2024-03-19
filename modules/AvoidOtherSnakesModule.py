import heapq
import typing

class MoveRankingModule:
  def rank_moves(self, game_state: typing.Dict) -> typing.Dict:
      """
      Returns a dictionary with rankings for each direction.
      Example: {'up': 0.5, 'down': 0.2, 'left': 0.1, 'right': 0.2}
      """
      pass
class AvoidOtherSnakesModule(MoveRankingModule):
  def rank_moves(self, game_state: typing.Dict) -> typing.Dict:
      my_head = game_state["you"]["body"][0]  # The current position of the snake's head
      other_snakes = game_state["board"]["snakes"]
      my_snake_id = game_state["you"]["id"]

      rankings = {'up': 1.0, 'down': 1.0, 'left': 1.0, 'right': 1.0}

      # Potential next positions for the head based on each move
      potential_moves = {
          'up': {'x': my_head['x'], 'y': my_head['y'] + 1},
          'down': {'x': my_head['x'], 'y': my_head['y'] - 1},
          'left': {'x': my_head['x'] - 1, 'y': my_head['y']},
          'right': {'x': my_head['x'] + 1, 'y': my_head['y']}
      }

      # Check each potential move for danger from other snakes
      for direction, next_head in potential_moves.items():
          for snake in other_snakes:
              if snake["id"] == my_snake_id:
                  continue  # Ignore own snake's body
              # Exclude the last segment of the snake's body
              for segment in snake["body"][:-1]:
                  if next_head['x'] == segment['x'] and next_head['y'] == segment['y']:
                      rankings[direction] = -100  # Highly penalize moves leading to collision with other snakes

      return rankings