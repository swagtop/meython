import os
from importlib import import_module
from random import randint, shuffle
from collections import deque

roll_pool: int list = [
    #  -->
    # | 
    # v   Rightmost or lowest is higher.
    41, 41, 42, 42, 43, 43, 
    51, 51, 52, 52, 53, 53, 54, 54, 
    61, 61, 62, 62, 63, 63, 64, 64, 65, 65,
    11, 22, 33, 44, 55, 66, 
    31, 31, 21, 21, 
    32, 32
]

roll_rank: int list = [
    # 0 is nothing, for when the round starts.
    0,
    41, 42, 43, 51, 52, 53, 54,
    61, 62, 63, 64, 65, 11, 22,
    33, 44, 55, 66, 31, 21, 32
]

valid_responses: set = set(roll_pool)
valid_responses.update([100, 200, 300])
valid_responses.remove(32)

def roll() -> int:
    '''Rolls two dices'''
    return roll_pool[randint(0, len(valid_rolls) - 1)]

def geq(a: int, b: int) -> bool:
    return roll_rank.index(a) >= roll_rank.index(b)

bots_path = "./bots/"
bots = {}
queue = deque()
stats = {}

def load_bots() -> None:
    for bot_file in os.listdir(bots_path):
        if bot_file.endswith('.py'):
            bot_name = os.path.splitext(bot_file)[0]
            
            bots[bot_name] = import_module(f'bots.{bot_name}')

    for name, bot in bots.items():
        queue.append(name)

    shuffle(queue)

def game(queue: list, start_health: int) -> str:
    load_bots()

    history = (0,)
    health = {name: start_health for name in queue}

    def damage_bot(bot) -> None:
        health[bot] -= 1

    prev_ans = 0

    while len(queue) > 1:

        bot = queue.pop()