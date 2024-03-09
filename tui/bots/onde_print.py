MY_NAME = ''

def answer(roll: int, previous: tuple, history: tuple[tuple], health: dict[int]) -> int | str:
    if history[-1][-1].answer == 'ABOVE':
        return 'ROLL'
    return 41

def roll_health() -> bool:
    return True

def init():
    return