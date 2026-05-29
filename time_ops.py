import time
from datetime import datetime
from math_ops import resolve

def run_time(line, variables):

    # time
    if line.startswith('time '):
        name = line[5:].strip()
        variables[name] = datetime.now().strftime('%H:%M:%S')
        return True

    # date
    if line.startswith('date '):
        name = line[5:].strip()
        variables[name] = datetime.now().strftime('%d.%m.%Y')
        return True

    # year
    if line.startswith('year '):
        name = line[5:].strip()
        variables[name] = datetime.now().year
        return True

    # month
    if line.startswith('month '):
        name = line[6:].strip()
        variables[name] = datetime.now().month
        return True

    # day
    if line.startswith('day '):
        name = line[4:].strip()
        variables[name] = datetime.now().day
        return True

    # hour
    if line.startswith('hour '):
        name = line[5:].strip()
        variables[name] = datetime.now().hour
        return True

    # minute
    if line.startswith('minute '):
        name = line[7:].strip()
        variables[name] = datetime.now().minute
        return True

    # sleep
    if line.startswith('sleep '):
        seconds = float(resolve(line[6:].strip(), variables))
        time.sleep(seconds)
        return True

    return False
