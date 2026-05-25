import sys

def evaluate_condition(condition, variables):
    parts = condition.split()
    left = parts[0]
    op = parts[1]
    right = parts[2]
    left = int(variables.get(left, left))
    right = int(variables.get(right, right))
    if op == '>':
        return left > right
    elif op == '<':
        return left < right
    elif op == '==':
        return left == right
    return False

def resolve(value, variables):
    value = value.strip()
    if value in variables:
        return int(variables[value])
    return int(value)

def calc(expression, variables):
    if '+' in expression:
        parts = expression.split('+')
        return resolve(parts[0], variables) + resolve(parts[1], variables)
    elif '-' in expression:
        parts = expression.split('-')
        return resolve(parts[0], variables) - resolve(parts[1], variables)
    elif '*' in expression:
        parts = expression.split('*')
        return resolve(parts[0], variables) * resolve(parts[1], variables)
    else:
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
            value = line[7:]
            if value.startswith('"') and value.endswith('"'):
                print(value[1:-1])
            elif value in variables:
                print(variables[value])
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
                if inner.startswith('fii ') or (not inner.startswith(' ') and not inner.startswith('\t') and inner and not in_les and len(true_block) > 0):
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
