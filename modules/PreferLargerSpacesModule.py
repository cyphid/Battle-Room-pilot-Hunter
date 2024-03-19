import heapq
import typing

class MoveRankingModule:
  def rank_moves(self, game_state: typing.Dict) -> typing.Dict:
      """
      Returns a dictionary with rankings for each direction.
      Example: {'up': 0.5, 'down': 0.2, 'left': 0.1, 'right': 0.2}
      """
      pass
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