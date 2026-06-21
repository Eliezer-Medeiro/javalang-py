import pytest
from javalang.jfloat import JFloat


def test_constructor_float():
    # Testando a criação de JFloat com um float
    jfloat = JFloat(1.5)
    assert jfloat.value == 1.5


def test_constructor_int():
    # Testando a criação de JFloat com um inteiro
    jfloat = JFloat(10)
    assert jfloat.value == 10.0


def test_constructor_string():
    # Testando a criação de JFloat com uma string numérica
    jfloat = JFloat("2.5")
    assert jfloat.value == 2.5


def test_constructor_invalid_string():
    # Testando a criação de JFloat com uma string inválida
    with pytest.raises(ValueError):
        JFloat("abc")

