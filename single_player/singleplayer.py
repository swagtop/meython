import os
from importlib import import_module

bots_path = "./bots/"
bots = {}

for bot_file in os.listdir(bots_path):
    if bot_file.endswith('.py'):
        bot_name = os.path.splitext(bot_file)[0]
        
        bots[bot_name] = import_module(f'bots.{bot_name}')

for name, bot in bots.items():
    ans = bot.answer(1, 1)
    print(f'My name is {name} bot and i answer: {ans}!')
