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
    31, 31, 21, 21, 
    32, 32
]

valid_responses: set = set(valid_rolls)
valid_responses.update([0, 1, 2, 3, 4])

def roll() -> int:
    '''Rolls two dices'''
    return valid_rolls[randint(0, len(valid_rolls) - 1)]

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
    
    def bot_dead(bot) -> bool:
        health[bot] -= 1
        if health[bot] == 0:
            return True
        return False
    
    prev_ans = 4

    while len(queue) > 1:
        print(health)

        bot = queue.pop()
        ans = bots[bot].answer(prev_ans, 4)
        if ans == 0:
            if prev_ans == 2:
                prev_ans = roll()
            # Compare [-1] with [-2]
            if geq(prev_ans, prev_ans):
                if bot_dead(queue[0]):
                    queue.pop(0)
                    queue.insert(0, bot)
            continue

        elif ans == 2:
            # Roll and send
            prev_ans = 2
            queue.insert(0, bot)
            continue
        elif ans != 1:
            # Damage bot and give [-1] another roll
            if bot_dead(bot):
                queue.pop(0)
                queue.insert(0, bot)
            else:
                prev_ans = 4
                queue.append(bot)
            continue
        
        ans = bots[bot].answer(roll(), prev_ans)

        if ans == 2:
            # Roll and send
            prev_ans = 2
            queue.insert(0, bot)
        elif ans not in valid_responses:
            # Damage bot and give [-1] another roll
            if bot_dead(bot):
                queue.pop(0)
                queue.insert(0, bot)
            else:
                prev_ans = 4
                queue.append(bot)
            continue

        # Send ans to next bot
        prev_ans = ans
        queue.insert(0, bot)
    
    print('Winner: ', queue.pop())

game(queue, 600000000)        


'''
def call(history: tuple, health: dict, bot_queue: tuple, current_bot) -> (int, int):
    answer = current_bot.aswer(0, history[-1], history[:-1], health)

    if answer == 1:
        answer = current_bot.answer(roll(), history[-1], history[:-1], health)

        if answer == 2:
            return answer, roll()
    
    if answer
'''  