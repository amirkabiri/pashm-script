class Actions:
    def __init__(self):
        self.stack = []
        self.code = []
        self.temp = []
        self.vars = {}

    def add_temp(self, value):
        self.temp.append(value)
        return len(self.temp) - 1

    def action_number(self, token):
        self.stack.append([
            'const',
            int(token['value'])
        ])

    def action_variable(self, token):
        self.stack.append([
            'vars',
            token['value']
        ])

    def action_assign(self, token):
        value = self.stack.pop()
        variable = self.stack.pop()
        self.code.append(['=', value, None, variable])

    def action_add(self, token):
        operand_a = self.stack.pop()
        operand_b = self.stack.pop()
        temp_index = self.add_temp(None)
        destination = ['temp', temp_index]

        self.code.append(['+', operand_a, operand_b, destination])
        self.stack.append(destination)

    def action_mult(self, token):
        operand_a = self.stack.pop()
        operand_b = self.stack.pop()
        temp_index = self.add_temp(None)
        destination = ['temp', temp_index]

        self.code.append(['*', operand_a, operand_b, destination])
        self.stack.append(destination)


