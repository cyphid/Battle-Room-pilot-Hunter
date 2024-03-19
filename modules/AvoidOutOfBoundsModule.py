import heapq
import typing

class MoveRankingModule:
  def rank_moves(self, game_state: typing.Dict) -> typing.Dict:
      """
      Returns a dictionary with rankings for each direction.
      Example: {'up': 0.5, 'down': 0.2, 'left': 0.1, 'right': 0.2}
      """
      pass
class AvoidOutOfBoundsModule(MoveRankingModule):
  def rank_moves(self, game_state: typing.Dict) -> typing.Dict:
      my_head = game_state["you"]["body"][0]
      board_width = game_state['board']['width']
      board_height = game_state['board']['height']

      # Default rankings for all directions
      rankings = {'up': 1.0, 'down': 1.0, 'left': 1.0, 'right': 1.0}

      # Set the ranking for moves that go out of bounds to zero
      if my_head['x'] == 0:  # At left edge, can't move left
          rankings['left'] = -100
      if my_head['x'] == board_width - 1:  # At right edge, can't move right
          rankings['right'] = -100
      if my_head['y'] == 0:  # At bottom edge, can't move down
          rankings['down'] = -100
      if my_head['y'] == board_height - 1:  # At top edge, can't move up
          rankings['up'] = -100

      return rankings