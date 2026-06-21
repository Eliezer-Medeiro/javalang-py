import math
from typing import Union


class JFloat:
    # CONSTANTES IEEE 754
    MAX_VALUE = 3.4028235e+38
    MIN_VALUE = -3.4028235e+38
    MIN_NORMAL = 1.17549435e-38

    POSITIVE_INFINITY = float("inf")
    NEGATIVE_INFINITY = float("-inf")
    NaN = float("nan")

    MAX_EXPONENT = 127
    MIN_EXPONENT = -126
    SIZE = 32
    BYTES = 4

    def __init__(self, value: Union[float, int, str] = 0.0):
        if isinstance(value, str):
            try:
                self.value = float(value)
            except ValueError:
                raise ValueError("Invalid string for float")
        else:
            self.value = float(value)

    # 🔹 Instância
    def isNaN(self):
        return math.isnan(self.value)

    def isInfinite(self):
        return math.isinf(self.value)

    # 🔹 Estático
    @staticmethod
    def isNaNValue(value):
        return math.isnan(value)

    @staticmethod
    def isInfiniteValue(value):
        return math.isinf(value)

    @staticmethod
    def isFinite(value):
        return not (math.isnan(value) or math.isinf(value))
