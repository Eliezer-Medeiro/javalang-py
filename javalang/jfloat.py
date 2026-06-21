from typing import Union


class JFloat:
    # Construtor da classe JFloat
    def __init__(self, value: Union[float, int, str] = 0.0):
        if isinstance(value, str):
            try:
                self.value = float(value)
            except ValueError as e:
                raise ValueError(f"Invalid string for JFloat: '{value}'") from e
        else:
            self.value = float(value)
