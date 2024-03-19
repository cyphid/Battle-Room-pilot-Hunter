import heapq
import typing

class MoveRankingModule:
  def rank_moves(self, game_state: typing.Dict) -> typing.Dict:
      """
      Returns a dictionary with rankings for each direction.
      Example: {'up': 0.5, 'down': 0.2, 'left': 0.1, 'right': 0.2}
      """
      pass
class AvoidBackwardMoveModule(MoveRankingModule):
  def rank_moves(self, game_state: typing.Dict) -> typing.Dict:
      my_head = game_state["you"]["body"][0]
      my_neck = game_state["you"]["body"][1]

      # Default rankings for all directions
      rankings = {'up': 1.0, 'down': 1.0, 'left': 1.0, 'right': 1.0}

      # Set the ranking for the backward move to zero
      if my_neck['x'] < my_head['x']:  # Neck is left of head, set moving left to zero
          rankings['left'] = -100
      elif my_neck['x'] > my_head['x']:  # Neck is right of head, set moving right to zero
          rankings['right'] = -100
      elif my_neck['y'] < my_head['y']:  # Neck is below head, set moving down to zero
          rankings['down'] = -100
      elif my_neck['y'] > my_head['y']:  # Neck is above head, set moving up to zero
          rankings['up'] = -100

      return rankings