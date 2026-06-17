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
