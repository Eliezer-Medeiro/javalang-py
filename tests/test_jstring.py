import pytest
from javalang.jstring import JString

class MockStringBuilder:
    def toString(self):
        return "conteudo_buffer"

def test_jstring_all_constructors():
    # Teste vazia e clonagem
    assert str(JString()) == ""
    assert str(JString("Teste")) == "Teste"
    assert str(JString(JString("Clone"))) == "Clone"

    # Teste char[] completo e com offset/count
    assert str(JString(['a', 'b', 'c', 'd'])) == "abcd"
    assert str(JString(['a', 'b', 'c', 'd'], 1, 2)) == "bc"

    # Teste de IndexError em char[]
    with pytest.raises(IndexError):
        JString(['a', 'b'], 1, 5)

    # Teste byte[] com encodings e parcial
    assert str(JString(b"cafe")) == "cafe"
    assert str(JString(b"abcdef", 2, 3)) == "cde"
    assert str(JString("Olá".encode("iso-8859-1"), "ISO-8859-1")) == "Olá"

    # Teste int[] codePoints (Ex: 128512 é o emoji 😀)
    assert str(JString([65, 66, 128512], 1, 2)) == "B😀"

    # Teste StringBuilder
    assert str(JString(MockStringBuilder())) == "conteudo_buffer"
