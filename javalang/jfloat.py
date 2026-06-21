import math

def isNaN(self):
    return math.isnan(self.value)

@staticmethod
def isNaNValue(value):
    return math.isnan(value)

def isInfinite(self):
    return math.isinf(self.value)

@staticmethod
def isInfiniteValue(value):
    return math.isinf(value)

@staticmethod
def isFinite(value):
    return not (math.isnan(value) or math.isinf(value))
