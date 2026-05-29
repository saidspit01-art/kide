import os
import shutil
import zipfile
from math_ops import resolve

def run_files(line, variables):

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
        return True

    # load
    if line.startswith('load '):
        parts = line[5:].split('=', 1)
        name = parts[0].strip()
        filename = parts[1].strip()
        if filename.startswith('"') and filename.endswith('"'):
            filename = filename[1:-1]
        with open(filename, 'r') as f:
            variables[name] = f.read()
        return True

    # fadd
    if line.startswith('fadd '):
        parts = line[5:].split('=', 1)
        filename = parts[0].strip()
        value = parts[1].strip()
        if value in variables:
            value = str(variables[value])
        elif value.startswith('"') and value.endswith('"'):
            value = value[1:-1]
        with open(filename, 'a') as f:
            f.write(value + '\n')
        return True

    # fdel
    if line.startswith('fdel '):
        filename = line[5:].strip().strip('"')
        os.remove(filename)
        return True

    # mkdr
    if line.startswith('mkdr '):
        dirname = line[5:].strip().strip('"')
        os.makedirs(dirname, exist_ok=True)
        return True

    # rmdr
    if line.startswith('rmdr '):
        dirname = line[5:].strip().strip('"')
        os.rmdir(dirname)
        return True

    # flist
    if line.startswith('flist '):
        parts = line[6:].split('=', 1)
        name = parts[0].strip()
        path = parts[1].strip().strip('"') if len(parts) > 1 else '.'
        variables[name] = os.listdir(path)
        return True

    # fex
    if line.startswith('fex '):
        parts = line[4:].split('=', 1)
        name = parts[0].strip()
        path = parts[1].strip().strip('"')
        variables[name] = os.path.exists(path)
        return True

    # curdr
    if line.startswith('curdr '):
        name = line[6:].strip()
        variables[name] = os.getcwd()
        return True

    # godr
    if line.startswith('godr '):
        path = line[5:].strip().strip('"')
        os.chdir(path)
        return True

    # fsize
    if line.startswith('fsize '):
        parts = line[6:].split('=', 1)
        name = parts[0].strip()
        path = parts[1].strip().strip('"')
        variables[name] = os.path.getsize(path)
        return True

    # fren
    if line.startswith('fren '):
        parts = line[5:].split(',')
        old = parts[0].strip().strip('"')
        new = parts[1].strip().strip('"')
        os.rename(old, new)
        return True

    # fcopy
    if line.startswith('fcopy '):
        parts = line[6:].split(',')
        src = parts[0].strip().strip('"')
        dst = parts[1].strip().strip('"')
        shutil.copy(src, dst)
        return True

    # fpath
    if line.startswith('fpath '):
        parts = line[6:].split('=', 1)
        name = parts[0].strip()
        path = parts[1].strip().strip('"')
        variables[name] = os.path.abspath(path)
        return True

    # fname
    if line.startswith('fname '):
        parts = line[6:].split('=', 1)
        name = parts[0].strip()
        path = parts[1].strip().strip('"')
        variables[name] = os.path.basename(path)
        return True

    # fdir
    if line.startswith('fdir '):
        parts = line[5:].split('=', 1)
        name = parts[0].strip()
        path = parts[1].strip().strip('"')
        variables[name] = os.path.dirname(path)
        return True

    # pjoin
    if line.startswith('pjoin '):
        parts = line[6:].split('=', 1)
        name = parts[0].strip()
        paths = [p.strip().strip('"') for p in parts[1].split(',')]
        variables[name] = os.path.join(*paths)
        return True

    # fext
    if line.startswith('fext '):
        parts = line[5:].split('=', 1)
        name = parts[0].strip()
        path = parts[1].strip().strip('"')
        variables[name] = os.path.splitext(path)[1]
        return True

    # zipc
    if line.startswith('zipc '):
        parts = line[5:].split(',')
        zipname = parts[0].strip().strip('"')
        filename = parts[1].strip().strip('"')
        with zipfile.ZipFile(zipname, 'w') as z:
            z.write(filename)
        return True

    # zipx
    if line.startswith('zipx '):
        parts = line[5:].split(',')
        zipname = parts[0].strip().strip('"')
        outdir = parts[1].strip().strip('"')
        with zipfile.ZipFile(zipname, 'r') as z:
            z.extractall(outdir)
        return True

    return False
