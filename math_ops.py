import math

def resolve(value, variables):
    value = value.strip()
    if value in variables:
        return variables[value]
    try:
        return int(value)
    except:
        try:
            return float(value)
        except:
            return value

def smart_num(val):
    try:
        if float(val) == int(float(val)):
            return int(float(val))
        return float(val)
    except:
        return val

def evaluate_condition(condition, variables):
    parts = condition.split()
    left = parts[0]
    op = parts[1]
    right = parts[2]
    left_val = resolve(left, variables)
    right_val = resolve(right, variables)
    if op == '>':
        return float(str(left_val)) > float(str(right_val))
    elif op == '<':
        return float(str(left_val)) < float(str(right_val))
    elif op == '==':
        return str(left_val) == str(right_val)
    elif op == '!=':
        return str(left_val) != str(right_val)
    return False

def calc(expression, variables):
    expression = expression.strip()
    for op in ['+', '-', '*', '/', '%']:
        if op in expression:
            parts = expression.split(op, 1)
            a = resolve(parts[0].strip(), variables)
            b = resolve(parts[1].strip(), variables)
            try:
                a, b = float(a), float(b)
                if op == '+': return smart_num(a + b)
                if op == '-': return smart_num(a - b)
                if op == '*': return smart_num(a * b)
                if op == '/': return int(a // b)
                if op == '%': return int(a % b)
            except:
                if op == '+':
                    return str(a) + str(b)
    return resolve(expression, variables)

def run_math(line, variables):

    # rot
    if line.startswith('rot '):
        parts = line[4:].split('=', 1)
        name = parts[0].strip()
        value = resolve(parts[1].strip(), variables)
        variables[name] = round(float(value))
        return True

    # abc
    if line.startswith('abc '):
        parts = line[4:].split('=', 1)
        name = parts[0].strip()
        value = resolve(parts[1].strip(), variables)
        variables[name] = smart_num(abs(float(value)))
        return True

    # hlam
    if line.startswith('hlam '):
        parts = line[5:].split('=', 1)
        name = parts[0].strip()
        nums = [resolve(x.strip(), variables) for x in parts[1].split(',')]
        variables[name] = max(nums)
        return True

    # zolot
    if line.startswith('zolot '):
        parts = line[6:].split('=', 1)
        name = parts[0].strip()
        nums = [resolve(x.strip(), variables) for x in parts[1].split(',')]
        variables[name] = min(nums)
        return True

    # many
    if line.startswith('many '):
        parts = line[5:].split('=', 1)
        name = parts[0].strip()
        nums = [resolve(x.strip(), variables) for x in parts[1].split(',')]
        variables[name] = sum(nums)
        return True

    # pow
    if line.startswith('pow '):
        parts = line[4:].split('=', 1)
        name = parts[0].strip()
        items = parts[1].strip().split(',')
        a = float(resolve(items[0].strip(), variables))
        b = float(resolve(items[1].strip(), variables))
        variables[name] = smart_num(a ** b)
        return True

    # sqrt
    if line.startswith('sqrt '):
        parts = line[5:].split('=', 1)
        name = parts[0].strip()
        value = float(resolve(parts[1].strip(), variables))
        variables[name] = smart_num(math.sqrt(value))
        return True

    # sin
    if line.startswith('sin '):
        parts = line[4:].split('=', 1)
        name = parts[0].strip()
        value = float(resolve(parts[1].strip(), variables))
        variables[name] = math.sin(value)
        return True

    # cos
    if line.startswith('cos '):
        parts = line[4:].split('=', 1)
        name = parts[0].strip()
        value = float(resolve(parts[1].strip(), variables))
        variables[name] = math.cos(value)
        return True

    # pi
    if line.startswith('pi '):
        name = line[3:].strip()
        variables[name] = math.pi
        return True

    # log
    if line.startswith('log '):
        parts = line[4:].split('=', 1)
        name = parts[0].strip()
        value = float(resolve(parts[1].strip(), variables))
        variables[name] = math.log(value)
        return True

    # som
    if line.startswith('som '):
        parts = line[4:].split('=', 1)
        name = parts[0].strip()
        lst = resolve(parts[1].strip(), variables)
        variables[name] = smart_num(sum(lst) / len(lst))
        return True

    # maxl
    if line.startswith('maxl '):
        parts = line[5:].split('=', 1)
        name = parts[0].strip()
        lst = resolve(parts[1].strip(), variables)
        variables[name] = max(lst)
        return True

    # minl
    if line.startswith('minl '):
        parts = line[5:].split('=', 1)
        name = parts[0].strip()
        lst = resolve(parts[1].strip(), variables)
        variables[name] = min(lst)
        return True

    # tobin
    if line.startswith('tobin '):
        parts = line[6:].split('=', 1)
        name = parts[0].strip()
        value = int(resolve(parts[1].strip(), variables))
        variables[name] = bin(value)
        return True

    # tohex
    if line.startswith('tohex '):
        parts = line[6:].split('=', 1)
        name = parts[0].strip()
        value = int(resolve(parts[1].strip(), variables))
        variables[name] = hex(value)
        return True

    # tochr
    if line.startswith('tochr '):
        parts = line[6:].split('=', 1)
        name = parts[0].strip()
        value = int(resolve(parts[1].strip(), variables))
        variables[name] = chr(value)
        return True

    # tord
    if line.startswith('tord '):
        parts = line[5:].split('=', 1)
        name = parts[0].strip()
        value = resolve(parts[1].strip(), variables)
        variables[name] = ord(str(value)[0])
        return True

    # 2-0
    if line.startswith('2-0 '):
        parts = line[4:].split('=', 1)
        name = parts[0].strip()
        value = int(resolve(parts[1].strip(), variables))
        variables[name] = value % 2 == 0
        return True

    # 2:0
    if line.startswith('2:0 '):
        parts = line[4:].split('=', 1)
        name = parts[0].strip()
        value = int(resolve(parts[1].strip(), variables))
        variables[name] = value % 2 != 0
        return True

    return False
