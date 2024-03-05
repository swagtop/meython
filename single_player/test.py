

bot_queue: tuple : (,)
alive_bots: set = {}
health: dict = {}

previous_rounds: tuple = (,)
this_round = lambda : previous_rounds[-1]

previous_rounds.append(0)
previous_rounds.append(1)
print()

previous_rounds.append(0)
print(this_round())

def answer(roll: int, this_round: tuple, previous_rounds: tuple, health: dict, rolled: bool) -> int:
    if not rolled:
        return 1
    else:
        return roll






'''
def call(history: tuple, health: dict, bot_queue: tuple, current_bot) -> (int, int):
    answer = current_bot.aswer(0, history[-1], history[:-1], health)

    if answer == 1:
        answer = current_bot.answer(roll(), history[-1], history[:-1], health)

        if answer == 2:
            return answer, roll()
    
    if answer
'''  