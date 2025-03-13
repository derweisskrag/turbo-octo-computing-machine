"""Very basic calculator"""

class Calculator:
    def add(self, x: int, y: int) -> int:
        return x + y

    def subtract(self, x: int, y: int) -> int:
        return x - y if y > x else y - x

    def multiply(self, x: int, y: int) -> int:
        return x * y

    def divide(self, x: int, y: int) -> int:
        return x / y if y != 0 else 0
