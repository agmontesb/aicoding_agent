
import sys
from pkg.calculator import Calculator
from pkg.render import render


def main():
    calculator = Calculator()
    if len(sys.argv) <= 1:
        print('Calculator App.')
        print('Usage: python main.py "expression"')
        print('Example: python main.py "2+2"')
        expression = input("Please enter an expression or type QUIT to exit:  ")
        if expression.upper() == "QUIT":
            sys.exit(0)
        expression = expression.strip()
    else:
        expression = " ".join(sys.argv[1:])
    result = calculator.evaluate(expression)
    to_print = render(expression, result)
    print(to_print)

if __name__ == "__main__":
    main()