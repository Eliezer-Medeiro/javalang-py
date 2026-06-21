from typing import Union
import math


class JFloat:
    # Constantes IEEE 754 (float 32 bits)
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
            try:
                self.value = float(value)
            except ValueError as e:
                raise ValueError(f"Invalid string for JFloat: '{value}'") from e
        else:
            self.value = float(value)

    # =========================
    # INSTANCE METHODS
    # =========================

    def isNaN(self):
        return math.isnan(self.value)

    def isInfinite(self):
        return math.isinf(self.value)

    def isFinite(self):
        return not (math.isnan(self.value) or math.isinf(self.value))

    # =========================
    # STATIC METHODS
    # =========================

    @staticmethod
    def isNaNValue(value: float):
        return math.isnan(value)

    @staticmethod
    def isInfiniteValue(value: float):
        return math.isinf(value)

    @staticmethod
    def isFiniteValue(value: float):
        return not (math.isnan(value) or math.isinf(value))

    @staticmethod
    def parseFloat(s: str):
        if s is None or s.strip() == "":
            raise ValueError("Invalid string")
        return float(s)

    @staticmethod
    def valueOf(value):
        return float(value)
@staticmethod
def compare(f1: float, f2: float):
    if math.isnan(f1) and math.isnan(f2):
        return 0
    if math.isnan(f1):
        return 1
    if math.isnan(f2):
        return -1
    if f1 == f2:
        return 0
    return -1 if f1 < f2 else 1
def compareTo(self, other):
    if isinstance(other, JFloat):
        other = other.value

    if math.isnan(self.value) and math.isnan(other):
        return 0
    if math.isnan(self.value):
        return 1
    if math.isnan(other):
        return -1

    if self.value == other:
        return 0
    return -1 if self.value < other else 1
@staticmethod
def max(f1: float, f2: float):
    return f1 if JFloat.compare(f1, f2) >= 0 else f2
@staticmethod
def min(f1: float, f2: float):
    return f1 if JFloat.compare(f1, f2) <= 0 else f2
