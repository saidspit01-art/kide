import json
import base64
from math_ops import resolve

try:
    import requests
    HAS_REQUESTS = True
except:
    HAS_REQUESTS = False

def run_web(line, variables):

    # wget
    if line.startswith('wget '):
        parts = line[5:].split('=', 1)
        name = parts[0].strip()
        url = parts[1].strip().strip('"')
        if HAS_REQUESTS:
            variables[name] = requests.get(url).text
        else:
            variables[name] = 'requests not installed'
        return True

    # wpost
    if line.startswith('wpost '):
        parts = line[6:].split('=', 1)
        name = parts[0].strip()
        items = parts[1].strip().split(',', 1)
        url = items[0].strip().strip('"')
        data = resolve(items[1].strip(), variables) if len(items) > 1 else {}
        if HAS_REQUESTS:
            variables[name] = requests.post(url, data=data).text
        else:
            variables[name] = 'requests not installed'
        return True

    # jget
    if line.startswith('jget '):
        parts = line[5:].split('=', 1)
        name = parts[0].strip()
        value = resolve(parts[1].strip(), variables)
        variables[name] = json.loads(str(value))
        return True

    # jmake
    if line.startswith('jmake '):
        parts = line[6:].split('=', 1)
        name = parts[0].strip()
        value = resolve(parts[1].strip(), variables)
        variables[name] = json.dumps(value, ensure_ascii=False)
        return True

    # b64
    if line.startswith('b64 '):
        parts = line[4:].split('=', 1)
        name = parts[0].strip()
        value = resolve(parts[1].strip(), variables)
        variables[name] = base64.b64encode(str(value).encode()).decode()
        return True

    # browse
    if line.startswith('browse '):
        import webbrowser
        url = line[7:].strip().strip('"')
        webbrowser.open(url)
        return True

    return False
