import re
import ast
import json


def _parse_ast(contents):
    try:
        return ast.literal_eval(contents)
    except SyntaxError:
        pass
    try:
        # remove all comments
        contents = re.sub(re.compile(r"/\*.*?\*/", re.DOTALL), "", contents)
        contents = re.sub(re.compile(r"#.*?\n"), "", contents)

        # remove anything before dict declaration like: "caps = { ..."
        match = re.match(r"^([^{]+)", contents)
        if match:
            contents = contents.replace(match.group(1), "")

        # and try again
        return ast.literal_eval(contents)
    except SyntaxError:
        pass

    return False


def _parse_manual(contents):
    capabilities = {}

    code_lines = contents.split('\n')
    for line in code_lines:
        if "desired_cap = {" in line:
            line = line.split("desired_cap = {")[1]

        # 'KEY' : 'VALUE'
        data = re.match(r"^\s*'([\S\s]+)'\s*:\s*'([\S\s]+)'\s*[,}]?\s*$", line)
        if data:
            key = data.group(1)
            value = data.group(2)
            capabilities[key] = value
            continue

        # "KEY" : "VALUE"
        data = re.match(r'^\s*"([\S\s]+)"\s*:\s*"([\S\s]+)"\s*[,}]?\s*$', line)
        if data:
            key = data.group(1)
            value = data.group(2)
            capabilities[key] = value
            continue

        # 'KEY' : "VALUE"
        data = re.match(
            r'''^\s*'([\S\s]+)'\s*:\s*"([\S\s]+)"\s*[,}]?\s*$''', line)
        if data:
            key = data.group(1)
            value = data.group(2)
            capabilities[key] = value
            continue

        # "KEY" : 'VALUE'
        data = re.match(
            r'''^\s*"([\S\s]+)"\s*:\s*'([\S\s]+)'\s*[,}]?\s*$''', line)
        if data:
            key = data.group(1)
            value = data.group(2)
            capabilities[key] = value
            continue

        # "KEY" : True
        data = re.match(
            r'''^\s*"([\S\s]+)"\s*:\s*True\s*[,}]?\s*$''', line)
        if data:
            key = data.group(1)
            value = True
            capabilities[key] = value
            continue

        # 'KEY' : True
        data = re.match(
            r'''^\s*'([\S\s]+)'\s*:\s*True\s*[,}]?\s*$''', line)
        if data:
            key = data.group(1)
            value = True
            capabilities[key] = value
            continue

        # "KEY" : False
        data = re.match(
            r'''^\s*"([\S\s]+)"\s*:\s*False\s*[,}]?\s*$''', line)
        if data:
            key = data.group(1)
            value = False
            capabilities[key] = value
            continue

        # 'KEY' : False
        data = re.match(
            r'''^\s*'([\S\s]+)'\s*:\s*False\s*[,}]?\s*$''', line)
        if data:
            key = data.group(1)
            value = False
            capabilities[key] = value
            continue

        # caps['KEY'] = 'VALUE'
        data = re.match(r"^\s*caps\['([\S\s]+)'\]\s*=\s*'([\S\s]+)'\s*$", line)
        if data:
            key = data.group(1)
            value = data.group(2)
            capabilities[key] = value
            continue

        # caps["KEY"] = "VALUE"
        data = re.match(r'^\s*caps\["([\S\s]+)"\]\s*=\s*"([\S\s]+)"\s*$', line)
        if data:
            key = data.group(1)
            value = data.group(2)
            capabilities[key] = value
            continue

        # caps['KEY'] = "VALUE"
        data = re.match(
            r'''^\s*caps\['([\S\s]+)'\]\s*=\s*"([\S\s]+)"\s*$''', line)
        if data:
            key = data.group(1)
            value = data.group(2)
            capabilities[key] = value
            continue

        # caps["KEY"] = 'VALUE'
        data = re.match(
            r'''^\s*caps\["([\S\s]+)"\]\s*=\s*'([\S\s]+)'\s*$''', line)
        if data:
            key = data.group(1)
            value = data.group(2)
            capabilities[key] = value
            continue

        # caps["KEY"] = True
        data = re.match(
            r'''^\s*caps\["([\S\s]+)"\]\s*=\s*True\s*$''', line)
        if data:
            key = data.group(1)
            value = True
            capabilities[key] = value
            continue

        # caps['KEY'] = True
        data = re.match(
            r'''^\s*caps\['([\S\s]+)'\]\s*=\s*True\s*$''', line)
        if data:
            key = data.group(1)
            value = True
            capabilities[key] = value
            continue

        # caps["KEY"] = False
        data = re.match(
            r'''^\s*caps\["([\S\s]+)"\]\s*=\s*False\s*$''', line)
        if data:
            key = data.group(1)
            value = False
            capabilities[key] = value
            continue

        # caps['KEY'] = False
        data = re.match(
            r'''^\s*caps\['([\S\s]+)'\]\s*=\s*False\s*$''', line)
        if data:
            key = data.group(1)
            value = False
            capabilities[key] = value
            continue

    return capabilities


def get_desired_capabilities(cap_file):
    f = open(cap_file, 'r')
    all_code = f.read()
    f.close()

    if cap_file.endswith('.py'):
        capabilities = _parse_ast(all_code)
        if not capabilities:
            capabilities = _parse_manual(all_code)
    elif cap_file.endswith('.json'):
        capabilities = json.loads(all_code)
    else:
        raise Exception("\n\n`%s` is not a Python or JSON file!\n\n" % cap_file)

    if len(capabilities.keys()) == 0:
        raise Exception("Unable to parse desired capabilities file!")

    return capabilities
