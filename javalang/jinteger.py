from typing import Final, Type, Union


class JInteger:
    #Contantes Oficiais da Classe Integer do Java SE 8
    MAX_VALUE: Final[int] = 2147483647
    MIN_VALUE: Final[int] = -2147483648
    SIZE: Final[int] = 32
    BYTES: Final[int] = 4

    #TYPE representa o tipo primitivo int do Java SE 8
    TYPE: Final[Type[int]] = int

    # Construtores, se receber uma string "123" é transformado em inteiro 123
    def __init__(self, value: Union[int, str]=0):
        if isinstance(value, str):
            try:
                self.value = int(value)
            except ValueError as e:
                raise ValueError(f"Invalid string for JInteger: '{value}'") from e
        else:
            self.value = int(value)

