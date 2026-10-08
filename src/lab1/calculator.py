"""Калькулятор арифметических выражений."""

from typing import List, Optional, Union

Token = Union[float, str]


def tokenize(expression: str) -> List[Token]:
    """Разделить выражение на числа, скобки и знаки."""
    tokens: List[Token] = []
    i = 0
    while i < len(expression):
        char = expression[i]
        if char.isspace():
            i += 1
            continue
        if char.isdigit() or char == ".":
            j = i
            while j < len(expression) and (expression[j].isdigit() or expression[j] == "."):
                j += 1
            tokens.append(float(expression[i:j]))
            i = j
        elif char in "+-*/()":
            tokens.append(char)
            i += 1
        else:
            raise ValueError(f"Unexpected character: {char}")
    return tokens


class Parser:
    """Рекурсивный парсер арифметического выражения."""

    def __init__(self, tokens: List[Token]) -> None:
        self.tokens = tokens
        self.pos = 0

    def peek(self) -> Optional[Token]:
        """Вернуть текущий токен без переходов."""
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def consume(self) -> Token:
        """Вернуть текущий токен и перейти к следующему."""
        token = self.peek()
        if token is None:
            raise ValueError("Unexpected end of expression")
        self.pos += 1
        return token

    def parse(self) -> float:
        """Парсинг полного выражения."""
        result = self.expression()
        if self.peek() is not None:
            raise ValueError("Unexpected token at the end of expression")
        return result

    def expression(self) -> float:
        """Парсинг сложения и вычитания."""
        result = self.term()
        while self.peek() in ("+", "-"):
            op = self.consume()
            right = self.term()
            if op == "+":
                result += right
            else:
                result -= right
        return result

    def term(self) -> float:
        """Парсинг умножения и деления."""
        result = self.factor()
        while self.peek() in ("*", "/"):
            op = self.consume()
            right = self.factor()
            if op == "*":
                result *= right
            else:
                if right == 0:
                    raise ZeroDivisionError("division by zero")
                result /= right
        return result

    def factor(self) -> float:
        """Парсинг чисел, знаков и скобок."""
        token = self.peek()
        if token == "-":
            self.consume()
            return -self.factor()
        if token == "+":
            self.consume()
            return self.factor()
        if token == "(":
            self.consume()
            result = self.expression()
            if self.peek() != ")":
                raise ValueError("Missing closing parenthesis")
            self.consume()
            return result
        if isinstance(token, float):
            self.consume()
            return token
        raise ValueError(f"Unexpected token: {token}")


def calculate(expression: str) -> float:
    """
    Посчитать арифметическое выражение.

    >>> calculate("2+2")
    4.0
    >>> calculate("2*2")
    4.0
    >>> calculate("2/2")
    1.0
    >>> calculate("2-2")
    0.0
    >>> calculate("2+2*2")
    6.0
    >>> calculate("(2+2)*2")
    8.0
    """
    tokens = tokenize(expression)
    parser = Parser(tokens)
    return parser.parse()
