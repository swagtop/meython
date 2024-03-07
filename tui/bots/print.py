MY_NAME = ''

def answer(roll: int, history: tuple[tuple], health: dict[int]) -> int:
    if history[-1][-1][-1]:
        return roll
    else:
        return 1

def roll_health() -> bool:
    return

def init(name: str, ):
    global MY_NAME
    MY_NAME = name
    return
