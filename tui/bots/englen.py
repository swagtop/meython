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

def answer(roll: int, previous: tuple, history: tuple[tuple], health: dict):
    prev = history[-1][-1]
    prev_prev = history[-1][-2]
    if roll != 0:
        return 'LIFT'
    else:
        if roll_bank.count('ABOVE') < 4:
            roll_bank.append('ABOVE')
            return 'ABOVE'
        else:
            return 'LIFT'


def roll_health():
    return True
