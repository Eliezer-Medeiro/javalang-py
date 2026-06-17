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
