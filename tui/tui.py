
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

def load_bots() -> deque:
    from os import listdir, path
    from importlib import import_module
    from collections import deque
    queue = deque()
    for bot_file in listdir(bots_path):
        if bot_file.endswith('.py'):
            bot_name = path.splitext(bot_file)[0]
            
            bots[bot_name] = import_module(f'bots.{bot_name}')

    for name, bot in bots.items():
        queue.append(name)
    return queue


def game(max_health=6, normal_damage=1, meyer_damage=2)
    from random import randint, shuffle
    MAX_HEALTH = max_health
    NORMAL_DAMAGE = normal_damage
    MEYER_DAMAGE = meyer_damage

    LogEntry = namedtuple(
        'LogEntry',
        ['bot', 'answer', 'events']
    )

    in_cup = None

    queue = shuffle(load_bots())
    history = ((LogEntry(None, 0, 'b'), ), )
    health = {name: MAX_HEALTH for name in queue}
    
    def damage(bot: str, amount: int):
        health[bot] -= amount
    
    def log(entry: tuple, round_over=False):
        history = history[:-1] + (history[-1] + entry)
        if round_over:
            history = history + (LogEntry(None, 0, 'b'),)

    while len(queue) > 1:

        bot = queue[-1]
        try:
            ans = bots[bot].answer(0, history, dict(health))
        except Exception:
            # DAMAGE BOT
            damage(bot, NORMAL_DAMAGE)
            log(LogEntry(bot, None, 'cde'))
            continue

        if ans is 'LIFT':
            if in_cup is None:
                # DAMAGE BOT
                damage(bot, NORMAL_DAMAGE)
                log(LogEntry(bot, 'LIFT', 'lcdi'))
                continue
            
            prev_bot = history[-1][-1]
            prev_prev_bot = history[-1][-2]

            if prev_ans is 'ABOVE':
                in_cup = roll()

                if not geq(in_cup, prev_prev_bot.answer):
                    # DAMAGE LAST BOT
                    damage(prev_bot, NORMAL_DAMAGE)
                    log(LogEntry(bot, 'LIFT', f'lpdt {in_cup}'))
                    queue.rotate(-1)
                else:
                    # DAMAGE BOT
                    damage(bot, NORMAL_DAMAGE)
                    log(LogEntry(bot, 'LIFT', f'lcdf {in_cup}'))
                continue
            
            else:
                if not geq(in_cup, prev_bot.answer):
                    # DAMAGE LAST BOT
                    damage(prev_bot, NORMAL_DAMAGE)
                    log(LogEntry(bot, 'LIFT', f'lpdl {in_cup}'))
                    queue.rotate(-1)
                else:
                    # DAMAGE BOT
            
            else:
                if not geq(in_cup, prev_prev_bot.answer):
                    # DAMAGE LAST BOT
                    queue.rotate(-1)
                else:
                    # DAMAGE BOT

        elif ans is 'ABOVE':
            # ROLL AND SEND

        elif ans is not 'ROLL':
            # DAMAGE BOT

        in_cup = roll()
        try:
            ans = bots[bot].answer(in_cup, history, dict(health))
        except Exception:
            # DAMAGE BOT

        if ans is 'ABOVE':
            # ROLL AND SEND

        if ans not in valid_responses:
            # DAMAGE BOT


    
