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

def answer_valid(previous: int, current: int) -> bool:
    return (current in valid_responses and geq(current, previous))

bots_path = "./bots/"
bots = {}
queue = []
history = []

for bot_file in os.listdir(bots_path):
    if bot_file.endswith('.py'):
        bot_name = os.path.splitext(bot_file)[0]
        
        bots[bot_name] = import_module(f'bots.{bot_name}')

for name, bot in bots.items():
    queue.append(name)

shuffle(queue)

current = queue.pop()
answer = bots[current].answer(None, roll())
history.append((answer, current))
print(f'My name is {current}, and i answer: {answer}')
if type(answer) != int:
    print(f'{current} has returned an invalid answer: {answer}')
while queue:
    previous = current
    current = queue.pop()
    answer = bots[current].answer(history[-1][0], roll())
    print(f'My name is {current}, and i answer: {answer}')
    if type(answer) != int:
        print(f'{current} has returned an invalid answer: {answer}')
        continue
 
print('Done!')
