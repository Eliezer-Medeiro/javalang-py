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

    def toString(self, i: int = None, radix: int = 10) -> str:
        """
        Implementação unificada de toString (instância) e toString (estático).
        Se 'i' for fornecido, comporta-se como o método estático do Java.
        Se 'i' for omitido, comporta-se como o método de instância.
        """
        if i is not None:
            # Lógica do método estático (convertendo base)
            if radix < 2 or radix > 36:
                raise ValueError("Radix must be between 2 and 36")
            if i < 0:
                # Nota: para os métodos estáticos, a especificação Java
                # para números negativos deve usar a máscara de 32 bits
                return JInteger.toString(None, i & 0xFFFFFFFF, radix)

            digits = "0123456789abcdefghijklmnopqrstuvwxyz"
            res = ""
            while i >= radix:
                res = digits[i % radix] + res
                i //= radix
            return digits[i] + res

        # Comporta-se como o método de instância original
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

    #implementar métodos estáticos de análise e fábricas (parseInt, valueOf, decode)
    @staticmethod
    def parseInt(s: str, radix: int = 10) -> int:
        """Implementação unificada de parseInt(s) e parseInt(s, radix)."""
        try:
            return int(s, radix)
        except ValueError as e:
            raise ValueError(f"Invalid string for parseInt: '{s}'") from e


    @staticmethod
    def parseUnsignedInt(s: str, radix: int = 10) -> int:
        """
        Implementação unificada de parseUnsignedInt(s) e
        parseUnsignedInt(s, radix).
        """
        value = int(s, radix)
        if value < 0 or value > 4294967295:
            raise ValueError(f"Value out of range for unsigned 32-bit int: '{s}'")
        return value


    @staticmethod
    def valueOf(val, radix: int = 10) -> 'JInteger':
        """Fábrica para criar JInteger a partir de int ou str."""
        if isinstance(val, int):
            return JInteger(val)
        return JInteger(int(val, radix))

    @staticmethod
    def decode(nm: str) -> 'JInteger':
        """Interpreta prefixos 0x, 0X, # e 0 (octal) conforme especificação Java."""
        if not nm:
            raise ValueError("String is empty")
        # Trata o prefixo # para hexadecimal
        if nm.startswith('#'):
            return JInteger(int(nm[1:], 16))

        if (
            nm.startswith('0') and len(nm) > 1 and
            not nm.lower().startswith(('0x', '0b'))
        ):
            # Se for '012', tratamos como octal (base 8)
            return JInteger(int(nm, 8))

        return JInteger(int(nm, 0))

    @staticmethod
    def toUnsignedString(i: int, radix: int = 10) -> str:
        """Retorna a representação string de um inteiro tratado como unsigned."""
        if i < 0:
            i += 1 << 32  # Tratar como unsigned
        return JInteger.toString(i, radix)

    @staticmethod
    def toBinaryString(i: int) -> str:
        """Retorna a representação binária de 32 bits (unsigned)."""
        # Aplica máscara para garantir 32 bits de representação (comportamento Java)
        return JInteger.toString(i & 0xFFFFFFFF, 2)

    @staticmethod
    def toOctalString(i: int) -> str:
        """Retorna a representação octal de 32 bits (unsigned)."""
        return JInteger.toString(i & 0xFFFFFFFF, 8)

    @staticmethod
    def toHexString(i: int) -> str:
        """Retorna a representação hexadecimal de 32 bits (unsigned)."""
        return JInteger.toString(i & 0xFFFFFFFF, 16)
