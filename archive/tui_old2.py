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
    0, #For first answer in round
    41, 42, 43, 51, 52, 53, 54,
    61, 62, 63, 64, 65, 11, 22,
    33, 44, 55, 66, 31, 21, 32
]

valid_responses: set = set(roll_pool)
valid_responses.update(['LIFT', 'ROLL', 'ABOVE'])
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
    LIED, WRONG, GIBBERISH, EXCEPTION = 111, 222, 333, 444
    LIFE_ROLLED, DESTROYED = 555, 666

    load_bots()

    RoundStart = namedtuple(
        'RoundStart',
        ['bot', 'answer', 'type'],
        defaults = [None, 0, 'round_start']
    )
    BotAction = namedtuple(
        'BotAction', 
        ['bot', 'answer', 'looked', 'type'],
        defaults = [None, None, False, 'bot_action']
    )
    DamageTaken = namedtuple(
        'DamageTaken',
        ['bot', 'reason', 'amount', 'type'],
        defaults = [None, None, None, 'damage_event']
    )
    LifeRoll = namedtuple(
        'LifeRoll',
        ['bot', 'result', 'type'],
        defaults = [None, None, 'life_roll']
    )
    GameEvent = namedtuple(
        'GameEvent', 
        ['bot', 'code', 'type'],
        defaults = [None, None, None, 'game_event']
    )

    history = ((GameEvent(answer=0),),)
    
    health = {name: start_health for name in queue}

    def log(event: namedtuple, round_over=False) -> None:
        history = history[:-1] + (history[-1] + event)
        if round_over:
            history = history + (RoundStart(answer=0),)
    
    def damage_bot(bot, meyer=False) -> None:
        log(bot, code=TOOK_DMG)
        if meyer == True:
            health[bot] -= 2
        else:
            health[bot] -= 1

    while len(queue) > 1:
        print(health)
        print(history)

        bot = queue.pop()
        ans = bots[bot].answer(0, history, dict(health))

        if ans is 'LIFT':
            log(BotAction(bot, answer='LIFT'))

            prev_ans = history[-1][-1].answer
            if prev_ans == ABOVE:
                prev_ans = roll()

            if geq(prev_ans, history[-1][-2].answer):
                queue.pop(0)
                prev_bot = history[-1][-2].bot
                damage_bot(prev_bot)
                queue.append(bot)
                if not health[prev_bot] > 0:
                    log(GameEvent(prev_bot, code='DIED'))
                    continue
                queue.append(prev_bot)
            else:
                damage_bot(bot)
                if not health[bot] > 0:
                    log(GameEvent(bot, code='DIED'))
                    continue
                queue.append(bot)
            continue
        
        elif ans is 'ABOVE':
            log(BotAction(bot, answer='ABOVE'))
            queue.appendleft(bot)
            continue
        
        elif ans is not 'ROLL':
            log(GameEvent(bot, ans))
        
        rolled = roll()
        ans = bots[bot].answer(rolled, history, dict(health))



                



game(6)