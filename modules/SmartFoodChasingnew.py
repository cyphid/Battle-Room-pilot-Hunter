import typing
import heapq

class SmartFoodChasingModule:
    def __init__(self):
        super().__init__()

    def heuristic(self, a, b):
        """Calculate the Manhattan distance between two points."""
        return abs(a['x'] - b['x']) + abs(a['y'] - b['y'])

    def get_neighbors(self, node, game_state):
        """Generate neighbors for a given node, excluding obstacles."""
        directions = [{'x': 0, 'y': -1}, {'x': 0, 'y': 1}, {'x': -1, 'y': 0}, {'x': 1, 'y': 0}]
        neighbors = []
        for direction in directions:
            nx, ny = node['x'] + direction['x'], node['y'] + direction['y']
            if 0 <= nx < game_state['board']['width'] and 0 <= ny < game_state['board']['height']:
                if not any(part['x'] == nx and part['y'] == ny for snake in game_state['board']['snakes'] for part in snake['body']):
                    neighbors.append({'x': nx, 'y': ny})
        return neighbors

    def a_star_search(self, start, goal, game_state):
        print("something idk")
        frontier = []
        tie_breaker = 0  # Incremental tie-breaker
        heapq.heappush(frontier, (0, tie_breaker, start))  # Include tie_breaker in the tuple
        came_from = {str(start): None}
        cost_so_far = {str(start): 0}
  
        while frontier:
            current_priority, _, current = heapq.heappop(frontier)  # Adjust unpacking to include tie_breaker
        
            if current == goal:
                break
        
            for next in self.get_neighbors(current, game_state):
                new_cost = cost_so_far[str(current)] + 1
                if str(next) not in cost_so_far or new_cost < cost_so_far[str(next)]:
                    cost_so_far[str(next)] = new_cost
                    priority = new_cost + self.heuristic(next, goal)
                    tie_breaker += 1  # Increment tie_breaker
                    heapq.heappush(frontier, (priority, tie_breaker, next))  # Update to include tie_breaker
        
        return came_from


    def reconstruct_path(self, came_from, start, goal):
        """Reconstruct the path from start to goal."""
        current = goal
        path = []
        while current != start:
            path.append(current)
            current = came_from.get(str(current))
            if current is None:
                return []  # Return an empty path if we can't reach the goal from start
        path.reverse()
        return path

    def rank_moves(self, game_state: typing.Dict) -> typing.Dict:
      my_head = game_state["you"]["body"][0]
      food_items = game_state["board"]["food"]
      if not food_items:
          return {'up': 0, 'down': 0, 'left': 0, 'right': 0}
  
      closest_food = min(food_items, key=lambda food: self.heuristic(my_head, food))
      came_from = self.a_star_search(my_head, closest_food, game_state)
  
      path = self.reconstruct_path(came_from, my_head, closest_food)
      if path:
          first_step = path[0] if path else my_head
          move_rankings = {'up': 0, 'down': 0, 'left': 0, 'right': 0}
          # Adjusted the condition to correctly reflect the movement in 2D grid
          if first_step['x'] < my_head['x']:
              move_rankings['left'] = 1
          elif first_step['x'] > my_head['x']:
              move_rankings['right'] = 1
          if first_step['y'] < my_head['y']:  # Y decreases as we go 'up'
              move_rankings['up'] = 1
          elif first_step['y'] > my_head['y']:  # Y increases as we move 'down'
              move_rankings['down'] = 1
          return move_rankings
  
      # If no path is found, default to neutral rankings
      return {'up': 0, 'down': 0, 'left': 0, 'right': 0}
