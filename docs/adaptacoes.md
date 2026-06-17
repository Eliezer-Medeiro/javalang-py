# Notas de Adaptação e Decisões de Design (Java vs. Python)

Este documento regista formalmente as decisões de engenharia de software adotadas na migração da classe `java.lang.Integer` (Java SE 8) para o ecossistema Python nativo na classe `JInteger`. 

---

## 1. Sobrecarga de Métodos (Method Overloading)

### parseInt e parseUnsignedInt
* **Especificação Java:** * `public static int parseInt(String s)`
  * `public static int parseInt(String s, int radix)`
  * `public static int parseUnsignedInt(String s)`
  * `public static int parseUnsignedInt(String s, int radix)`
* **Estratégia em Python:** Unificação num único método utilizando argumentos padrão/opcionais (`radix: int = 10`).
* **Justificativa:** O runtime do Python não suporta nativamente sobrecarga de métodos pelo número ou tipo de argumentos (o último método declarado sobrescreve os anteriores). A utilização de parâmetros padrão é a abordagem idiomática em Python para obter o mesmo comportamento funcional sem duplicar assinaturas ou forçar nomes artificiais (como `parseIntWithRadix`).

### valueOf
* **Especificação Java:**
  * `public static Integer valueOf(int i)`
  * `public static Integer valueOf(String s)`
  * `public static Integer valueOf(String s, int radix)`
* **Estratégia em Python:** Unificação num único método `valueOf(val, radix=10)` inspecionando o tipo dinâmico do argumento através de `isinstance(val, int)`.
* **Justificativa:** Como o Python possui tipagem dinâmica, um único argumento pode receber tanto `int` quanto `str`. A validação interna por tipo garante o comportamento de fábrica correto para ambos os casos, respeitando a filosofia Python de *"one way to do it"*.

---

## 2. Ciclo de Vida e Métodos de Objeto (Dunder Methods)

### hashCode e equals
* **Especificação Java:** `public int hashCode()` e `public boolean equals(Object obj)`
* **Estratégia em Python:** Mapeamento explícito dos métodos Java para os métodos mágicos nativos do Python (`__hash__` e `__eq__`).
* **Justificativa:** Em Java, a igualdade estrutural e as tabelas de dispersão dependem de `equals` e `hashCode`. Para que o `JInteger` funcione de forma transparente em estruturas de dados do Python (como chaves de dicionários `dict` ou elementos de conjuntos `set`), é obrigatório implementar o protocolo de hashing do Python através dos *dunder methods*, que por sua vez delegam a lógica para as assinaturas padrão Java.

---

## 3. Comportamento Específico de Parsing (decode)

### decode
* **Especificação Java:** `public static Integer decode(String nm)` (Suporta prefixos `0x`, `0X`, `#` para Hexadecimal e `0` para Octal).
* **Estratégia em Python:** Implementação de parsing manual com tratamento explícito de strings via `startswith`.
* **Justificativa:** A função nativa `int(nm, 0)` do Python falha ao tentar interpretar o caractere `#` (comum no Java para hexadecimais) e acusa erro em octais legados sem o prefixo moderno `0o` (como `'012'`). A lógica foi adaptada para intercetar estes prefixos manualmente antes de delegar para o conversor do Python, garantindo 100% de paridade com o comportamento do Java.

---

## 4. Formatação e Conversão de Bases (toString/toUnsignedString)
* **Especificação Java:** Múltiplos métodos `toXXXString` e sobrecarga de `toString`.
* **Estratégia em Python:** * Unificação de `toString` via argumento opcional `radix`.
    * Utilização de máscaras de bits (`i & 0xFFFFFFFF`) para simular o comportamento de 32 bits assinado do Java em `toBinaryString`, `toOctalString` e `toHexString`.
* **Justificativa:** O Python lida com inteiros de precisão arbitrária (tamanho infinito). Para replicar a formatação de 32 bits do Java (onde números negativos são representados em complemento de dois), a máscara `0xFFFFFFFF` é necessária para truncar o valor conforme o padrão esperado pela especificação Java SE 8.

---

## 5. Conflito de Nomes: toString (Instância vs. Estático)
* **Especificação Java:** * `public String toString()` (Instância)
    * `public static String toString(int i, int radix)` (Estático)
* **Conflito no Python:** A classe Python não permite a coexistência de dois métodos com o mesmo nome (`toString`), resultando em erro de redefinição (`F811`).
* **Decisão de Design:** Unificação do método através de *argumentos opcionais*. O método `toString` foi redefinido para aceitar parâmetros opcionais que permitem comportamentos distintos:
    1. `obj.toString()`: Retorna a string do valor da instância.
    2. `JInteger.toString(i, radix)`: Executa a conversão lógica baseada na especificação estática do Java.
* **Justificativa:** Esta abordagem preserva a integridade dos nomes exigidos pela especificação, evita a criação de métodos com nomes não oficiais e respeita a limitação técnica do interpretador Python, mantendo a compatibilidade funcional com o contrato Java original.
