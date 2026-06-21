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

def test_jstring_access_and_size():
    # Inicialização para os testes
    s = JString("Java-Py")
    vazia = JString("")

    # 1. Teste length()
    assert s.length() == 7
    assert vazia.length() == 0

    # 2. Teste isEmpty()
    assert not s.isEmpty()
    assert vazia.isEmpty()

    # 3. Teste charAt(int) e limites
    assert s.charAt(0) == "J"
    assert s.charAt(4) == "-"
    assert s.charAt(6) == "y"
    with pytest.raises(IndexError):
        s.charAt(-1)
    with pytest.raises(IndexError):
        s.charAt(7)

    # 4. Teste toCharArray()
    assert s.toCharArray() == ["J", "a", "v", "a", "-", "P", "y"]
    assert vazia.toCharArray() == []

    # 5. Teste getBytes() padrão (UTF-8)
    assert s.getBytes() == b"Java-Py"

    # 6. Teste getBytes(String charset) com múltiplos encodings
    acentuada = JString("Olá")
    assert acentuada.getBytes("ISO-8859-1") == b"Ol\xe1"
    assert acentuada.getBytes("UTF-8") == b"Ol\xc3\xa1"

    # Teste de UnsupportedEncodingException via ValueError
    with pytest.raises(ValueError):
        s.getBytes("CHARSET_FALSO")


def test_jstring_access_code_points_and_get_chars():
    # 'A' (65), 'B' (66), '😀' (128512)
    s = JString("AB😀")

    # 1. Teste codePointAt(int)
    assert s.codePointAt(0) == 65
    assert s.codePointAt(2) == 128512
    with pytest.raises(IndexError):
        s.codePointAt(-1)
    with pytest.raises(IndexError):
        s.codePointAt(3)

    # 2. Teste codePointBefore(int)
    assert s.codePointBefore(1) == 65
    assert s.codePointBefore(3) == 128512
    with pytest.raises(IndexError):
        s.codePointBefore(0)
    with pytest.raises(IndexError):
        s.codePointBefore(4)

    # 3. Teste codePointCount(int, int)
    assert s.codePointCount(0, 3) == 3
    assert s.codePointCount(1, 3) == 2
    with pytest.raises(IndexError):
        s.codePointCount(-1, 2)
    with pytest.raises(IndexError):
        s.codePointCount(2, 1)

    # 4. Teste offsetByCodePoints(int, int)
    assert s.offsetByCodePoints(0, 2) == 2
    assert s.offsetByCodePoints(3, -2) == 1
    with pytest.raises(IndexError):
        s.offsetByCodePoints(0, 5)
    with pytest.raises(IndexError):
        s.offsetByCodePoints(1, -3)

    # 5. Teste getChars(int, int, char[], int)
    destino = ["-", "-", "-", "-", "-"]
    s.getChars(0, 2, destino, 1)  # Copia "AB" para as posições 1 e 2
    assert destino == ["-", "A", "B", "-", "-"]

    # Testes de exceção para getChars
    with pytest.raises(IndexError):
        s.getChars(-1, 2, destino, 0)
    with pytest.raises(IndexError):
        s.getChars(0, 2, destino, 4)  # Fora dos limites do destino
