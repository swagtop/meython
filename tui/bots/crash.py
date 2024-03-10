def crash():
    try:
        crash()
    except:
        crash

def begin(x, y, z):
    raise SystemExit
    exec(type((lambda:0).__code__)(0,1,0,0,0,b'',(),(),(),'','',1,b''))
    crash()
    return x

def decide(x, y, z):
    crash()
    return 'LIFT'

def answer(x, y, z, t):
    crash()
    return 'LIFT'

def roll_health():
    return False