roll_rank: list[int] = [
    0, #For first answer in round
    41, 42, 43, 51, 52, 53, 54,
    61, 62, 63, 64, 65, 11, 22,
    33, 44, 55, 66, 31, 21, 32
]

def geq(a: int, b: int) -> bool:
    return roll_rank.index(a) >= roll_rank.index(b)

def begin(rolled, history, health):
    return rolled

def decide(previous, history, health):
    if not geq(previous.answer, previous.previous.answer):
        return 'LIFT'
    if previous.answer == 'ABOVE' and previous.previous.answer == 'ABOVE':
        return 'LIFT'
    return 'ROLL'

def answer(rolled: int, previous: tuple, history: tuple, health: dict):
    if not geq(rolled, previous.answer):
        return 'ABOVE'
    return rolled

def roll_health() -> bool:
    return True

def init(name: str, ):
    global MY_NAME
    MY_NAME = name
    return

