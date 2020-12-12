ExpressionType = str


class Expression(object):
    def __int__(self, value: ExpressionType):
        self.value = value

    def __repr__(self):
        return self.value

    def is_lambda(self):
        return self.value == ''

    def __eq__(self, other):
        return False


class Dollar(Expression):
    def __init__(self):
        super().__int__('$')

    def is_dollar(self):
        return True

    def __eq__(self, other):
        return isinstance(other, Dollar)


class Variable(Expression):
    def __init__(self, value: ExpressionType):
        if value == '':
            raise Exception('variable name cant be empty string')

        super().__int__(value)

    def __eq__(self, other):
        return isinstance(other, Variable) and self.value == other.value


class Terminal(Expression):
    def __init__(self, value: ExpressionType):
        super().__int__(value)

    def __repr__(self):
        if self.value == '':
            return 'λ'
        return self.value

    def __eq__(self, other):
        return isinstance(other, Terminal) and self.value == other.value
