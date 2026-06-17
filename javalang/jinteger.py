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

    def toString(self, *args, **kwargs) -> str:
        """
        Implementação unificada de toString (instância) e toString (estático).
        Preserva rigorosamente o nome exigido e resolve o erro F811.
        """
        # Se foi chamado estaticamente: JInteger.toString(255, 16)
        # O 'self' na verdade será o primeiro número inteiro enviado
        if isinstance(self, int) or len(args) > 0 or "i" in kwargs:
            # Descobre quem é o 'i' e quem é o 'radix' baseado em como foi chamado
            if isinstance(self, int):
                i = self
                radix = args[0] if len(args) > 0 else kwargs.get("radix", 10)
            else:
                i = args[0] if len(args) > 0 else kwargs.get("i")
                radix = args[1] if len(args) > 1 else kwargs.get("radix", 10)

            if radix < 2 or radix > 36:
                raise ValueError("Radix must be between 2 and 36")

            if i == 0:
                return "0"

            if i < 0:
                # Caso seja negativo, reaproveita a lógica com o valor positivo
                return '-' + JInteger.toString(-i, radix)

            digits = "0123456789abcdefghijklmnopqrstuvwxyz"
            result = ""
            n = i
            while n > 0:
                result = digits[n % radix] + result
                n //= radix
            return result

        # Se foi chamado como instância: obj.toString()
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
    def toBinaryString(i: int) -> str:
        """Retorna a representation binária de um inteiro."""
        return JInteger.toString(i & 0xFFFFFFFF, 2)

    @staticmethod
    def toOctalString(i: int) -> str:
        """Retorna a representação octal de um inteiro."""
        return JInteger.toString(i & 0xFFFFFFFF, 8)

    @staticmethod
    def toHexString(i: int) -> str:
        """Retorna a representação hexadecimal de um inteiro."""
        return JInteger.toString(i & 0xFFFFFFFF, 16)

    @staticmethod
    def toUnsignedString(i: int, radix: int = 10) -> str:
        """Retorna a representação string de um inteiro tratado como unsigned."""
        if i < 0:
            i += 1 << 32
        return JInteger.toString(i, radix)

    # Métodos adicionais para manipulação de bits, como bitCount e highestOneBit
    @staticmethod
    def _to_signed_32(n: int) -> int:
        n &= 0xFFFFFFFF
        return n - 0x100000000 if n & 0x80000000 else n

    @staticmethod
    def bitCount(i: int) -> int:
        return bin(i & 0xFFFFFFFF).count('1')

    @staticmethod
    def highestOneBit(i: int) -> int:
        i &= 0xFFFFFFFF
        if i == 0:
            return 0
        return JInteger._to_signed_32(1 << (i.bit_length() - 1))

    # Metodo lowestOneBit e numberOfLeadingZeros e numberOfTrailingZeros
    @staticmethod
    def lowestOneBit(i: int) -> int:
        i &= 0xFFFFFFFF
        return JInteger._to_signed_32(i & (~i + 1))

    @staticmethod
    def numberOfLeadingZeros(i: int) -> int:
        i &= 0xFFFFFFFF
        return 32 - i.bit_length() if i != 0 else 32

    @staticmethod
    def numberOfTrailingZeros(i: int) -> int:
        i &= 0xFFFFFFFF
        return (i & (~i + 1)).bit_length() - 1 if i != 0 else 32

    # Métodos adicionais para manipulação de bits, como reverse e rotateLeft
    @staticmethod
    def reverse(i: int) -> int:
        i &= 0xFFFFFFFF
        return JInteger._to_signed_32(int(f"{i:032b}"[::-1], 2))

    @staticmethod
    def reverseBytes(i: int) -> int:
        i &= 0xFFFFFFFF
        return JInteger._to_signed_32(((i >> 24) & 0xFF) | ((i >> 8) & 0xFF00) |
                                      ((i << 8) & 0xFF0000) | ((i << 24) & 0xFF000000))

    @staticmethod
    def rotateLeft(i: int, distance: int) -> int:
        i &= 0xFFFFFFFF
        dist = distance & 31
        res = ((i << dist) | (i >> (32 - dist))) & 0xFFFFFFFF
        return JInteger._to_signed_32(res)

    @staticmethod
    def rotateRight(i: int, distance: int) -> int:
        i &= 0xFFFFFFFF  # Trata como 32 bits unsigned
        dist = distance & 31
        # Rotaciona como unsigned e aplica a máscara
        res = ((i >> dist) | (i << (32 - dist))) & 0xFFFFFFFF
        return JInteger._to_signed_32(res)

    @staticmethod
    def signum(i: int) -> int:
        return 1 if i > 0 else (-1 if i < 0 else 0)

    # Aritmetica estatica
    @staticmethod
    def sum(a: int, b: int) -> int:
        """Retorna a soma de dois inteiros simulando overflow de 32 bits."""
        return JInteger._to_signed_32(a + b)

    @staticmethod
    def max(a: int, b: int) -> int:
        return JInteger._to_signed_32(a if a > b else b)

    @staticmethod
    def min(a: int, b: int) -> int:
        return a if a < b else b

