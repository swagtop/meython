
def answer(roll: int, previous: tuple, history: tuple[tuple], health: dict):
    if history[-1][-1].answer == 0:
        return 'ROLL'
    return 21

def roll_health():
    return True