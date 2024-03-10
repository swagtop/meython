MY_NAME = ''

roll_rank: list[int] = [
    0, #For first answer in round
    41, 42, 43, 51, 52, 53, 54,
    61, 62, 63, 64, 65, 11, 22,
    33, 44, 55, 66, 31, 21, 32
]

def geq(a: int, b: int) -> bool:
    return roll_rank.index(a) >= roll_rank.index(b)

roll_bank = []

def begin(rolled, history, health):
    return rolled

def decide(previous, history, health):
    return 'ABOVE'

def answer(rolled: int, previous: tuple, history: tuple[tuple], health: dict):
    return 'ABOVE'

def roll_health():
    return True

def init():
    return