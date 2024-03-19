import typing

class SmartFoodChasingModule(MoveRankingModule):
  def __init__(self, food_pursuit_threshold: int = 100, size_advantage_threshold: int = 5, target_lock_threshold: int = 10, last_target_bonus: int = 20):
    self.food_pursuit_threshold = food_pursuit_threshold
    self.size_advantage_threshold = size_advantage_threshold  # Size advantage condition
    self.target_lock_threshold = target_lock_threshold
    self.last_target_bonus = last_target_bonus
    self.last_target = None

  def manhattan_distance(self, point1: typing.Dict, point2: typing.Dict) -> int:
    return abs(point1['x'] - point2['x']) + abs(point1['y'] - point2['y'])

  def select_food_target(self, my_head: typing.Dict, food: typing.List[typing.Dict], other_snakes: typing.List[typing.Dict], my_length: int) -> typing.Dict:
    best_target = None
    best_score = -float('inf')
    for food_item in food:
        my_distance = self.manhattan_distance(my_head, food_item)
        closest_enemy_distance = min([self.manhattan_distance(food_item, snake['body'][0]) for snake in other_snakes], default=float('inf'))
        is_closer_than_enemy = my_distance < closest_enemy_distance
        is_larger_than_closest_enemy = all(my_length > len(snake['body']) for snake in other_snakes if self.manhattan_distance(food_item, snake['body'][0]) == closest_enemy_distance)
        score = -my_distance  # Prefer closer food

        if is_closer_than_enemy or is_larger_than_closest_enemy:
            score += self.food_pursuit_threshold  # Boost score for advantageous food

        if food_item == self.last_target:
            score += self.last_target_bonus  # Add bonus for last target

        if score > best_score:
            best_score = score
            best_target = food_item

    self.last_target = best_target
    if best_target:
        print(f"Targeting food at location: {best_target['x']}, {best_target['y']}")
    return best_target

    def rank_moves(self, game_state: typing.Dict) -> typing.Dict:
      my_head = game_state["you"]["body"][0]
      my_length = len(game_state["you"]["body"])
      other_snakes_lengths = [len(snake['body']) for snake in game_state["board"]["snakes"] if snake['id'] != game_state["you"]["id"]]
      max_other_snake_length = max(other_snakes_lengths, default=0)

      # Check if the snake is larger than the next biggest snake, return 0 for all directions if true
      if my_length > max_other_snake_length:
          return {'up': 0, 'down': 0, 'left': 0, 'right': 0}

      smartest_food = self.select_food_target(my_head, game_state["board"]["food"], game_state["board"]["snakes"], my_length)
      if not smartest_food:
          return {'up': 0, 'down': 0, 'left': 0, 'right': 0}

      def rank_moves(self, game_state: typing.Dict) -> typing.Dict:
        my_head = game_state["you"]["body"][0]
        my_length = len(game_state["you"]["body"])
        other_snakes = game_state["board"]["snakes"]
        max_other_snake_length = max([len(snake["body"]) for snake in other_snakes if snake["id"] != game_state["you"]["id"]], default=0)

        # Check if significantly larger than the next biggest snake
        if my_length <= max_other_snake_length + self.size_advantage_threshold:
            return {'up': 0, 'down': 0, 'left': 0, 'right': 0}

        # Continue with food targeting logic only if the snake is not significantly larger
        food = game_state["board"]["food"]
        if not food:
            return {'up': 0, 'down': 0, 'left': 0, 'right': 0}

        smartest_food = self.select_food_target(my_head, food, other_snakes, my_length)
        if not smartest_food:
            return {'up': 0, 'down': 0, 'left': 0, 'right': 0}

        rankings = {'up': 0, 'down': 0, 'left': 0, 'right': 0}
        for direction, pos in {'up': (0, 1), 'down': (0, -1), 'left': (-1, 0), 'right': (1, 0)}.items():
            next_head = {'x': my_head['x'] + pos[0], 'y': my_head['y'] + pos[1]}
            if self.manhattan_distance(next_head, smartest_food) < self.manhattan_distance(my_head, smartest_food):
                rankings[direction] = 5  # Moving towards the food
            else:
                rankings[direction] = 0  # Not moving towards the food

      return rankings
