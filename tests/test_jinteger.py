import pytest

from javalang.jinteger import JInteger

def test_constants_integer():
    assert JInteger.MAX_VALUE == 2147483647
    assert JInteger.MIN_VALUE == -2147483648
    assert JInteger.SIZE == 32
    assert JInteger.BYTES == 4
    assert JInteger.TYPE is int

def test_constructor_integer():
    # Testando a criação de JInteger com um inteiro
    jint1 = JInteger(123)
    assert jint1.value == 123

    # Testando a criação de JInteger com uma string numérica
    jint2 = JInteger("456")
    assert jint2.value == 456

    # Testando a criação de JInteger com uma string inválida
    try:
        JInteger("abc")
        assert False, "Expected ValueError for invalid string"
    except ValueError as e:
        assert str(e) == "Invalid string for JInteger: 'abc'"

def test_value_methods_integer():
    jint = JInteger(300)

    # Testando byteValue
    assert jint.byteValue() == 44  # 300 mod 256 = 44

    # Testando shortValue
    assert jint.shortValue() == 300  # 300 fits in a short

    # Testando intValue
    assert jint.intValue() == 300

    # Testando longValue
    assert jint.longValue() == 300

def test_float_double_and_string_methods():
    jint = JInteger(123)

    # Testando floatValue
    assert jint.floatValue() == 123.0

    # Testando doubleValue
    assert jint.doubleValue() == 123.0

    # Testando toString
    assert jint.toString() == "123"


def test_hash_code_and_equality():
    jint1 = JInteger(123)
    jint2 = JInteger(123)
    jint3 = JInteger(456)

    # Testando hashCode
    assert jint1.hashCode() == 123
    assert jint2.hashCode() == 123
    assert jint3.hashCode() == 456

    # Testando igualdade
    assert jint1 == jint2
    assert jint1 != jint3
    assert jint1.equals(jint2)
    assert not jint1.equals(jint3)

    # Testando compareTo
    assert jint1.compareTo(jint2) == 0
    assert jint1.compareTo(jint3) < 0
    assert jint3.compareTo(jint1) > 0

    # Testando compareTo com um tipo diferente
    import pytest
    with pytest.raises(TypeError):
        jint1.compareTo(123)

def test_static_parsing_methods():
    # Testando parseInt
    assert JInteger.parseInt("123") == 123
    assert JInteger.parseInt("1010", 2) == 10
    assert JInteger.parseInt("FF", 16) == 255
    with pytest.raises(ValueError):
        JInteger.parseInt("abc")  # Base 10 padrão não aceita letras

    # Testando parseUnsignedInt
    assert JInteger.parseUnsignedInt("4294967295") == 4294967295
    assert JInteger.parseUnsignedInt("10", 16) == 16
    with pytest.raises(ValueError):
        JInteger.parseUnsignedInt("-1") # Deve falhar (unsigned)
    with pytest.raises(ValueError):
        JInteger.parseUnsignedInt("5000000000") # Excede 32 bits

    # Testando valueOf (Fábrica)
    j1 = JInteger.valueOf(100)
    assert isinstance(j1, JInteger)
    assert j1.value == 100

    j2 = JInteger.valueOf("200", 10)
    assert j2.value == 200

    j3 = JInteger.valueOf("10", 2)
    assert j3.value == 2

    # Testando decode
    assert JInteger.decode("0xAF").value == 175
    # O int(nm, 0) do Python precisa de ajuste para #
    assert JInteger.decode("#AF").value == 175
    # Octal (012 em octal é 10)
    assert JInteger.decode("012").value == 10

    #  testes de formatação
def test_formatting_methods():
    # Teste de toString padrão
    assert JInteger.toString(255, 16) == "ff"
    assert JInteger.toString(-255, 10) == "-255"

    # Testes de representação de 32 bits (Crucial para o Java)
    # -1 em complemento de dois de 32 bits é 32 uns
    assert JInteger.toBinaryString(-1) == "11111111111111111111111111111111"
    assert JInteger.toHexString(-1) == "ffffffff"

    # Teste Unsigned
    assert JInteger.toUnsignedString(-1) == "4294967295"

def test_bit_counting():
    # 0x0000000F = 15 (4 bits um)
    assert JInteger.bitCount(15) == 4
    # -1 em 32 bits é 0xFFFFFFFF (32 bits um)
    assert JInteger.bitCount(-1) == 32

def test_highest_lowest_one_bit():
    # 10 é 1010 em binário. Highest: 8 (1000), Lowest: 2 (0010)
    assert JInteger.highestOneBit(10) == 8
    assert JInteger.lowestOneBit(10) == 2
    assert JInteger.highestOneBit(0) == 0

def test_zeros_counting():
    # 1 (0...01). Liderança: 31 zeros, Trilha: 0 zeros
    assert JInteger.numberOfLeadingZeros(1) == 31
    assert JInteger.numberOfTrailingZeros(1) == 0
    # 0 tem 32 zeros de ambos os lados
    assert JInteger.numberOfLeadingZeros(0) == 32
    assert JInteger.numberOfTrailingZeros(0) == 32

def test_reversal():
    # Reverter 1 (000...001) vira 0x80000000 (-2147483648 em signed 32)
    assert JInteger.reverse(1) == -2147483648
    # Reverter bytes de 0x12345678 -> 0x78563412
    assert JInteger.reverseBytes(0x12345678) == 0x78563412

def test_rotation():
    # Rotação de 32 bits: 1 rodado 1 para esquerda vira 2
    assert JInteger.rotateLeft(1, 1) == 2
    # Rotação de 32 bits: 0x80000000 (-2147483648) rodado 1 para direita vira 1073741824
    assert JInteger.rotateRight(-2147483648, 1) == 1073741824

def test_signum():
    assert JInteger.signum(100) == 1
    assert JInteger.signum(-100) == -1
    assert JInteger.signum(0) == 0

def test_static_arithmetic():
    # Teste normal de soma
    assert JInteger.sum(10, 20) == 30

    # Teste crítico de Overflow do Java (Integer.MAX_VALUE + 1)
    # 2147483647 + 1 deve virar -2147483648
    assert JInteger.sum(2147483647, 1) == -2147483648

    # Testes de max e min
    assert JInteger.max(10, 20) == 20
    assert JInteger.max(-5, -10) == -5
    assert JInteger.min(10, 20) == 10
    assert JInteger.min(-5, -10) == -10

def test_unsigned_math_and_compare():
    # compare: normal vs com sinal
    # Em compare normal, -1 < 1 -> retorna -1
    assert JInteger.compare(-1, 1) == -1
    # Em compareUnsigned, -1 vira 4294967295, logo -1 > 1 -> retorna 1
    assert JInteger.compareUnsigned(-1, 1) == 1
    assert JInteger.compareUnsigned(5, 5) == 0

    # divideUnsigned: -1 (4294967295) // 2 = 2147483647
    assert JInteger.divideUnsigned(-1, 2) == 2147483647

    # remainderUnsigned: -1 (4294967295) % 10 = 5
    assert JInteger.remainderUnsigned(-1, 10) == 5

    # Teste de Exceção (Lançar ZeroDivisionError)
    with pytest.raises(ZeroDivisionError):
        JInteger.divideUnsigned(10, 0)

    with pytest.raises(ZeroDivisionError):
        JInteger.remainderUnsigned(10, 0)
