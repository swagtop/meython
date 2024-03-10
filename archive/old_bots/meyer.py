def begin(rolled, history, health):
    return 21

def decide(previous, history, health):
    if previous.answer == 21:
        return 'LIFT'
    return 'ROLL'

def answer(roll: int, previous: tuple, history: tuple[tuple], health: dict):
    return 21

def roll_health():
    return True