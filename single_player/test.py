import os
from importlib import import_module
from random import randint, shuffle

valid_rolls: list[int] = [
    #  -->
    # | 
    # v   Rightmost or lowest is higher.
    41, 41, 42, 42, 43, 43, 
    51, 51, 52, 52, 53, 53, 54, 54, 
    61, 61, 62, 62, 63, 63, 64, 64, 65, 65,
    11, 22, 33, 44, 55, 66, 
    31, 21, 
    32
]

valid_responses: list[int] = set(valid_rolls)
valid_responses.update([0, 1, 2, 3, 4])

def roll() -> int:
    '''Rolls two dices'''
    return valid_rolls[randint(0, 32)]

def geq(a: int, b: int) -> bool:
    return valid_rolls.index(a) >= valid_rolls.index(b)

bots_path = "./bots/"
bots = {}
queue = []
history = []
stats = {}

for bot_file in os.listdir(bots_path):
    if bot_file.endswith('.py'):
        bot_name = os.path.splitext(bot_file)[0]
        
        bots[bot_name] = import_module(f'bots.{bot_name}')

for name, bot in bots.items():
    queue.append(name)

shuffle(queue)

def game(queue: list, start_health: int):
    history = (None,)
    health = {name: start_health for name in queue}
    
    prev_ans = None

    while 1:
        if len(queue) == 1:
            break

        bot = queue.pop()
        ans = bots[bot].answer(prev_ans, prev_ans)
        if ans == 0:
            # Compare [-1] with [-2]
            1
        elif ans == 2:
            # Roll and send
            prev_ans = 2
            queue.insert(0, bot)
        elif ans != 1:
            # Kill bot and give [-1] another roll
            prev_ans = None
            queue.append(queue.pop(0))
            continue
        
        ans = bots[bot].answer(roll(), prev_ans)

        if ans == 2:
            # Roll and send
            prev_ans = 2
            queue.insert(0, bot)
        elif ans not in valid_responses:
            # Kill bot and give [-1] another roll
            prev_ans = None
            queue.append(queue.pop(0))
            continue

        # Send ans to next bot
        prev_ans = ans
        queue.insert(0, bot)
    
    print('Winner: ', queue.pop())

game(queue, 6)        


'''
def call(history: tuple, health: dict, bot_queue: tuple, current_bot) -> (int, int):
    answer = current_bot.aswer(0, history[-1], history[:-1], health)

    if answer == 1:
        answer = current_bot.answer(roll(), history[-1], history[:-1], health)

        if answer == 2:
            return answer, roll()
    
    if answer
'''  