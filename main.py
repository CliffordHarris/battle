# Welcome to
# __________         __    __  .__                               __
# \______   \_____ _/  |__/  |_|  |   ____   ______ ____ _____  |  | __ ____
#  |    |  _/\__  \\   __\   __\  | _/ __ \ /  ___//    \\__  \ |  |/ // __ \
#  |    |   \ / __ \|  |  |  | |  |_\  ___/ \___ \|   |  \/ __ \|    <\  ___/
#  |________/(______/__|  |__| |____/\_____>______>___|__(______/__|__\\_____>
#
# This file can be a nice home for your Battlesnake logic and helper functions.
#
# To get you started we've included code to prevent your Battlesnake from moving backwards.
# For more info see docs.battlesnake.com

import random
import typing


# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
# TIP: If you open your Battlesnake URL in a browser you should see this data
def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "dannnnnnny",  # TODO: Your Battlesnake Username
        "color": "#0096FF",  # TODO: Choose color
        "head": "beluga",  # TODO: Choose head
        "tail": "do-sammy",  # TODO: Choose tail
    }


# start is called when your Battlesnake begins a game
def start(game_state: typing.Dict):
    print("GAME START")


# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
    print("GAME OVER\n")


# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move(game_state: typing.Dict) -> typing.Dict:
    is_move_safe = {"up": True, "down": True, "left": True, "right": True}

    # We've included code to prevent your Battlesnake from moving backwards
    my_head = game_state["you"]["body"][0]  # Coordinates of your head
    my_neck = game_state["you"]["body"][1]  # Coordinates of your "neck"

    if my_neck["x"] < my_head["x"]:  # Neck is left of head, don't move left
        is_move_safe["left"] = False

    if my_neck["x"] > my_head["x"]:  # Neck is right of head, don't move right
        is_move_safe["right"] = False

    if my_neck["y"] < my_head["y"]:  # Neck is below head, don't move down
        is_move_safe["down"] = False

    if my_neck["y"] > my_head["y"]:  # Neck is above head, don't move up
        is_move_safe["up"] = False

    # TODO: Step 1 - Prevent your Battlesnake from moving out of bounds
    board_width = game_state['board']['width']
    board_height = game_state['board']['height']

    if my_head["x"] == 0:
        is_move_safe["left"] = False
    if my_head["x"] == board_width - 1:
        is_move_safe["right"] = False
    if my_head["y"] == 0:
        is_move_safe["down"] = False
    if my_head["y"] == board_height - 1:
        is_move_safe["up"] = False

    # TODO: Step 2 - Prevent your Battlesnake from colliding with itself
    my_body = game_state['you']['body']
    for body_part in my_body:
        if body_part["x"] == my_head["x"] and body_part["y"] == my_head["y"]+1:
            is_move_safe["up"] = False
        if body_part["x"] == my_head["x"] and body_part["y"] == my_head["y"]-1:
            is_move_safe["down"] = False
        if body_part["x"] == my_head["x"]+1 and body_part["y"] == my_head["y"]:
            is_move_safe["right"] = False
        if body_part["x"] == my_head["x"]-1 and body_part["y"] == my_head["y"]:
            is_move_safe["left"] = False

    # TODO: Step 3 - Prevent your Battlesnake from colliding with other Battlesnakes
    opponents = [x["body"] for x in game_state['board']['snakes']]
    for op in opponents:
        for op_body_part in op:
            if op_body_part["x"] == my_head["x"] and op_body_part["y"] == my_head["y"]+1:
                is_move_safe["up"] = False
            if op_body_part["x"] == my_head["x"] and op_body_part["y"] == my_head["y"]-1:
                is_move_safe["down"] = False
            if op_body_part["x"] == my_head["x"]+1 and op_body_part["y"] == my_head["y"]:
                is_move_safe["right"] = False
            if op_body_part["x"] == my_head["x"]-1 and op_body_part["y"] == my_head["y"]:
                is_move_safe["left"] = False

    for snake in game_state['board']['snakes']:
        # Skip our own snake
        if snake['id'] == game_state['you']['id']:
            continue

        opponent_head = snake['head']

        if len(snake['body']) >= len(game_state['you']['body']):
            # Check potential next positions of opponent's head
            possible_opponent_moves = [
                {"x": opponent_head["x"], "y": opponent_head["y"] + 1},  # up
                {"x": opponent_head["x"], "y": opponent_head["y"] - 1},  # down
                {"x": opponent_head["x"] + 1, "y": opponent_head["y"]},  # right
                {"x": opponent_head["x"] - 1, "y": opponent_head["y"]}   # left
            ]

            # Disable moves that could result in head-to-head collision
            for possible_move in possible_opponent_moves:
                if possible_move["x"] == my_head["x"] and possible_move["y"] == my_head["y"] + 1:
                    is_move_safe["up"] = False
                if possible_move["x"] == my_head["x"] and possible_move["y"] == my_head["y"] - 1:
                    is_move_safe["down"] = False
                if possible_move["x"] == my_head["x"] + 1 and possible_move["y"] == my_head["y"]:
                    is_move_safe["right"] = False
                if possible_move["x"] == my_head["x"] - 1 and possible_move["y"] == my_head["y"]:
                    is_move_safe["left"] = False

    # Are there any safe moves left?
    safe_moves = []
    for move, isSafe in is_move_safe.items():
        if isSafe:
            safe_moves.append(move)
    print(f"MOVE {game_state['turn']}")
    print("safemoves", safe_moves)

    if len(safe_moves) == 0:
        print(f"MOVE {game_state['turn']}: No safe moves detected! Moving down")
        return {"move": "down"}

    # Choose a random move from the safe ones
    print(game_state['you']['health'])
    if game_state['you']['health'] < 95:
        where_da_food_at = game_state['board']['food']
    
        print("food", where_da_food_at)
        print("me", my_head)
        closest_food = get_distance_to_food(my_head, where_da_food_at)
        print('closest food', closest_food)
    
        if closest_food:
            move_score = {}
            enemies = [snake for snake in game_state['board']['snakes'] if snake['id'] != game_state['you']['id']]
            for move in safe_moves:
                possible_move = {
                    'up': {'x': my_head['x'], 'y': my_head['y'] + 1},
                    'down': {'x': my_head['x'], 'y': my_head['y'] - 1},
                    'left': {'x': my_head['x'] - 1, 'y': my_head['y']},
                    'right': {'x': my_head['x'] + 1, 'y': my_head['y']}
                }
                move_score[move] = get_manhat_dist(possible_move[move], closest_food)
                
                for snake in enemies:
                    #print("pos move = ",possible_move[move])
                    #print("Opponent = ", snake["head"])
    
                    dist_to_enemy = get_manhat_dist(possible_move[move], snake["head"])
                    if dist_to_enemy > 2:
                        move_score[move] -= 2
    
            scored_moves = [(score, move) for move, score in move_score.items()]
            # Get move with lowest score
            best_score, best_move = min(scored_moves)
            print(best_move)
            return { 'move':best_move }

    print("after food", safe_moves)
    dir = find_space(my_head, opponents, game_state['board']['height'], game_state['board']['width'])
    print(dir)
    if dir in safe_moves:
        return { 'move': dir }
    
    next_move = random.choice(safe_moves)

    # TODO: Step 4 - Move towards food instead of random, to regain health and survive longer
    # food = game_state['board']['food']

    # print(f"MOVE {game_state['turn']}: {next_move}")
    return {"move": next_move}

def find_space(head, opp, h, w):
    bodies = [x for op in opp for x in op]
    print('bodies', bodies, h, w, head)
    vert = h - head["y"] 
    horiz = w - head["x"]
    print(horiz, vert) 
    print("h > v", horiz > vert) 
    if horiz > vert:
        return "right" if horiz > h//2 else "left"
    else:
        return "up" if vert > w//2 else "down"


def get_distance_to_food(head, all_food):
    if not all_food:
        return None


    x = min(all_food, key=lambda food: get_manhat_dist(head, food))
    return x
#    dists = [get_manhat_dist(head, f) for f in all_food]
    #return dists


def get_manhat_dist(head, food):
    return abs(head["x"] - food["x"]) + abs(head["y"] - food["y"])

# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({"info": info, "start": start, "move": move, "end": end})
