from os import listdir, path
from random import randint, shuffle
from importlib import import_module
from collections import deque, namedtuple

roll_pool: list[int] = [
    41, 41, 42, 42, 43, 43, 
    51, 51, 52, 52, 53, 53, 54, 54, 
    61, 61, 62, 62, 63, 63, 64, 64, 65, 65,
    11, 22, 33, 44, 55, 66, 
    31, 31, 21, 21, 
    32, 32
]

roll_rank: list[int] = [
    0, #For first answer in round
    41, 42, 43, 51, 52, 53, 54,
    61, 62, 63, 64, 65, 11, 22,
    33, 44, 55, 66, 31, 21, 32
]

valid_begin: set = set(roll_pool)
valid_begin.remove(32)

valid_decide: set = set(['LIFT', 'ROLL', 'ABOVE'])

valid_answer: set = set(valid_begin)
valid_answer.update(['ABOVE'])

def roll() -> int:
    '''Rolls two dices'''
    return roll_pool[randint(0, len(roll_pool) - 1)]

def geq(a: int, b: int) -> bool:
    return roll_rank.index(a) >= roll_rank.index(b)

bots_path = path.join(path.dirname(path.abspath(__file__)), "bots")
bots: dict = {}
queue = deque()
has_rolled = set()

def load_bots():
    for bot_file in listdir(bots_path):
        if bot_file.endswith('.py'):
            bot_name = path.splitext(bot_file)[0]
            
            bots[bot_name] = import_module(f'bots.{bot_name}')

    for name, bot in bots.items():
        queue.append(name)

    shuffle(queue)

def parse_entry(entry: tuple) -> str:
    result = f'{entry.bot} '
    for character in entry.events:
        match character:
            case 'b':
                result += 'begins round, '
            case 's':
                result += f'says they rolled {entry.answer}'
            case 'r':
                result += 'rolls and looks into the cup, '
            case 'a':
                result += 'says above, rolls and sends'
            case 'l':
                result += 'lifts the cup, '
            case 'b':
                result += 'its group toast!'
            case 'c':
                result += 'takes '
            case 'p':
                result += 'deals '
            case 'n':
                result += 'normal damage, '
            case 'm':
                result += 'meyer damage, '
            case 't':
                result += 'because they rolled too low'
            case 'f':
                result += 'because they were wrong'
            case 'u':
                result += 'because they lied'
            case 'i':
                result += 'because of invalid response'
            case 'e':
                result += 'because of exception'
            case 'z':
                result += 'because they were too slow'
            case 'x':
                result += ', and dies!'
            case 'h':
                result += ', and rolls for health'
            case ' ':
                result += f', {entry.events.split()[1]} was in the cup.'
    return result

