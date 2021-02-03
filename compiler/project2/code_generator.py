class Actions:
    def __init__(self):
        self.stack = []
        self.code = []
        self.temp = []
        self.vars = {}

    def before(self, action, token):
        pass

    def after(self, action, token):
        pass

    def add_temp(self, value):
        self.temp.append(value)
        return len(self.temp) - 1

    def action_number(self, token):
        value = token['value']
        self.stack.append([
            'const',
            float(value) if '.' in value else int(value)
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
        operand_b = self.stack.pop()
        operand_a = self.stack.pop()
        temp_index = self.add_temp(None)
        destination = ['temp', temp_index]

        self.code.append(['+', operand_a, operand_b, destination])
        self.stack.append(destination)

    def action_subtract(self, token):
        operand_b = self.stack.pop()
        operand_a = self.stack.pop()
        temp_index = self.add_temp(None)
        destination = ['temp', temp_index]

        self.code.append(['-', operand_a, operand_b, destination])
        self.stack.append(destination)

    def action_multiply(self, token):
        operand_b = self.stack.pop()
        operand_a = self.stack.pop()
        temp_index = self.add_temp(None)
        destination = ['temp', temp_index]

        self.code.append(['*', operand_a, operand_b, destination])
        self.stack.append(destination)

    def action_pow(self, token):
        operand_b = self.stack.pop()
        operand_a = self.stack.pop()
        temp_index = self.add_temp(None)
        destination = ['temp', temp_index]

        self.code.append(['^', operand_a, operand_b, destination])
        self.stack.append(destination)

    def action_divide(self, token):
        operand_b = self.stack.pop()
        operand_a = self.stack.pop()
        temp_index = self.add_temp(None)
        destination = ['temp', temp_index]

        self.code.append(['/', operand_a, operand_b, destination])
        self.stack.append(destination)

    def action_save(self, token):
        self.stack.append(['save', len(self.code)])
        self.code.append(['NOP', None, None, None])

    def action_label(self, token):
        self.stack.append(['label', len(self.code)])

    def action_if(self, token):
        index = self.stack.pop()[1]
        self.code[index] = ['JMPF', self.stack.pop(), ['code', len(self.code)], None]

    def action_while(self, token):
        save = self.stack.pop()
        expression = self.stack.pop()
        label = self.stack.pop()

        self.code[save[1]] = ['JMPF', expression, ['code', len(self.code) + 1], None]
        self.code.append(['JMP', ['code', label[1]], None, None])

    def action_do_while(self, token):
        expression = self.stack.pop()
        label = self.stack.pop()

        self.code.append(['JMPT', expression, ['code', label[1]], None])

    def action_function(self, token):
        self.stack.append(['function', token['value']])

    def action_call(self, token):
        count = 0
        temp_index = self.add_temp(None)
        destination = ['temp', temp_index]

        for i in range(len(self.stack) - 1, -1, -1):
            head = self.stack[i]
            if isinstance(head, list) and head[0] == 'function':
                self.code.append(['CALL', head[1], count, destination])
                break

            self.code.append(['PARAM', head, None, None])
            count += 1

        for i in range(count + 1):
            self.stack.pop()

        self.stack.append(destination)

    def action_void_call(self, token):
        count = 0

        for i in range(len(self.stack) - 1, -1, -1):
            head = self.stack[i]
            if isinstance(head, list) and head[0] == 'function':
                self.code.append(['CALL', head[1], count, None])
                break

            self.code.append(['PARAM', head, None, None])
            count += 1

        for i in range(count + 1):
            self.stack.pop()

    def action_not(self, token):
        operand = self.stack.pop()
        temp_index = self.add_temp(None)
        destination = ['temp', temp_index]

        self.code.append(['!', operand, None, destination])
        self.stack.append(destination)

    def action_unary_minus(self, token):
        operand = self.stack.pop()
        temp_index = self.add_temp(None)
        destination = ['temp', temp_index]

        self.code.append(['-', operand, None, destination])
        self.stack.append(destination)

    def action_unary_plus(self, token):
        operand = self.stack.pop()
        temp_index = self.add_temp(None)
        destination = ['temp', temp_index]

        self.code.append(['+', operand, None, destination])
        self.stack.append(destination)

    def action_modulo(self, token):
        operand_b = self.stack.pop()
        operand_a = self.stack.pop()
        temp_index = self.add_temp(None)
        destination = ['temp', temp_index]

        self.code.append(['%', operand_a, operand_b, destination])
        self.stack.append(destination)

    def action_less_than(self, token):
        operand_b = self.stack.pop()
        operand_a = self.stack.pop()
        temp_index = self.add_temp(None)
        destination = ['temp', temp_index]

        self.code.append(['<', operand_a, operand_b, destination])
        self.stack.append(destination)

    def action_less_than_and_equal(self, token):
        operand_b = self.stack.pop()
        operand_a = self.stack.pop()
        temp_index = self.add_temp(None)
        destination = ['temp', temp_index]

        self.code.append(['<=', operand_a, operand_b, destination])
        self.stack.append(destination)

    def action_greater_than(self, token):
        operand_b = self.stack.pop()
        operand_a = self.stack.pop()
        temp_index = self.add_temp(None)
        destination = ['temp', temp_index]

        self.code.append(['>', operand_a, operand_b, destination])
        self.stack.append(destination)

    def action_greater_than_and_equal(self, token):
        operand_b = self.stack.pop()
        operand_a = self.stack.pop()
        temp_index = self.add_temp(None)
        destination = ['temp', temp_index]

        self.code.append(['>=', operand_a, operand_b, destination])
        self.stack.append(destination)

    def action_equal(self, token):
        operand_b = self.stack.pop()
        operand_a = self.stack.pop()
        temp_index = self.add_temp(None)
        destination = ['temp', temp_index]

        self.code.append(['==', operand_a, operand_b, destination])
        self.stack.append(destination)

    def action_not_equal(self, token):
        operand_b = self.stack.pop()
        operand_a = self.stack.pop()
        temp_index = self.add_temp(None)
        destination = ['temp', temp_index]

        self.code.append(['!=', operand_a, operand_b, destination])
        self.stack.append(destination)

    def action_and(self, token):
        operand_b = self.stack.pop()
        operand_a = self.stack.pop()
        temp_index = self.add_temp(None)
        destination = ['temp', temp_index]

        self.code.append(['&&', operand_a, operand_b, destination])
        self.stack.append(destination)

    def action_or(self, token):
        operand_b = self.stack.pop()
        operand_a = self.stack.pop()
        temp_index = self.add_temp(None)
        destination = ['temp', temp_index]

        self.code.append(['||', operand_a, operand_b, destination])
        self.stack.append(destination)
