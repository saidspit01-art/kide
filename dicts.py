from math_ops import resolve

def run_dicts(line, variables):

    # dict
    if line.startswith('dict '):
        name = line[5:].strip()
        variables[name] = {}
        return True

    # dadd
    if line.startswith('dadd '):
        parts = line[5:].split(',')
        name = parts[0].strip()
        key = parts[1].strip().strip('"')
        value = resolve(parts[2].strip(), variables)
        if name in variables:
            variables[name][key] = value
        return True

    # dget
    if line.startswith('dget '):
        parts = line[5:].split('=', 1)
        name = parts[0].strip()
        items = parts[1].strip().split(',')
        dname = items[0].strip()
        key = items[1].strip().strip('"')
        variables[name] = variables.get(dname, {}).get(key)
        return True

    # dkeys
    if line.startswith('dkeys '):
        parts = line[6:].split('=', 1)
        name = parts[0].strip()
        dname = parts[1].strip()
        variables[name] = list(variables.get(dname, {}).keys())
        return True

    # dvals
    if line.startswith('dvals '):
        parts = line[6:].split('=', 1)
        name = parts[0].strip()
        dname = parts[1].strip()
        variables[name] = list(variables.get(dname, {}).values())
        return True

    # ddel
    if line.startswith('ddel '):
        parts = line[5:].split(',')
        name = parts[0].strip()
        key = parts[1].strip().strip('"')
        if name in variables:
            variables[name].pop(key, None)
        return True

    # dlen
    if line.startswith('dlen '):
        parts = line[5:].split('=', 1)
        name = parts[0].strip()
        dname = parts[1].strip()
        variables[name] = len(variables.get(dname, {}))
        return True

    # dclr
    if line.startswith('dclr '):
        name = line[5:].strip()
        if name in variables:
            variables[name].clear()
        return True

    # dcopy
    if line.startswith('dcopy '):
        parts = line[6:].split('=', 1)
        name = parts[0].strip()
        dname = parts[1].strip()
        variables[name] = variables.get(dname, {}).copy()
        return True

    # dmerge
    if line.startswith('dmerge '):
        parts = line[7:].split(',')
        name = parts[0].strip()
        other = parts[1].strip()
        if name in variables and other in variables:
            variables[name].update(variables[other])
        return True

    # isdict
    if line.startswith('isdict '):
        parts = line[7:].split('=', 1)
        name = parts[0].strip()
        value = resolve(parts[1].strip(), variables)
        variables[name] = isinstance(value, dict)
        return True

    return False
