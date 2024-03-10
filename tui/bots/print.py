MY_NAME = ''

def begin(rolled, history, health):
    return rolled

def decide(previous, history, health):
    if previous.answer == 21:
        return 'LIFT'
    return 'ROLL'

def answer(rolled: int, previous: tuple, history: tuple, health: dict):
    return rolled

def roll_health(history, health) -> bool:
    return True

def init(name: str, ):
    global MY_NAME
    MY_NAME = name
    return
