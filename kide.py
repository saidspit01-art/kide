import sys
import random
import time
from datetime import datetime

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

def calc(expression, variables):
    expression = expression.strip()
    for op in ['+', '-', '*', '/', '%']:
        if op in expression:
            parts = expression.split(op, 1)
            a = resolve(parts[0].strip(), variables)
            b = resolve(parts[1].strip(), variables)
            try:
                a, b = float(a), float(b)
                if op == '+': return int(a + b) if a + b == int(a + b) else a + b
                if op == '-': return int(a - b) if a - b == int(a - b) else a - b
                if op == '*': return int(a * b) if a * b == int(a * b) else a * b
                if op == '/': return int(a // b)
                if op == '%': return int(a % b)
            except:
                if op == '+':
                    return str(a) + str(b)
    return resolve(expression, variables)

def run(lines, variables, functions):
    i = 0
    while i < len(lines):
        line = lines[i].strip()

        if not line:
            i += 1
            continue
        if line.startswith('#$'):
            i += 1
            continue

        # Пасхалки
        if line == 'Sakura':
            print('🌸 🌸 🌸 🌸 🌸')
            print('  🌸 🌸 🌸 🌸')
            print('🌸 🌸 🌸 🌸 🌸')
            i += 1
            continue
        if line == 'creatork':
            print('Thank you so much for supporting us!')
            i += 1
            continue
        if line == 'der':
            print('⛩️  ⛩️  ⛩️')
            i += 1
            continue
        if line == 'fedaw':
            print('Deeply grateful')
            i += 1
            continue

        # pirent
        if line.startswith('pirent '):
            value = line[7:].strip()
            if value.startswith('"') and value.endswith('"'):
                print(value[1:-1])
            elif value in variables:
                print(variables[value])
            else:
                print(calc(value, variables))
            i += 1
            continue

        # ret
        if line.startswith('ret '):
            parts = line[4:].split('=', 1)
            name = parts[0].strip()
            value = parts[1].strip()
            if value.startswith('"') and value.endswith('"'):
                variables[name] = value[1:-1]
            else:
                variables[name] = calc(value, variables)
            i += 1
            continue

        # ask
        if line.startswith('ask '):
            parts = line[4:].split('=', 1)
            name = parts[0].strip()
            prompt = parts[1].strip()
            if prompt.startswith('"') and prompt.endswith('"'):
                prompt = prompt[1:-1]
            variables[name] = input(prompt + ' ')
            i += 1
            continue

        # loin
        if line.startswith('loin '):
            parts = line[5:].split('=', 1)
            name = parts[0].strip()
            value = parts[1].strip()
            if value.startswith('"') and value.endswith('"'):
                variables[name] = len(value[1:-1])
            elif value in variables:
                variables[name] = len(str(variables[value]))
            i += 1
            continue

        # jen
        if line.startswith('jen '):
            parts = line[4:].split('=', 1)
            name = parts[0].strip()
            value = parts[1].strip()
            items = value.split('+')
            result = ''
            for item in items:
                item = item.strip()
                if item.startswith('"') and item.endswith('"'):
                    result += item[1:-1]
                elif item in variables:
                    result += str(variables[item])
            variables[name] = result
            i += 1
            continue

        # rand
        if line.startswith('rand '):
            parts = line[5:].split('=', 1)
            name = parts[0].strip()
            nums = parts[1].strip().split()
            a, b = int(nums[0]), int(nums[1])
            variables[name] = random.randint(a, b)
            i += 1
            continue

        # save
        if line.startswith('save '):
            parts = line[5:].split('=', 1)
            filename = parts[0].strip()
            value = parts[1].strip()
            if value in variables:
                value = str(variables[value])
            elif value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            with open(filename, 'w') as f:
                f.write(value)
            i += 1
            continue

        # load
        if line.startswith('load '):
            parts = line[5:].split('=', 1)
            name = parts[0].strip()
            filename = parts[1].strip()
            if filename.startswith('"') and filename.endswith('"'):
                filename = filename[1:-1]
            with open(filename, 'r') as f:
                variables[name] = f.read()
            i += 1
            continue

        # imr
        if line.startswith('imr '):
            filename = line[4:].strip()
            if not filename.endswith('.kide'):
                filename += '.kide'
            with open(filename, 'r') as f:
                imported = f.read().split('\n')
            run(imported, variables, functions)
            i += 1
            continue

        # rot (округление)
        if line.startswith('rot '):
            parts = line[4:].split('=', 1)
            name = parts[0].strip()
            value = resolve(parts[1].strip(), variables)
            variables[name] = round(float(value))
            i += 1
            continue

        # abc (абсолютное)
        if line.startswith('abc '):
            parts = line[4:].split('=', 1)
            name = parts[0].strip()
            value = resolve(parts[1].strip(), variables)
            variables[name] = abs(float(value))
            i += 1
            continue

        # hlam (максимум)
        if line.startswith('hlam '):
            parts = line[5:].split('=', 1)
            name = parts[0].strip()
            nums = [resolve(x.strip(), variables) for x in parts[1].split(',')]
            variables[name] = max(nums)
            i += 1
            continue

        # zolot (минимум)
        if line.startswith('zolot '):
            parts = line[6:].split('=', 1)
            name = parts[0].strip()
            nums = [resolve(x.strip(), variables) for x in parts[1].split(',')]
            variables[name] = min(nums)
            i += 1
            continue

        # many (сумма)
        if line.startswith('many '):
            parts = line[5:].split('=', 1)
            name = parts[0].strip()
            nums = [resolve(x.strip(), variables) for x in parts[1].split(',')]
            variables[name] = sum(nums)
            i += 1
            continue

        # type
        if line.startswith('type '):
            parts = line[5:].split('=', 1)
            name = parts[0].strip()
            value = resolve(parts[1].strip(), variables)
            variables[name] = type(value).__name__
            i += 1
            continue

        # int
        if line.startswith('int '):
            parts = line[4:].split('=', 1)
            name = parts[0].strip()
            value = resolve(parts[1].strip(), variables)
            variables[name] = int(float(str(value)))
            i += 1
            continue

        # str
        if line.startswith('str '):
            parts = line[4:].split('=', 1)
            name = parts[0].strip()
            value = resolve(parts[1].strip(), variables)
            variables[name] = str(value)
            i += 1
            continue

        # float
        if line.startswith('float '):
            parts = line[6:].split('=', 1)
            name = parts[0].strip()
            value = resolve(parts[1].strip(), variables)
            variables[name] = float(str(value))
            i += 1
            continue

        # split
        if line.startswith('split '):
            parts = line[6:].split('=', 1)
            name = parts[0].strip()
            items = parts[1].strip().split(',', 1)
            value = resolve(items[0].strip(), variables)
            sep = items[1].strip().strip('"') if len(items) > 1 else ' '
            variables[name] = str(value).split(sep)
            i += 1
            continue

        # strip
        if line.startswith('strip '):
            parts = line[6:].split('=', 1)
            name = parts[0].strip()
            value = resolve(parts[1].strip(), variables)
            variables[name] = str(value).strip()
            i += 1
            continue

        # replace
        if line.startswith('replace '):
            parts = line[8:].split('=', 1)
            name = parts[0].strip()
            items = parts[1].strip().split(',')
            value = resolve(items[0].strip(), variables)
            old = items[1].strip().strip('"')
            new = items[2].strip().strip('"')
            variables[name] = str(value).replace(old, new)
            i += 1
            continue

        # up (верхний регистр)
        if line.startswith('up '):
            parts = line[3:].split('=', 1)
            name = parts[0].strip()
            value = resolve(parts[1].strip(), variables)
            variables[name] = str(value).upper()
            i += 1
            continue

        # do (нижний регистр)
        if line.startswith('do '):
            parts = line[3:].split('=', 1)
            name = parts[0].strip()
            value = resolve(parts[1].strip(), variables)
            variables[name] = str(value).lower()
            i += 1
            continue

        # find
        if line.startswith('find '):
            parts = line[5:].split('=', 1)
            name = parts[0].strip()
            items = parts[1].strip().split(',')
            value = resolve(items[0].strip(), variables)
            search = items[1].strip().strip('"')
            variables[name] = str(value).find(search)
            i += 1
            continue

        # repeat
        if line.startswith('repeat '):
            parts = line[7:].split('=', 1)
            name = parts[0].strip()
            items = parts[1].strip().split(',')
            value = resolve(items[0].strip(), variables)
            times = int(resolve(items[1].strip(), variables))
            variables[name] = str(value) * times
            i += 1
            continue

        # exit
        if line == 'exit':
            sys.exit()

        # sleep
        if line.startswith('sleep '):
            seconds = float(resolve(line[6:].strip(), variables))
            time.sleep(seconds)
            i += 1
            continue

        # time
        if line.startswith('time '):
            name = line[5:].strip()
            variables[name] = datetime.now().strftime('%H:%M:%S')
            i += 1
            continue

        # date
        if line.startswith('date '):
            name = line[5:].strip()
            variables[name] = datetime.now().strftime('%d.%m.%Y')
            i += 1
            continue

        # tri/katch
        if line.startswith('tri:'):
            try_block = []
            catch_block = []
            in_katch = False
            i += 1
            while i < len(lines):
                inner = lines[i].strip()
                if inner.startswith('katch:'):
                    in_katch = True
                    i += 1
                    continue
                if not lines[i].startswith(' ') and not lines[i].startswith('\t') and inner:
                    break
                if in_katch:
                    catch_block.append(inner)
                else:
                    try_block.append(inner)
                i += 1
            try:
                run(try_block, variables, functions)
            except:
                run(catch_block, variables, functions)
            continue

        # fii/les
        if line.startswith('fii '):
            condition = line[4:].rstrip(':')
            result = evaluate_condition(condition, variables)
            i += 1
            true_block = []
            false_block = []
            in_les = False
            while i < len(lines):
                inner = lines[i].strip()
                if inner.startswith('les:'):
                    in_les = True
                    i += 1
                    continue
                if not lines[i].startswith(' ') and not lines[i].startswith('\t') and inner:
                    break
                if in_les:
                    false_block.append(inner)
                else:
                    true_block.append(inner)
                i += 1
            if result:
                run(true_block, variables, functions)
            else:
                run(false_block, variables, functions)
            continue

        # fedya
        if line.startswith('fedya '):
            name = line[6:].rstrip(':').rstrip('()')
            name = name.strip()
            body = []
            i += 1
            while i < len(lines):
                inner = lines[i]
                if inner and not inner.startswith(' ') and not inner.startswith('\t'):
                    break
                body.append(inner.strip())
                i += 1
            functions[name] = body
            continue

        # rex
        if line.startswith('rex '):
            count = int(line[4:].rstrip(':'))
            body = []
            i += 1
            while i < len(lines):
                inner = lines[i]
                if inner and not inner.startswith(' ') and not inner.startswith('\t'):
                    break
                body.append(inner.strip())
                i += 1
            for _ in range(count):
                run(body, variables, functions)
            continue

        # liw
        if line.startswith('liw '):
            condition = line[4:].rstrip(':')
            body = []
            i += 1
            while i < len(lines):
                inner = lines[i]
                if inner and not inner.startswith(' ') and not inner.startswith('\t'):
                    break
                body.append(inner.strip())
                i += 1
            while evaluate_condition(condition, variables):
                run(body, variables, functions)
            continue

        # Вызов функции
        if line.rstrip('()') in functions:
            name = line.rstrip('()')
            run(functions[name], variables, functions)
            i += 1
            continue

        i += 1

if len(sys.argv) < 2:
    print('Использование: python3 kide.py файл.kide')
else:
    with open(sys.argv[1], 'r') as f:
        code = f.read()
    lines = code.split('\n')
    run(lines, {}, {})
