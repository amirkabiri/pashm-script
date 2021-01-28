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

    for code in actions.code:
        if code[0] == '+':
            set(code[3], get(code[1]) + get(code[2]))
        elif code[0] == '*':
            set(code[3], get(code[1]) * get(code[2]))
        elif code[0] == '=':
            set(code[3], get(code[1]))

    return actions