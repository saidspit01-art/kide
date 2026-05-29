import random
from math_ops import resolve

def run_lists(line, variables):

    # list
    if line.startswith('list '):
        parts = line[5:].split('=', 1)
        name = parts[0].strip()
        if ',' in parts[1]:
            items = [resolve(x.strip(), variables) for x in parts[1].split(',')]
            variables[name] = items
        else:
            variables[name] = []
        return True

    # app
    if line.startswith('app '):
        parts = line[4:].split(',', 1)
        name = parts[0].strip()
        value = resolve(parts[1].strip(), variables)
        if name in variables and isinstance(variables[name], list):
            variables[name].append(value)
        return True

    # dda
    if line.startswith('dda '):
        parts = line[4:].split(',', 1)
        name = parts[0].strip()
        value = resolve(parts[1].strip(), variables)
        if name in variables and isinstance(variables[name], list):
            variables[name].remove(value)
        return True

    # sort
    if line.startswith('sort '):
        name = line[5:].strip()
        if name in variables and isinstance(variables[name], list):
            variables[name].sort()
        return True

    # reverse
    if line.startswith('reverse '):
        name = line[8:].strip()
        if name in variables and isinstance(variables[name], list):
            variables[name].reverse()
        return True

    # first
    if line.startswith('first '):
        parts = line[6:].split('=', 1)
        name = parts[0].strip()
        lst = resolve(parts[1].strip(), variables)
        if isinstance(lst, list):
            variables[name] = lst[0]
        return True

    # last
    if line.startswith('last '):
        parts = line[5:].split('=', 1)
        name = parts[0].strip()
        lst = resolve(parts[1].strip(), variables)
        if isinstance(lst, list):
            variables[name] = lst[-1]
        return True

    # count
    if line.startswith('count '):
        parts = line[6:].split('=', 1)
        name = parts[0].strip()
        items = parts[1].strip().split(',')
        lst = resolve(items[0].strip(), variables)
        value = resolve(items[1].strip(), variables)
        variables[name] = lst.count(value) if isinstance(lst, list) else str(lst).count(str(value))
        return True

    # index
    if line.startswith('index '):
        parts = line[6:].split('=', 1)
        name = parts[0].strip()
        items = parts[1].strip().split(',')
        lst = resolve(items[0].strip(), variables)
        value = resolve(items[1].strip(), variables)
        variables[name] = lst.index(value) if isinstance(lst, list) else -1
        return True

    # insert
    if line.startswith('insert '):
        parts = line[7:].split(',')
        name = parts[0].strip()
        idx = int(resolve(parts[1].strip(), variables))
        value = resolve(parts[2].strip(), variables)
        if name in variables and isinstance(variables[name], list):
            variables[name].insert(idx, value)
        return True

    # clear
    if line.startswith('clear '):
        name = line[6:].strip()
        if name in variables and isinstance(variables[name], list):
            variables[name].clear()
        return True

    # copy
    if line.startswith('copy '):
        parts = line[5:].split('=', 1)
        name = parts[0].strip()
        value = resolve(parts[1].strip(), variables)
        if isinstance(value, list):
            variables[name] = value.copy()
        return True

    # exp
    if line.startswith('exp '):
        parts = line[4:].split(',', 1)
        name = parts[0].strip()
        other = resolve(parts[1].strip(), variables)
        if name in variables and isinstance(variables[name], list):
            variables[name].extend(other)
        return True

    # slice
    if line.startswith('slice '):
        parts = line[6:].split('=', 1)
        name = parts[0].strip()
        items = parts[1].strip().split(',')
        lst = resolve(items[0].strip(), variables)
        a = int(resolve(items[1].strip(), variables))
        b = int(resolve(items[2].strip(), variables))
        variables[name] = lst[a:b]
        return True

    # shuffle
    if line.startswith('shuffle '):
        name = line[8:].strip()
        if name in variables and isinstance(variables[name], list):
            random.shuffle(variables[name])
        return True

    # choice
    if line.startswith('choice '):
        parts = line[7:].split('=', 1)
        name = parts[0].strip()
        lst = resolve(parts[1].strip(), variables)
        variables[name] = random.choice(lst)
        return True

    # rang
    if line.startswith('rang '):
        parts = line[5:].split('=', 1)
        name = parts[0].strip()
        nums = parts[1].strip().split(',')
        a = int(resolve(nums[0].strip(), variables))
        b = int(resolve(nums[1].strip(), variables))
        variables[name] = list(range(a, b))
        return True

    # uniq
    if line.startswith('uniq '):
        parts = line[5:].split('=', 1)
        name = parts[0].strip()
        lst = resolve(parts[1].strip(), variables)
        variables[name] = list(set(lst))
        return True

    # zipl
    if line.startswith('zipl '):
        parts = line[5:].split('=', 1)
        name = parts[0].strip()
        items = parts[1].strip().split(',')
        a = resolve(items[0].strip(), variables)
        b = resolve(items[1].strip(), variables)
        variables[name] = list(zip(a, b))
        return True

    # enum
    if line.startswith('enum '):
        parts = line[5:].split('=', 1)
        name = parts[0].strip()
        lst = resolve(parts[1].strip(), variables)
        variables[name] = list(enumerate(lst))
        return True

    # get
    if line.startswith('get '):
        parts = line[4:].split('=', 1)
        name = parts[0].strip()
        items = parts[1].strip().split(',')
        lst = resolve(items[0].strip(), variables)
        idx = int(resolve(items[1].strip(), variables))
        variables[name] = lst[idx]
        return True

    # seti
    if line.startswith('seti '):
        parts = line[5:].split(',')
        name = parts[0].strip()
        idx = int(resolve(parts[1].strip(), variables))
        value = resolve(parts[2].strip(), variables)
        if name in variables and isinstance(variables[name], list):
            variables[name][idx] = value
        return True

    # freeze
    if line.startswith('freeze '):
        parts = line[7:].split('=', 1)
        name = parts[0].strip()
        value = resolve(parts[1].strip(), variables)
        variables[name] = tuple(value) if isinstance(value, list) else value
        return True

    # islist
    if line.startswith('islist '):
        parts = line[7:].split('=', 1)
        name = parts[0].strip()
        value = resolve(parts[1].strip(), variables)
        variables[name] = isinstance(value, list)
        return True

    # each
    if line.startswith('each '):
        return 'each'

    return False
