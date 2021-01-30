def executer(actions):
    def set(address, value):
        nonlocal actions
        if address[0] == 'const':
            return None
        getattr(actions, address[0])[address[1]] = value

    def get(address):
        nonlocal actions
        if address[0] == 'const':
            return address[1]
        return getattr(actions, address[0])[address[1]]

    i = 0
    while i < len(actions.code):
        code = actions.code[i]

        if code[0] == '+':
            set(code[3], get(code[1]) + get(code[2]))
        elif code[0] == '-':
            set(code[3], get(code[1]) - get(code[2]))
        elif code[0] == '*':
            set(code[3], get(code[1]) * get(code[2]))
        elif code[0] == '/':
            set(code[3], get(code[1]) / get(code[2]))
        elif code[0] == '=':
            set(code[3], get(code[1]))
        elif code[0] == 'JMP':
            i = code[1][1]
            continue
        elif code[0] == 'JMPT':
            if get(code[1]):
                i = code[2][1]
                continue
        elif code[0] == 'JMPF':
            if not get(code[1]):
                i = code[2][1]
                continue

        i += 1

    return actions