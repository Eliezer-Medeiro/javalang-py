from typing import Union
import math


class JFloat:
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

    def __init__(self, value: Union[float, str] = 0.0):
        if isinstance(value, str):
            if value.strip() == "":
                raise ValueError("Empty string")
            self.value = float(value)
        else:
            self.value = float(value)

    def isNaN(self):
        return math.isnan(self.value)

    def isInfinite(self):
        return math.isinf(self.value)

    @staticmethod
    def isNaNValue(value: float):
        return math.isnan(value)

    @staticmethod
    def isInfiniteValue(value: float):
        return math.isinf(value)

    @staticmethod
    def isFinite(value: float):
        return not (math.isnan(value) or math.isinf(value))

    @staticmethod
    def parseFloat(s: str):
        if s is None or s.strip() == "":
            raise ValueError("Invalid string")
        return float(s)

    @staticmethod
    def valueOf(value):
        return float(value)
