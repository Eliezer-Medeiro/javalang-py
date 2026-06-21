from __future__ import annotations
from typing import List, Union, Optional, Any


class JString:
    def __init__(
        self,
        value: Optional[
            Union[str, JString, List[str], bytes, List[int], Any]
        ] = None,
        arg2: Optional[Union[int, str]] = None,
        arg3: Optional[int] = None,
    ):
        """Construtores unificados para paridade com java.lang.String (Java SE 8)."""
        # 1. String()
        if value is None:
            self.value = ""
            return

        # 2. String(String original) ou String nativa do Python
        if isinstance(value, JString):
            self.value = value.value
            return
        if isinstance(value, str):
            self.value = value
            return

        # 3. String(StringBuilder)
        if type(value).__name__ == "StringBuilder" or hasattr(value, "toString"):
            self.value = (
                value.toString() if hasattr(value, "toString") else str(value)
            )
            return

        # Tratamento de Listas: char[] ou int[] codePoints
        if isinstance(value, list):
            if not value:
                self.value = ""
                return

            if isinstance(arg2, int) and isinstance(arg3, int):
                offset, count = arg2, arg3
                if offset < 0 or count < 0 or (offset + count) > len(value):
                    msg = "IndexOutOfBoundsException: limites invalidos"
                    raise IndexError(msg)
                sub_list = value[offset : offset + count]
            else:
                sub_list = value

            if all(isinstance(x, int) for x in sub_list):
                self.value = "".join(chr(cp) for cp in sub_list)
            else:
                self.value = "".join(str(ch) for ch in sub_list)
            return

        # Tratamento de byte[]
        if isinstance(value, (bytes, bytearray)):
            # Analisa assinaturas baseando em arg2 e arg3
            if isinstance(arg2, int) and isinstance(arg3, int):
                offset, length = arg2, arg3
                if offset < 0 or length < 0 or (offset + length) > len(value):
                    msg = "IndexOutOfBoundsException: limites invalidos"
                    raise IndexError(msg)
                byte_data = value[offset : offset + length]
                charset = "utf-8"

            elif isinstance(arg2, str):
                byte_data = value
                charset = self._map_charset(arg2)

            else:
                byte_data = value
                charset = "utf-8"

            try:
                self.value = byte_data.decode(charset, errors="replace")
            except LookupError:
                msg = f"UnsupportedEncodingException: {arg2}"
                raise ValueError(msg)
            return

        raise ValueError("Invalid type for JString constructor")

    def _map_charset(self, java_charset: str) -> str:
        """Mapeia os charsets padrao do Java para o identificador do Python."""
        mapping = {
            "UTF-16BE": "utf-16-be",
            "UTF-16LE": "utf-16-le",
            "UTF-16": "utf-16",
            "US-ASCII": "ascii",
            "ISO-8859-1": "iso-8859-1",
            "UTF-8": "utf-8",
        }
        return mapping.get(java_charset, java_charset)

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return f"JString('{self.value}')"

    def length(self) -> int:
        """Retorna o comprimento da string."""
        return len(self.value)

    def isEmpty(self) -> bool:
        """Retorna true se length() for 0."""
        return len(self.value) == 0

    def charAt(self, index: int) -> str:
        """Retorna o valor char no indice especificado."""
        if index < 0 or index >= len(self.value):
            msg = f"String index out of range: {index}"
            raise IndexError(msg)
        return self.value[index]

    def toCharArray(self) -> List[str]:
        """Converte esta string em um novo array de caracteres."""
        return list(self.value)

    def getBytes(self, charsetName: Optional[str] = None) -> bytes:
        """Codifica esta JString em uma sequencia de bytes."""
        if charsetName is None:
            return self.value.encode("utf-8")

        python_charset = self._map_charset(charsetName)
        try:
            return self.value.encode(python_charset)
        except LookupError:
            msg = f"UnsupportedEncodingException: {charsetName}"
            raise ValueError(msg)

    def codePointAt(self, index: int) -> int:
        """Retorna o codigo Unicode (Code Point) no indice dado."""
        if index < 0 or index >= len(self.value):
            msg = f"String index out of range: {index}"
            raise IndexError(msg)
        return ord(self.value[index])

    def codePointBefore(self, index: int) -> int:
        """Retorna o codigo Unicode no indice anterior ao fornecido."""
        if index < 1 or index > len(self.value):
            msg = f"String index out of range: {index}"
            raise IndexError(msg)
        return ord(self.value[index - 1])

    def codePointCount(self, beginIndex: int, endIndex: int) -> int:
        """Retorna o numero de Code Points no intervalo especificado."""
        if (
            beginIndex < 0
            or endIndex > len(self.value)
            or beginIndex > endIndex
        ):
            msg = "IndexOutOfBoundsException: indices invalidos"
            raise IndexError(msg)
        # Em Python nativo, cada elemento de str já representa um code point
        return len(self.value[beginIndex:endIndex])

    def offsetByCodePoints(self, index: int, codePointOffset: int) -> int:
        """Retorna o indice deslocado pelo offset de Code Points."""
        if index < 0 or index > len(self.value):
            msg = f"String index out of range: {index}"
            raise IndexError(msg)
        target = index + codePointOffset
        if target < 0 or target > len(self.value):
            msg = "IndexOutOfBoundsException: deslocamento invalido"
            raise IndexError(msg)
        return target

    def getChars(
        self, srcBegin: int, srcEnd: int, dst: list, dstBegin: int
    ) -> None:
        """Copia os caracteres desta string para o array de destino."""
        if (
            srcBegin < 0
            or srcEnd > len(self.value)
            or srcBegin > srcEnd
        ):
            msg = "IndexOutOfBoundsException: limites da origem invalidos"
            raise IndexError(msg)

        chars_to_copy = list(self.value[srcBegin:srcEnd])
        length = len(chars_to_copy)

        if dstBegin < 0 or (dstBegin + length) > len(dst):
            msg = "IndexOutOfBoundsException: limites do destino invalidos"
            raise IndexError(msg)

        # Modifica a lista destino in-place
        dst[dstBegin : dstBegin + length] = chars_to_copy

    def equals(self, anObject: Any) -> bool:
        """Compara esta string com o objeto especificado."""
        return self == anObject

    def __eq__(self, other: Any) -> bool:
        """Dunder method para suportar o operador == do Python nativamente."""
        if isinstance(other, JString):
            return self.value == other.value
        return False

    def equalsIgnoreCase(self, anotherString: Union[str, 'JString']) -> bool:
        """Compara esta string com outra, ignorando consideracoes de caixa."""
        if isinstance(anotherString, JString):
            other_val = anotherString.value
        else:
            other_val = str(anotherString)
        return self.value.lower() == other_val.lower()

    def compareTo(self, anotherString: 'JString') -> int:
        """Compara duas strings lexicograficamente."""
        if not isinstance(anotherString, JString):
            raise TypeError("compareTo exige um objeto JString")

        len1, len2 = len(self.value), len(anotherString.value)
        lim = min(len1, len2)

        for k in range(lim):
            c1, c2 = self.value[k], anotherString.value[k]
            if c1 != c2:
                return ord(c1) - ord(c2)
        return len1 - len2

    def compareToIgnoreCase(self, anotherString: 'JString') -> int:
        """Compara duas strings lexicograficamente, ignorando caixa."""
        if not isinstance(anotherString, JString):
            raise TypeError("compareToIgnoreCase exige um objeto JString")

        # Cria cópias temporárias em minúsculas e aplica a mesma lógica
        temp_self = JString(self.value.lower())
        temp_other = JString(anotherString.value.lower())
        return temp_self.compareTo(temp_other)

    def contentEquals(self, cs: Any) -> bool:
        """Compara esta string a um CharSequence (ex: StringBuilder, str)."""
        if isinstance(cs, JString):
            return self.value == cs.value
        if isinstance(cs, str):
            return self.value == cs
        if hasattr(cs, "toString"):
            return self.value == cs.toString()
        return False

    def regionMatches(
        self, arg1: Any, arg2: Any, arg3: Any, arg4: Any, arg5: Any = None
    ) -> bool:
        """Testa se duas regioes de string sao iguais, lidando com sobrecarga."""
        if arg5 is None:
            # Assinatura: regionMatches(toffset, other, ooffset, len)
            ignoreCase, toffset, other, ooffset, length = False, arg1, arg2, arg3, arg4
        else:
            # Assinatura: regionMatches(ignoreCase, toffset, other, ooffset, len)
            ignoreCase, toffset, other, ooffset, length = arg1, arg2, arg3, arg4, arg5

        other_str = other.value if isinstance(other, JString) else str(other)

        # Validações de limites impostas pelo Java (Quebradas para o Ruff)
        if (
            toffset < 0
            or ooffset < 0
            or toffset + length > len(self.value)
            or ooffset + length > len(other_str)
        ):
            return False

        s1 = self.value[toffset : toffset + length]
        s2 = other_str[ooffset : ooffset + length]

        if ignoreCase:
            return s1.lower() == s2.lower()
        return s1 == s2

    def hashCode(self) -> int:
        """Retorna o codigo hash (formula exata do Java com overflow de 32 bits)."""
        h = 0
        for char in self.value:
            # h = 31 * h + char, mascarado para 32 bits sem sinal
            h = (31 * h + ord(char)) & 0xFFFFFFFF
        # Converte para int de 32 bits com sinal
        return h if h < 0x80000000 else h - 0x100000000

    def __hash__(self) -> int:
        """Dunder method para tornar JString 'hashable' em sets e dicts."""
        return self.hashCode()

    def indexOf(
        self, ch_or_str: Union[int, str, 'JString'], fromIndex: int = 0
    ) -> int:
        """Retorna o indice da primeira ocorrencia do caractere ou substring."""
        if isinstance(ch_or_str, JString):
            target = ch_or_str.value
        elif isinstance(ch_or_str, int):
            target = chr(ch_or_str)
        else:
            target = str(ch_or_str)

        # Java trata indices negativos em indexOf como 0
        from_idx = max(0, fromIndex)
        return self.value.find(target, from_idx)

    def lastIndexOf(
        self, ch_or_str: Union[int, str, 'JString'], fromIndex: Optional[int] = None
    ) -> int:
        """Retorna o indice da ultima ocorrencia do caractere ou substring."""
        if isinstance(ch_or_str, JString):
            target = ch_or_str.value
        elif isinstance(ch_or_str, int):
            target = chr(ch_or_str)
        else:
            target = str(ch_or_str)

        if fromIndex is None:
            return self.value.rfind(target)

        # Se fromIndex < 0, Java não encontra nada (retorna -1)
        if fromIndex < 0:
            return -1

        # rfind(sub, start, end) procura dentro de s[start:end].
        # Para bater com o limite superior do Java, end = fromIndex + len(target)
        end_idx = min(len(self.value), fromIndex + len(target))
        return self.value.rfind(target, 0, end_idx)

    def contains(self, s: Any) -> bool:
        """Retorna true se a string contiver a sequencia de caracteres especificada."""
        if isinstance(s, JString):
            target = s.value
        elif hasattr(s, "toString"):
            target = s.toString()
        else:
            target = str(s)
        return target in self.value

    def startsWith(
        self, prefix: Union[str, 'JString'], toffset: int = 0
    ) -> bool:
        """Testa se a substring inicia com o prefixo dado."""
        target = (
            prefix.value if isinstance(prefix, JString) else str(prefix)
        )
        if toffset < 0 or toffset > len(self.value):
            return False
        return self.value.startswith(target, toffset)

    def endsWith(self, suffix: Union[str, 'JString']) -> bool:
        """Testa se esta string termina com o sufixo especificado."""
        target = suffix.value if isinstance(suffix, JString) else str(suffix)
        return self.value.endswith(target)
