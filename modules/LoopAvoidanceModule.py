import heapq
import typing

class MoveRankingModule:
  def rank_moves(self, game_state: typing.Dict) -> typing.Dict:
      """
      Returns a dictionary with rankings for each direction.
      Example: {'up': 0.5, 'down': 0.2, 'left': 0.1, 'right': 0.2}
      """
      pass
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