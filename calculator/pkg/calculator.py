import re

class Calculator:
    def __init__(self):
        self.operators = {
            '+': lambda a, b: a + b,
            '-': lambda a, b: a - b,
            '*': lambda a, b: a * b,
            '/': lambda a, b: a / b,
        }

        self.precedence = {
            '+': 1,
            '-': 1,
            '*': 2,
            '/': 2,
        }

    def evaluate(self, expression):
        tokens = [token for token in re.split(r'(\+|\(|\)|-|\*|/)', expression.replace(' ', '')) if token]
        return self._evaluate_infix(tokens)

    def _evaluate_infix(self, tokens):
        values = []
        operators = []
        parentheses = []

        start = 0
        for token in tokens:
            if token in self.operators:
                while(
                    operators[start:]
                    and self.precedence[operators[-1]] >= self.precedence[token]
                ):
                    values = self._apply_operator(operators, values)
                operators.append(token)
            else:
                if token == '(':
                    start = len(operators)
                    parentheses.append(start)
                elif token == ')':
                    try:
                        start = parentheses.pop()
                    except IndexError:
                        raise ValueError('Unbalanced parentheses')
                    while len(operators[start:]):
                        values = self._apply_operator(operators, values)
                    start = parentheses.pop() if len(parentheses) else 0
                else:
                    try:
                        values.append(float(token))
                    except ValueError:
                        raise ValueError(f'Invalid token "{token}"')

        while operators:
            values = self._apply_operator(operators, values)
        if len(values) != 1:
            raise ValueError('invalid expression')
        return values[0]

    def _apply_operator(self, operators, values):
        if not operators:
            return
        
        operator = operators.pop()
        if len(values) < 2:
            raise ValueError(f'not enough operands for operator "{operator}"')
        b = values.pop()
        a = values.pop()
        result = self.operators[operator](a, b)
        values.append(result)
        return values
    
if __name__ == '__main__':
    calculator = Calculator()
    calculator.evaluate('2*(2 + 2)')