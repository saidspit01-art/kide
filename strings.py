import re
from math_ops import resolve

def run_strings(line, variables):

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
        return True

    # loin
    if line.startswith('loin '):
        parts = line[5:].split('=', 1)
        name = parts[0].strip()
        value = parts[1].strip()
        if value.startswith('"') and value.endswith('"'):
            variables[name] = len(value[1:-1])
        elif value in variables:
            variables[name] = len(str(variables[value]))
        return True

    # up
    if line.startswith('up '):
        parts = line[3:].split('=', 1)
        name = parts[0].strip()
        value = resolve(parts[1].strip(), variables)
        variables[name] = str(value).upper()
        return True

    # do
    if line.startswith('do '):
        parts = line[3:].split('=', 1)
        name = parts[0].strip()
        value = resolve(parts[1].strip(), variables)
        variables[name] = str(value).lower()
        return True

    # replace
    if line.startswith('replace '):
        parts = line[8:].split('=', 1)
        name = parts[0].strip()
        items = parts[1].strip().split(',')
        value = resolve(items[0].strip(), variables)
        old = items[1].strip().strip('"')
        new = items[2].strip().strip('"')
        variables[name] = str(value).replace(old, new)
        return True

    # split
    if line.startswith('split '):
        parts = line[6:].split('=', 1)
        name = parts[0].strip()
        items = parts[1].strip().split(',', 1)
        value = resolve(items[0].strip(), variables)
        sep = items[1].strip().strip('"') if len(items) > 1 else ' '
        variables[name] = str(value).split(sep)
        return True

    # strip
    if line.startswith('strip '):
        parts = line[6:].split('=', 1)
        name = parts[0].strip()
        value = resolve(parts[1].strip(), variables)
        variables[name] = str(value).strip()
        return True

    # find
    if line.startswith('find '):
        parts = line[5:].split('=', 1)
        name = parts[0].strip()
        items = parts[1].strip().split(',')
        value = resolve(items[0].strip(), variables)
        search = items[1].strip().strip('"')
        variables[name] = str(value).find(search)
        return True

    # repeat
    if line.startswith('repeat '):
        parts = line[7:].split('=', 1)
        name = parts[0].strip()
        items = parts[1].strip().split(',')
        value = resolve(items[0].strip(), variables)
        times = int(resolve(items[1].strip(), variables))
        variables[name] = str(value) * times
        return True

    # starts
    if line.startswith('starts '):
        parts = line[7:].split('=', 1)
        name = parts[0].strip()
        items = parts[1].strip().split(',')
        value = resolve(items[0].strip(), variables)
        prefix = items[1].strip().strip('"')
        variables[name] = str(value).startswith(prefix)
        return True

    # ends
    if line.startswith('ends '):
        parts = line[5:].split('=', 1)
        name = parts[0].strip()
        items = parts[1].strip().split(',')
        value = resolve(items[0].strip(), variables)
        suffix = items[1].strip().strip('"')
        variables[name] = str(value).endswith(suffix)
        return True

    # ljust
    if line.startswith('ljust '):
        parts = line[6:].split('=', 1)
        name = parts[0].strip()
        items = parts[1].strip().split(',')
        value = resolve(items[0].strip(), variables)
        width = int(resolve(items[1].strip(), variables))
        variables[name] = str(value).ljust(width)
        return True

    # rjust
    if line.startswith('rjust '):
        parts = line[6:].split('=', 1)
        name = parts[0].strip()
        items = parts[1].strip().split(',')
        value = resolve(items[0].strip(), variables)
        width = int(resolve(items[1].strip(), variables))
        variables[name] = str(value).rjust(width)
        return True

    # center
    if line.startswith('center '):
        parts = line[7:].split('=', 1)
        name = parts[0].strip()
        items = parts[1].strip().split(',')
        value = resolve(items[0].strip(), variables)
        width = int(resolve(items[1].strip(), variables))
        variables[name] = str(value).center(width)
        return True

    # fmt (исправлен баг с кавычками)
    if line.startswith('fmt '):
        parts = line[4:].split('=', 1)
        name = parts[0].strip()
        items = parts[1].strip().split(',')
        template = items[0].strip().strip('"')
        args = []
        for x in items[1:]:
            v = x.strip()
            if v.startswith('"') and v.endswith('"'):
                args.append(v[1:-1])
            else:
                args.append(resolve(v, variables))
        variables[name] = template.format(*args)
        return True

    # joins (исправлен баг с кавычками)
    if line.startswith('joins '):
        parts = line[6:].split('=', 1)
        name = parts[0].strip()
        items = parts[1].strip().split(',', 1)
        sep = items[0].strip().strip('"')
        lst = resolve(items[1].strip(), variables)
        result = []
        for x in lst:
            s = str(x)
            if s.startswith('"') and s.endswith('"'):
                s = s[1:-1]
            result.append(s)
        variables[name] = sep.join(result)
        return True

    # dedup
    if line.startswith('dedup '):
        parts = line[6:].split('=', 1)
        name = parts[0].strip()
        lst = resolve(parts[1].strip(), variables)
        variables[name] = list(dict.fromkeys(lst))
        return True

    # isnum
    if line.startswith('isnum '):
        parts = line[6:].split('=', 1)
        name = parts[0].strip()
        value = resolve(parts[1].strip(), variables)
        variables[name] = str(value).isnumeric()
        return True

    # isalp
    if line.startswith('isalp '):
        parts = line[6:].split('=', 1)
        name = parts[0].strip()
        value = resolve(parts[1].strip(), variables)
        variables[name] = str(value).isalpha()
        return True

    # isalnum
    if line.startswith('isalnum '):
        parts = line[8:].split('=', 1)
        name = parts[0].strip()
        value = resolve(parts[1].strip(), variables)
        variables[name] = str(value).isalnum()
        return True

    # isspc
    if line.startswith('isspc '):
        parts = line[6:].split('=', 1)
        name = parts[0].strip()
        value = resolve(parts[1].strip(), variables)
        variables[name] = str(value).isspace()
        return True

    # isup
    if line.startswith('isup '):
        parts = line[5:].split('=', 1)
        name = parts[0].strip()
        value = resolve(parts[1].strip(), variables)
        variables[name] = str(value).isupper()
        return True

    # isdo
    if line.startswith('isdo '):
        parts = line[5:].split('=', 1)
        name = parts[0].strip()
        value = resolve(parts[1].strip(), variables)
        variables[name] = str(value).islower()
        return True

    # refind
    if line.startswith('refind '):
        parts = line[7:].split('=', 1)
        name = parts[0].strip()
        items = parts[1].strip().split(',')
        pattern = items[0].strip().strip('"')
        text = resolve(items[1].strip(), variables)
        match = re.search(pattern, str(text))
        variables[name] = match.group() if match else ''
        return True

    # resub
    if line.startswith('resub '):
        parts = line[6:].split('=', 1)
        name = parts[0].strip()
        items = parts[1].strip().split(',')
        pattern = items[0].strip().strip('"')
        repl = items[1].strip().strip('"')
        text = resolve(items[2].strip(), variables)
        variables[name] = re.sub(pattern, repl, str(text))
        return True

    # fmt исправлен выше
    return False
