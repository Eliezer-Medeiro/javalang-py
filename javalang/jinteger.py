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

    #Implementação de métodos de conversão para tipos numéricos no JInteger
    def byteValue(self) -> int:
        """Retorna o valor do JInteger como um byte (8 bits)"""
        return (self.value + 128) % 256 - 128

    def shortValue(self) -> int:
        """Retorna o valor do JInteger como um short (16 bits)"""
        return (self.value + 32768) % 65536 - 32768

    def intValue(self) -> int:
        """Retorna o valor do JInteger como um int (32 bits)"""
        return self.value

    def longValue(self) -> int:
        """Retorna o valor do JInteger como um long (64 bits)"""
        return self.value


    #Implementação de métodos de conversão para ponto flutuante e texto no JInteger
    def floatValue(self) -> float:
        """Retorna o valor do JInteger como um float (32 bits)"""
        return float(self.value)

    def doubleValue(self) -> float:
        """Retorna o valor do JInteger como um double (64 bits)"""
        return float(self.value)

    def toString(self) -> str:
        """Retorna a representação string do valor do JInteger"""
        return str(self.value)

    # Implementação de métodos de comparação e igualdade no JInteger

    def hashCode(self) -> int:
        """Retorna o hash code do JInteger, que é o próprio valor inteiro"""
        return self.value

    def __hash__(self) -> int:
        """Permite que JInteger seja usado em estruturas de dados baseadas em hash"""
        return self.hashCode()

    def equals(self, other) -> bool:
        """Verifica se outro objeto é igual a este JInteger"""
        if isinstance(other, JInteger):
            return self.value == other.value
        return False

    def __eq__(self, other) -> bool:
        """Permite comparação de igualdade usando o operador =="""
        return self.equals(other)

    def compareTo(self, other) -> int:
        """Compara este JInteger com outro JInteger"""
        if not isinstance(other, JInteger):
            raise TypeError("Can only compare with another JInteger")
        return (self.value > other.value) - (self.value < other.value)
