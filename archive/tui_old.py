import os
from importlib import import_module
from random import randint, shuffle
from collections import deque, namedtuple

roll_pool: list[int] = [
    41, 41, 42, 42, 43, 43, 
    51, 51, 52, 52, 53, 53, 54, 54, 
    61, 61, 62, 62, 63, 63, 64, 64, 65, 65,
    11, 22, 33, 44, 55, 66, 
    31, 31, 21, 21, 
    32, 32
]

roll_rank: list[int] = [
    # 0 is nothing, for round start.
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
bots: dict = {}
queue = deque()

def load_bots() -> None:
    for bot_file in os.listdir(bots_path):
        if bot_file.endswith('.py'):
            bot_name = os.path.splitext(bot_file)[0]
            
            bots[bot_name] = import_module(f'bots.{bot_name}')

    for name, bot in bots.items():
        queue.append(name)

    shuffle(queue)

def game(start_health: int) -> str:
    LIFT, ROLL, ABOVE = 100, 200, 300

    load_bots()

    BotAction = namedtuple(
        'BotAction', 
        ['bot', 'answer', 'looked', 'botaction'],
        defaults = [None, None, False, True]
    )
    GameEvent = namedtuple(
        'GameEvent', 
        ['bot', 'answer', 'code', 'botaction'],
        defaults = [None, None, None, False]
    )

    history = ((GameEvent(answer=0),),)
    
    health = {name: start_health for name in queue}

    def damage_bot(bot, meyer=False) -> None:
        if meyer == True:
            health[bot] -= 2
        else:
            health[bot] -= 1

    def log(event: tuple, round_over=False) -> None:
        history = history[:-1] + (history[-1] + event)
        if round_over:
            history = history + (0,)

    while len(queue) > 1:
        print(health)
        print(history[-1])

        bot = queue.pop()
        ans = bots[bot].answer(0, history, dict(health))

        if ans == LIFT:
            #Compare [-1] with [-2]
            if geq(history[-1][-1].ans, history[-1][-2].ans):
                damage_bot(history[-1][-1].bot)
                log((bot, ans), round_over=True)
                queue.append(bot)
                queue.append(queue.pop(0))
            else:
                damage_bot(bot)
                log((bot, ans), round_over=True)
                queue.append(bot)
            continue
        elif ans == ABOVE:
            #Roll and send
            log((bot, ABOVE))
            queue.appendleft(bot)
            continue
        elif ans != ROLL:
            #Dmg bot and retry
            damage_bot(bot)
            log(('lol'), round_over=True)
            queue.append(bot)
            continue

        rolled = roll()
        ans = bots[bot].answer(rolled, history, dict(health))

        if ans == ABOVE:
            #Roll and send
            log((bot, 200, ABOVE), looked=True)
            queue.appendleft(bot)
            continue
        elif ans not in valid_responses:
            #Dmg bot and retry
            damage_bot(bot)
            log('lol', looked=True, round_over=True)
            queue.append(bot)
            continue
        
        log((bot, ans,))
        queue.appendleft(bot)

game(6)