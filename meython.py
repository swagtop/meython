from random import randint
from time import time

valid_rolls: list[int] = [41, 41, 42, 42, 43, 43, 51, 51, 52, 52, 53, 53,
                          54, 54, 61, 61, 62, 62, 63, 63, 64, 64, 65, 65,
                          11, 22, 33, 44, 55, 66, 31, 21, 32
                          ]

valid_responses: list[int] = set(valid_rolls)
valid_responses.update([0, 1, 2, 3, 4])

def roll() -> int:
    return valid_rolls[randint(0, 32)]

def geq(a: int, b: int) -> bool:
    return valid_rolls.index(a) >= valid_rolls.index(b)

def answer_valid(previous: int, current: int):
    return (current in valid_responses and geq(current, previous))

if __name__ == '__main__':
    '''
    first = roll()
    second = roll()
    print(f'Is {first} greater or equal {second}?')
    print(geq(first, second))
    print('Valid responses:')
    print(valid_responses)
    '''
    '''
    print(valid_responses)
    start = time()
    for i in range(0, 99999999):
        if roll() in valid_responses:
            1
    print(f'Set time: {time() - start}')
    '''
    print(answer_valid(41, 45))
