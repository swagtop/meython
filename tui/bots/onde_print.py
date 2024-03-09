MY_NAME = ''

def begin(rolled, history, health):
    return rolled

def decide(previous, history, health):
    if previous.answer == 21:
        return 'LIFT'
    return 'ROLL'

def answer(rolled: int, previous: tuple, history: tuple[tuple], health: dict[int]) -> int | str:
    return 'ABOVE'

def roll_health() -> bool:
    return True

def init():
    return