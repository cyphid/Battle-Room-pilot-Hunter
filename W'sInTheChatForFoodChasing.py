import typing
import math
from queue import PriorityQueue
class FoodChase(MoveRankingModule):
  def __init__(self):
    pass
  def distance(self, pos1: typing.Dict, pos2: typing.Dict):
    return pos1[0]-pos2[0]+pos1[1]-pos2[1]
  def rank_moves(self, game_state: typing.Dict) -> typing.Dict:
    foods = []
    for food in game_state["board"]["food"]:
      food_in_dict = [food["x"], food["y"]]
      head_in_dict = [game_state["you"]["head"]["x"], game_state["you"]["head"]["y"]]
      current = {}
      # Put pos in dictionary
      current["pos"] = food
      current["all_snakes"] = []
      # Add distance from snake
      for snake in game_state["snakes"]:
        current["all_snakes"][snake["id"]]["distance"] = (self.distance(head_in_dict, food_in_dict))
        current["all_snakes"][snake["id"]]["difference_in_size"] = game_state["you"]["length"] - snake["length"]
      head_in_dict = [game_state["you"]["head"]["x"], game_state["you"]["head"]["y"]]
      food_in_dict = [food["x"], food["y"]]
      current["is_straight_line"] = self.a_star(head_in_dict, food_in_dict)
      
      foods.append(current)
      
    for food in foods:
      dis = food[game_state["you"]["id"]]["distance"]
      dis_float = float(dis)
      #size difference of the two snakes
      snake_size_diff = min(current["all_snakes"], key=lambda snake: snake["distance"])
      dis_y = 20 / ((1 + math.e ** (-0.722 * (snake_size_diff - 1))) - 10)
      #distance of our snake to food
      other_y = -0.0114 * dis_float ** 3 + 0.382 * dis_float ** 2 - 4.47 * dis_float + 22.11
      #
      sum = dis_y+other_y
      food["weight"] = sum

    return foods

  def a_star(pos1, pos2, movecount):
    
  
    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
  
    def a_star_search(start, goal, move_limit):
        frontier = PriorityQueue()
        frontier.put((0, start))
        came_from = {start: None}
        cost_so_far = {start: 0}
  
        while not frontier.empty():
            current = frontier.get()[1]
  
            if current == goal:
                break
  
            for next in [(current[0] + dx, current[1] + dy) for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]]:
                new_cost = cost_so_far[current] + 1  # Assuming cost of 1 for each move
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    if new_cost > move_limit:
                        continue
                    cost_so_far[next] = new_cost
                    priority = new_cost + heuristic(goal, next)
                    frontier.put((priority, next))
                    came_from[next] = current
  
        if goal not in came_from:
            return False  # No path found
        return True  # Path found
  
    # Check if the path exists and is within the movecount
    if a_star_search(pos1, pos2, movecount):
        return 0  # Path found within movecount
    else:
        return 1  # Path not found or exceeds movecount



        

  


y= 20/(a+)
#postion: (X,Y)
#snake1 (difference in size, distance to food)
#











