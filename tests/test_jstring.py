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

class MockStringBuilderJava:
    def toString(self):
        return "Java"

def test_jstring_equality_and_hashing():
    s1 = JString("Java")
    s2 = JString("Java")
    s3 = JString("java")

    # equals e __eq__
    assert s1.equals(s2)
    assert s1 == s2
    assert s1 != s3
    assert not s1.equals("Java") # equals nativo deve exigir o mesmo tipo

    # equalsIgnoreCase
    assert s1.equalsIgnoreCase(s3)
    assert s1.equalsIgnoreCase("JAVA")

    # contentEquals (aceita str e Mock)
    assert s1.contentEquals("Java")
    assert s1.contentEquals(MockStringBuilderJava())

    # hashCode (A fórmula para "A" é 65, para "AB" é 65*31 + 66 = 2081)
    assert JString("A").hashCode() == 65
    assert JString("AB").hashCode() == 2081
    # Hash nativo do Python mapeado
    assert hash(s1) == s1.hashCode()
    # Uso num set (valida __hash__ e __eq__)
    my_set = {s1}
    assert s2 in my_set

def test_jstring_compare_and_region():
    s1 = JString("ABC")
    s2 = JString("ABE")
    s3 = JString("abc")

    # compareTo
    # 'C' (67) - 'E' (69) = -2
    assert s1.compareTo(s2) == -2
    # s1 é menor que algo maior ("ABCD")
    assert s1.compareTo(JString("ABCD")) == -1 # dif de length 3 - 4 = -1

    with pytest.raises(TypeError):
        s1.compareTo("ABE")

    # compareToIgnoreCase
    assert s1.compareToIgnoreCase(s3) == 0

    # regionMatches(toffset, other, ooffset, len)
    # Testa "BC" dentro de "ABC" vs "BC" dentro de "XBCY"
    assert s1.regionMatches(1, JString("XBCY"), 1, 2)
    assert not s1.regionMatches(1, JString("XbcY"), 1, 2)

    # regionMatches(ignoreCase, toffset, other, ooffset, len)
    assert s1.regionMatches(True, 1, JString("XbcY"), 1, 2)

    # Teste de limites negativos/fora da string
    assert not s1.regionMatches(0, JString("X"), 0, 50)
    assert not s1.regionMatches(-1, JString("X"), 0, 1)