def game(max_health=6, normal_damage=1, meyer_damage=2, timeout_seconds=1):
    from random import randint, shuffle
    MAX_HEALTH = max_health
    HALFWAY = max_health // 2
    NORMAL_DAMAGE = normal_damage
    MEYER_DAMAGE = meyer_damage
    TIMEOUT_SECONDS = timeout_seconds

    LogEntry = namedtuple(
        'LogEntry',
        ['bot', 'answer', 'events', 'previous']
    )

    load_bots()

    history = (
        tuple(),
    )
    health = {name: MAX_HEALTH for name in queue}
    
    def damage(bot: str, slot_one=None, slot_two=None, slot_three=None) -> str:
        '''
        Damages bot, and returns characters to attatch to event string,
        that documents if the damage taken was normal, or meyer, and
        attatches an h or x depending on if the bot rolled for health,
        or died.
        '''
        ev = ''
        if slot_one == 21 or slot_two == 21 or slot_three == 21:
            ev += 'm'
            health[bot] -= MEYER_DAMAGE
        else:
            ev += 'n'
            health[bot] -= NORMAL_DAMAGE

        if health[bot] < 0:
            queue.remove(bot)
            return ev + 'x'
        elif health[bot] == HALFWAY and bot not in has_rolled:
            has_rolled.update(bot)
            rolls = bots[bot].roll_health()
            if rolls:
                health[bot] = randint(1, MAX_HEALTH)
                return ev + 'h'
            else:
                return ev

        return ev
    
    def log(bot: str, answer: int, events: str, continue_round=False):
        nonlocal history
        nonlocal round_start
        if round_start:
            previous = LogEntry(None, 0, 'b', None)
        else:
            previous = history[-1][-1]
        history = history[:-1] + (
            history[-1] + ((
                LogEntry(
                    bot, 
                    answer, 
                    events, 
                    previous
                )
            ),),
        )
        if not continue_round:
            history = history + (
                tuple(),
            )
            round_start = True
            in_cup = None
    
    def print_history(history: tuple):
        i = 1
        for round in history:
            print('ROUND:', i)
            i += 1
            for entry in round:
                print(parse_entry(entry))

    round_start = True
    in_cup = None
    last_known = None

    while len(queue) > 1:
        print(queue)

        ev = ''
        bot = queue[-1]

        if round_start:
            ev += 'b'
            in_cup = roll()
            if in_cup == 32:
                ev += 'g'
                log(bot, None, ev)
                continue
            try:
                ans = bots[bot].begin(in_cup, history, dict(health))
            except (Exception, SystemExit) as e:
                # DAMAGE BOT
                print(e)
                ev += 'cde' + damage(bot)
                log(bot, None, ev)
                continue
            except TimeoutError as e:
                # DAMAGE BOT
                print(e)
                ev += 'cdz' + damage(bot)
                log(bot, None, ev)
                print(e)
                continue

            if ans not in valid_begin:
                # DAMAGE BOT
                ev += 'scdi' + damage(bot)
                log(bot, ans, ev)
                continue
            ev += 's'
            log(bot, ans, ev, continue_round=True)
            queue.rotate(1)
            round_start = False
            continue
        
        prev = history[-1][-1]

        try:
            ans = bots[bot].decide(prev, history, dict(health))
        except Exception as e:
            # DAMAGE BOT
            print(e)
            ev += 'cde' + damage(bot)
            log(bot, None, ev)
            continue
        if ans not in valid_decide:
            # DAMAGE BOT
            ev += 'cdi' + damage(bot)
            log(bot, ans, ev)
            continue
        
        if ans == 'LIFT' and (in_cup == None or prev.answer == 0):
            # DAMAGE BOT
            ev += 'lcdi' + damage(bot)
            log(bot, 'LIFT', ev)
            continue
        
        if ans == 'LIFT' and prev.answer == 'ABOVE':
            in_cup = roll()

            if not geq(in_cup, last_known):
                # DAMAGE LAST BOT
                ev += 'lpdt' + damage(prev.bot, in_cup, last_known) + f' {in_cup}'
            else:
                # DAMAGE BOT
                ev += 'lcdf' + damage(bot, in_cup, last_known) + f' {in_cup}'
            log(bot, 'LIFT', ev)
            continue
        
        if ans == 'LIFT' and prev.answer != 'ABOVE':
            if not geq(in_cup, prev.answer):
                # DAMAGE LAST BOT
                ev += 'lpdt' + damage(prev.bot, in_cup, prev.answer, prev.previous.answer) + f' {in_cup}'
            else:
                # DAMAGE BOT
                ev += 'lcdf' + damage(bot, in_cup, prev.answer, prev.previous.answer) + f' {in_cup}'
            log(bot, 'LIFT', ev)
            continue
            
        if ans == 'ABOVE' and prev.answer == 0:
            # DAMAGE BOT
            ev += 'acdi' + damage(bot)
            log(bot, 'ABOVE', ev)
            continue
        
        if ans == 'ABOVE' and prev.answer != 0:
            # ROLL AND SEND
            ev += 'a'
            if prev.answer != 'ABOVE':
                last_known = prev.answer
            log(bot, 'ABOVE', ev, continue_round=True)
            queue.rotate(1)
            continue

        if not ans == 'ROLL':
            # DAMAGE BOT
            ev += 'rcdi'
            log(bot, ans, ev)
            continue

        ev += 'r'
        in_cup = roll()
        if in_cup == 32:
            ev += 'g'
            log(bot, None, ev)
            continue
        try:
            ans = bots[bot].answer(in_cup, prev, history, dict(health))
        except (Exception, SystemExit):
            # DAMAGE BOT
            ev += 'cde' + damage(bot, prev.answer)
            log(bot, None, ev)
            continue
        if ans == 'ROLL' or ans == 'LIFT':
            # DAMAGE BOT
            if ans == 'ROLL':
                ev += 'r'
            elif ans == 'LIFT':
                ev += 'l'
            ev += 'cdi' + damage(bot, prev.answer)
            log(bot, ans, ev)
            continue
        if ans not in valid_answer:
            # DAMAGE BOT
            ev += 'cdi' + damage(bot, prev.answer)
            log(bot, ans, ev)
            continue
        if ans == 'ABOVE':
            # ROLL AND SEND
            if prev.answer != 'ABOVE':
                last_known = prev.answer
            ev += 'a'
            log(bot, 'ABOVE', ev, continue_round=True)
            queue.rotate(1)
            continue


        ev += 's'
        log(bot, ans, ev, continue_round=True)
        queue.rotate(1)
    
    print_history(history)
    print('Winner is: ', queue[0])
    print('Health:\n', health[queue[0]])

game(max_health=6)