ans = int | str

def last_known(previous: tuple) -> int:
    current = previous
    while current.answer != 0:
        current = current.previous
    return current.answer

high_rolls = {22, 33, 44, 55, 66, 31, 21}
medium_rolls = {61, 62, 63, 64, 65, 11}
low_rolls = {41, 42, 43, 51, 52, 53, 54}

roll_rank = [
    0,
    41, 42, 43, 51, 52, 53, 54,
    61, 62, 63, 64, 65, 11, 22,
    33, 44, 55, 66, 31, 21, 32
]

#-----------------------------------------------------------------------------#
def init():
    return

def begin(rolled: int, history: tuple, health: dict) -> ans:
    return rolled

def decide(previous: tuple, history: tuple, health: dict) -> ans:
    if previous.answer == 'ABOVE' and last_known(previous) in high:
        return 'LIFT'
    if roll_rank.index(previous.answer) < roll_rank.index(previous.previous.answer):
        return 'LIFT'
    return 'ROLL'

def answer(rolled: int, previous: tuple, history: tuple, health: dict) -> ans:
    if roll_rank.index(rolled) >= roll_rank.index(last_known(previous)):
        return rolled
    return 'ABOVE'

def roll_health(history: tuple, health: dict) -> bool:
    return True
#-----------------------------------------------------------------------------#