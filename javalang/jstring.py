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
