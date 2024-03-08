from os import listdir, path
from random import randint, shuffle
from importlib import import_module
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
    return roll_pool[randint(0, len(roll_pool) - 1)]

def geq(a: int, b: int) -> bool:
    return roll_rank.index(a) >= roll_rank.index(b)

bots_path = "./bots/"
bots: dict = {}
queue = deque()

def load_bots():
    for bot_file in listdir(bots_path):
        if bot_file.endswith('.py'):
            bot_name = path.splitext(bot_file)[0]
            
            bots[bot_name] = import_module(f'bots.{bot_name}')

    for name, bot in bots.items():
        queue.append(name)

    shuffle(queue)

def game(max_health=6, normal_damage=1, meyer_damage=2):
    from random import randint, shuffle
    MAX_HEALTH = max_health
    NORMAL_DAMAGE = normal_damage
    MEYER_DAMAGE = meyer_damage

    LogEntry = namedtuple(
        'LogEntry',
        ['bot', 'answer', 'events']
    )

    load_bots()

    in_cup = None

    history = (
        (LogEntry(None, 0, 'b'), ),
    )
    health = {name: MAX_HEALTH for name in queue}
    
    def damage(bot: str, amount: int):
        print(bot, 'takes', amount, 'damage')
        health[bot] -= amount
        if health[bot] < 1:
            queue.remove(bot)
    
    def log(entry: tuple, continue_round=False):
        nonlocal history
        print(entry)
        history = history[:-1] + (history[-1] + (entry,),)
        if not continue_round:
            history = history + ((LogEntry(None, 0, 'b'),),)
            in_cup = None

    while len(queue) > 1:

        bot = queue[-1]
        try:
            ans = bots[bot].answer(0, history, dict(health))
        except Exception:
            # DAMAGE BOT
            damage(bot, NORMAL_DAMAGE)
            log(LogEntry(bot, None, 'cde'))
            continue

        if ans == 'LIFT':
            if in_cup is None:
                # DAMAGE BOT
                damage(bot, NORMAL_DAMAGE)
                log(LogEntry(bot, 'LIFT', 'lcdi'))
                continue
            
            prev_bot = history[-1][-1]
            prev_prev_bot = history[-1][-2]

            if prev_ans == 'ABOVE':
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
            
            else:
                if not geq(in_cup, prev_bot.answer):
                    # DAMAGE LAST BOT
                    damage(prev_bot, NORMAL_DAMAGE)
                    log(LogEntry(bot, 'LIFT', f'lpdu {in_cup}'))
                    queue.rotate(-1)
                else:
                    # DAMAGE BOT
                    damage(bot, NORMAL_DAMAGE)
                    log(LogEntry(bot, 'LIFT', f'lcdf {in_cup}'))
                continue

            if not geq(in_cup, prev_prev_bot.answer):
                # DAMAGE LAST BOT
                damage(prev_bot, NORMAL_DAMAGE)
                log(LogEntry(bot, 'LIFT', f'lpdt {in_cup}'))
                queue.rotate(-1)
            else:
                # DAMAGE BOT
                damage(bot, NORMAL_DAMAGE)
                log(LogEntry(bot, 'LIFT', f'lpdf {in_cup}'))
            continue

        elif ans == 'ABOVE':
            # ROLL AND SEND
            log(LogEntry(bot, 'ABOVE', 'a'), continue_round=True)
            queue.rotate(1)
            continue

        elif ans != 'ROLL':
            # DAMAGE BOT
            damage(bot, NORMAL_DAMAGE)
            log(LogEntry(bot, ans, 'cdi'))
            continue


        in_cup = roll()
        try:
            ans = bots[bot].answer(in_cup, history, dict(health))
        except Exception:
            # DAMAGE BOT
            damage(bot, NORMAL_DAMAGE)
            log(LogEntry(bot, None, 'rcde'))
            continue

        if ans == 'ABOVE':
            # ROLL AND SEND
            log(LogEntry(bot, 'ABOVE', 'ra'), continue_round=True)
            queue.rotate(1)
            continue

        elif ans == 'ROLL':
            # DAMAGE BOT
            damage(bot, NORMAL_DAMAGE)
            log(LogEntry(bot, ans, 'rcdi'))
            continue

        elif ans not in valid_responses:
            # DAMAGE BOT
            damage(bot, NORMAL_DAMAGE)
            log(LogEntry(bot, ans, 'rcdi'))
            continue

        else:
            log(LogEntry(bot, ans, 'rs'), continue_round=True)
            queue.rotate(1)
    
    print('History:\n', history)
    print('Winner is: ', queue[0])

game()