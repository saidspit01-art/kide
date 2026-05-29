import sys
from math_ops import resolve, evaluate_condition, calc
from core import run_core
from math_ops import run_math
from strings import run_strings
from lists import run_lists
from dicts import run_dicts
from files import run_files
from web import run_web
from time_ops import run_time
from utils import run_utils

def easter(line):
    if line == 'Sakura':
        print('🌸 🌸 🌸 🌸 🌸')
        print('  🌸 🌸 🌸 🌸')
        print('🌸 🌸 🌸 🌸 🌸')
        return True
    if line == 'creatork':
        print('Thank you so much for supporting us!')
        return True
    if line == 'der':
        print('⛩️  ⛩️  ⛩️')
        return True
    if line == 'fedaw':
        print('Deeply grateful')
        return True
    return False

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
        if easter(line):
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

        # each
        if line.startswith('each '):
            parts = line[5:].split(',', 1)
            varname = parts[0].strip()
            listname = parts[1].strip().rstrip(':')
            body = []
            i += 1
            while i < len(lines):
                inner = lines[i]
                if inner and not inner.startswith(' ') and not inner.startswith('\t'):
                    break
                body.append(inner.strip())
                i += 1
            lst = variables.get(listname, [])
            for item in lst:
                variables[varname] = item
                run(body, variables, functions)
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

        # Модули
        result = run_core(line, lines, i, variables, functions, run)
        if result is not None:
            i = result
            continue

        if run_math(line, variables):
            i += 1
            continue

        if run_strings(line, variables):
            i += 1
            continue

        if run_lists(line, variables):
            i += 1
            continue

        if run_dicts(line, variables):
            i += 1
            continue

        if run_files(line, variables):
            i += 1
            continue

        if run_web(line, variables):
            i += 1
            continue

        if run_time(line, variables):
            i += 1
            continue

        if run_utils(line, variables):
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
