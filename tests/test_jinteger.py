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

