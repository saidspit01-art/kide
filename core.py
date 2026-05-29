def run_core(line, lines, i, variables, functions, run):

    # pirent
    if line.startswith('pirent '):
        value = line[7:].strip()
        if value.startswith('"') and value.endswith('"'):
            print(value[1:-1])
        elif value in variables:
            print(variables[value])
        else:
            from math_ops import calc
            print(calc(value, variables))
        return i + 1

    # ret
    if line.startswith('ret '):
        from math_ops import calc
        parts = line[4:].split('=', 1)
        name = parts[0].strip()
        value = parts[1].strip()
        if value.startswith('"') and value.endswith('"'):
            variables[name] = value[1:-1]
        else:
            variables[name] = calc(value, variables)
        return i + 1

    # ask
    if line.startswith('ask '):
        parts = line[4:].split('=', 1)
        name = parts[0].strip()
        prompt = parts[1].strip()
        if prompt.startswith('"') and prompt.endswith('"'):
            prompt = prompt[1:-1]
        variables[name] = input(prompt + ' ')
        return i + 1

    # fii/les
    if line.startswith('fii '):
        from math_ops import evaluate_condition
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
        return i

    # fedya
    if line.startswith('fedya '):
        name = line[6:].rstrip(':').rstrip('()').strip()
        body = []
        i += 1
        while i < len(lines):
            inner = lines[i]
            if inner and not inner.startswith(' ') and not inner.startswith('\t'):
                break
            body.append(inner.strip())
            i += 1
        functions[name] = body
        return i

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
        return i

    # liw
    if line.startswith('liw '):
        from math_ops import evaluate_condition
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
        return i

    # Вызов функции
    if line.rstrip('()') in functions:
        name = line.rstrip('()')
        run(functions[name], variables, functions)
        return i + 1

    return None
