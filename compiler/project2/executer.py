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
            if code[2] is None:
                set(code[3], +get(code[1]))
            else:
                set(code[3], get(code[1]) + get(code[2]))

        elif code[0] == '!':
            set(code[3], int(not get(code[1])))

        elif code[0] == '-':
            if code[2] is None:
                set(code[3], -get(code[1]))
            else:
                set(code[3], get(code[1]) - get(code[2]))


        elif code[0] == '*':
            set(code[3], get(code[1]) * get(code[2]))

        elif code[0] == '%':
            set(code[3], get(code[1]) % get(code[2]))

        elif code[0] == '>':
            set(code[3], int(get(code[1]) > get(code[2])))

        elif code[0] == '>=':
            set(code[3], int(get(code[1]) >= get(code[2])))

        elif code[0] == '<':
            set(code[3], int(get(code[1]) < get(code[2])))

        elif code[0] == '<=':
            set(code[3], int(get(code[1]) <= get(code[2])))

        elif code[0] == '==':
            set(code[3], int(get(code[1]) == get(code[2])))

        elif code[0] == '!=':
            set(code[3], int(get(code[1]) != get(code[2])))

        elif code[0] == '&&':
            set(code[3], int(get(code[1]) and get(code[2])))

        elif code[0] == '||':
            set(code[3], int(get(code[1]) or get(code[2])))

        elif code[0] == '^':
            set(code[3], get(code[1]) ** get(code[2]))

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

        elif code[0] == 'CALL':
            params = []
            for j in range(i - 1, i - code[2] - 1, -1):
                params.append(get(actions.code[j][1]))

            result = eval(f'{ code[1] }({ ",".join([str(p) for p in params]) })')

            if code[3] is not None:
                set(code[3], result)

        i += 1

    return actions