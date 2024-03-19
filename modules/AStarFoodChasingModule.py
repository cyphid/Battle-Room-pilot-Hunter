import heapq
import typing

class MoveRankingModule:
  def rank_moves(self, game_state: typing.Dict) -> typing.Dict:
      """
      Returns a dictionary with rankings for each direction.
      Example: {'up': 0.5, 'down': 0.2, 'left': 0.1, 'right': 0.2}
      """
      pass

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