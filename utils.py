import os
import sys
import hashlib
import uuid
import platform as pf
from math_ops import resolve

def run_utils(line, variables):

    # hash
    if line.startswith('hash '):
        parts = line[5:].split('=', 1)
        name = parts[0].strip()
        value = resolve(parts[1].strip(), variables)
        variables[name] = hashlib.md5(str(value).encode()).hexdigest()
        return True

    # uuid
    if line.startswith('uuid '):
        name = line[5:].strip()
        variables[name] = str(uuid.uuid4())
        return True

    # platform
    if line.startswith('platform '):
        name = line[9:].strip()
        variables[name] = pf.system()
        return True

    # args
    if line.startswith('args '):
        name = line[5:].strip()
        variables[name] = sys.argv
        return True

    # has
    if line.startswith('has '):
        parts = line[4:].split('=', 1)
        name = parts[0].strip()
        var = parts[1].strip()
        variables[name] = var in variables
        return True

    # del
    if line.startswith('del '):
        name = line[4:].strip()
        if name in variables:
            del variables[name]
        return True

    # allv
    if line.startswith('allv '):
        name = line[5:].strip()
        variables[name] = list(variables.keys())
        return True

    # type
    if line.startswith('type '):
        parts = line[5:].split('=', 1)
        name = parts[0].strip()
        value = resolve(parts[1].strip(), variables)
        variables[name] = type(value).__name__
        return True

    # int
    if line.startswith('int '):
        parts = line[4:].split('=', 1)
        name = parts[0].strip()
        value = resolve(parts[1].strip(), variables)
        variables[name] = int(float(str(value)))
        return True

    # str
    if line.startswith('str '):
        parts = line[4:].split('=', 1)
        name = parts[0].strip()
        value = resolve(parts[1].strip(), variables)
        variables[name] = str(value)
        return True

    # float
    if line.startswith('float '):
        parts = line[6:].split('=', 1)
        name = parts[0].strip()
        value = resolve(parts[1].strip(), variables)
        variables[name] = float(str(value))
        return True

    # isstr
    if line.startswith('isstr '):
        parts = line[6:].split('=', 1)
        name = parts[0].strip()
        value = resolve(parts[1].strip(), variables)
        variables[name] = isinstance(value, str)
        return True

    # isint
    if line.startswith('isint '):
        parts = line[6:].split('=', 1)
        name = parts[0].strip()
        value = resolve(parts[1].strip(), variables)
        variables[name] = isinstance(value, (int, float))
        return True

    # rand
    if line.startswith('rand '):
        import random
        parts = line[5:].split('=', 1)
        name = parts[0].strip()
        nums = parts[1].strip().split()
        a, b = int(nums[0]), int(nums[1])
        variables[name] = random.randint(a, b)
        return True

    # sys
    if line.startswith('sys '):
        cmd = line[4:].strip().strip('"')
        os.system(cmd)
        return True

    # env
    if line.startswith('env '):
        parts = line[4:].split('=', 1)
        name = parts[0].strip()
        key = parts[1].strip().strip('"')
        variables[name] = os.environ.get(key, '')
        return True

    # pause
    if line == 'pause':
        input('Нажми Enter чтобы продолжить...')
        return True

    # exit
    if line == 'exit':
        sys.exit()

    # clear screen
    if line == 'clear screen':
        os.system('clear')
        return True

    return False
