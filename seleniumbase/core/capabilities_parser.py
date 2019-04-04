import re


def get_desired_capabilities(cap_file):
    if not cap_file.endswith('.py'):
        raise Exception("\n\n`%s` is not a Python file!\n\n" % cap_file)

    f = open(cap_file, 'r')
    all_code = f.read()
    f.close()

    desired_capabilities = {}
    num_capabilities = 0

    code_lines = all_code.split('\n')
    for line in code_lines:
        if "desired_cap = {" in line:
            line = line.split("desired_cap = {")[1]

        # 'KEY' : 'VALUE'
        data = re.match(r"^\s*'([\S\s]+)'\s*:\s*'([\S\s]+)'\s*[,}]?\s*$", line)
        if data:
            key = data.group(1)
            value = data.group(2)
            desired_capabilities[key] = value
            num_capabilities += 1
            continue

        # "KEY" : "VALUE"
        data = re.match(r'^\s*"([\S\s]+)"\s*:\s*"([\S\s]+)"\s*[,}]?\s*$', line)
        if data:
            key = data.group(1)
            value = data.group(2)
            desired_capabilities[key] = value
            num_capabilities += 1
            continue

        # 'KEY' : "VALUE"
        data = re.match(
            r'''^\s*'([\S\s]+)'\s*:\s*"([\S\s]+)"\s*[,}]?\s*$''', line)
        if data:
            key = data.group(1)
            value = data.group(2)
            desired_capabilities[key] = value
            num_capabilities += 1
            continue

        # "KEY" : 'VALUE'
        data = re.match(
            r'''^\s*"([\S\s]+)"\s*:\s*'([\S\s]+)'\s*[,}]?\s*$''', line)
        if data:
            key = data.group(1)
            value = data.group(2)
            desired_capabilities[key] = value
            num_capabilities += 1
            continue

        # "KEY" : True
        data = re.match(
            r'''^\s*"([\S\s]+)"\s*:\s*True\s*[,}]?\s*$''', line)
        if data:
            key = data.group(1)
            value = True
            desired_capabilities[key] = value
            num_capabilities += 1
            continue

        # 'KEY' : True
        data = re.match(
            r'''^\s*'([\S\s]+)'\s*:\s*True\s*[,}]?\s*$''', line)
        if data:
            key = data.group(1)
            value = True
            desired_capabilities[key] = value
            num_capabilities += 1
            continue

        # "KEY" : False
        data = re.match(
            r'''^\s*"([\S\s]+)"\s*:\s*False\s*[,}]?\s*$''', line)
        if data:
            key = data.group(1)
            value = False
            desired_capabilities[key] = value
            num_capabilities += 1
            continue

        # 'KEY' : False
        data = re.match(
            r'''^\s*'([\S\s]+)'\s*:\s*False\s*[,}]?\s*$''', line)
        if data:
            key = data.group(1)
            value = False
            desired_capabilities[key] = value
            num_capabilities += 1
            continue

        # caps['KEY'] = 'VALUE'
        data = re.match(r"^\s*caps\['([\S\s]+)'\]\s*=\s*'([\S\s]+)'\s*$", line)
        if data:
            key = data.group(1)
            value = data.group(2)
            desired_capabilities[key] = value
            num_capabilities += 1
            continue

        # caps["KEY"] = "VALUE"
        data = re.match(r'^\s*caps\["([\S\s]+)"\]\s*=\s*"([\S\s]+)"\s*$', line)
        if data:
            key = data.group(1)
            value = data.group(2)
            desired_capabilities[key] = value
            num_capabilities += 1
            continue

        # caps['KEY'] = "VALUE"
        data = re.match(
            r'''^\s*caps\['([\S\s]+)'\]\s*=\s*"([\S\s]+)"\s*$''', line)
        if data:
            key = data.group(1)
            value = data.group(2)
            desired_capabilities[key] = value
            num_capabilities += 1
            continue

        # caps["KEY"] = 'VALUE'
        data = re.match(
            r'''^\s*caps\["([\S\s]+)"\]\s*=\s*'([\S\s]+)'\s*$''', line)
        if data:
            key = data.group(1)
            value = data.group(2)
            desired_capabilities[key] = value
            num_capabilities += 1
            continue

        # caps["KEY"] = True
        data = re.match(
            r'''^\s*caps\["([\S\s]+)"\]\s*=\s*True\s*$''', line)
        if data:
            key = data.group(1)
            value = True
            desired_capabilities[key] = value
            num_capabilities += 1
            continue

        # caps['KEY'] = True
        data = re.match(
            r'''^\s*caps\['([\S\s]+)'\]\s*=\s*True\s*$''', line)
        if data:
            key = data.group(1)
            value = True
            desired_capabilities[key] = value
            num_capabilities += 1
            continue

        # caps["KEY"] = False
        data = re.match(
            r'''^\s*caps\["([\S\s]+)"\]\s*=\s*False\s*$''', line)
        if data:
            key = data.group(1)
            value = False
            desired_capabilities[key] = value
            num_capabilities += 1
            continue

        # caps['KEY'] = False
        data = re.match(
            r'''^\s*caps\['([\S\s]+)'\]\s*=\s*False\s*$''', line)
        if data:
            key = data.group(1)
            value = False
            desired_capabilities[key] = value
            num_capabilities += 1
            continue

    if num_capabilities == 0:
        raise Exception("Unable to parse desired capabilities file!")

    return desired_capabilities
