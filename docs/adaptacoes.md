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

---

## 6. Implementação de Operações Bit a Bit (Issue #10)
* **Conformidade:** Implementados todos os 10 métodos conforme a API estática do Java `java.lang.Integer`.
* **Tratamento de bits:** Dada a natureza de precisão arbitrária do `int` em Python, todos os métodos utilizam a máscara `& 0xFFFFFFFF` para emular o registo de 32 bits da JVM.
* **Complemento de Dois:** Criado o método auxiliar `_to_signed_32` para garantir que o bit de sinal seja preservado em operações de rotação e inversão, mantendo a paridade com o comportamento de números negativos do Java.

---

## 7. Métodos de Aritmética Estática
* **Conformidade:** Implementados `sum`, `max` e `min` conforme a API do Java SE 8.
* **Overflow de 32 bits:** No método `sum`, devido à precisão arbitrária do Python, utilizou-se o método auxiliar `_to_signed_32` para forçar o comportamento de *overflow* cíclico do complemento de dois (ex: somar 1 ao valor máximo de 32 bits resulta no valor mínimo negativo), replicando fielmente o comportamento da JVM.

---

## 8. Comparações e Aritmética Sem Sinal (Unsigned Operations)
* **Conformidade:** Implementados `compare`, `compareUnsigned`, `divideUnsigned` e `remainderUnsigned` conforme Java SE 8.
* **Mapeamento de Exceções:** Alterada a interceção de divisão por zero de `ValueError` para `ZeroDivisionError`, alinhando o comportamento com a `ArithmeticException` do Java de forma idiomática em Python.
* **Semântica Unsigned:** Utilizou-se a máscara `& 0xFFFFFFFF` para converter números negativos em suas representações equivalentes de magnitude unsigned de 32 bits (ex: `-1` interpretado como `4294967295`), garantindo que divisões, restos e comparações operem sob a especificação correta da JVM.

---

## 9. Construtores do Ciclo de Vida (JString)
* **Simulação de Sobrecarga:** Como o Python não possui sobrecarga nativa de métodos por assinatura de tipo, unificou-se os 9 construtores do Java SE 8 num único inicializador `__init__`, fazendo a distinção em tempo de execução (*runtime*) via `isinstance` e análise de assinaturas posicionais opcionais (`arg2`, `arg3`).
* **Tratamento de Exceções e Paridade de Tipos:** * A exceção Java `IndexOutOfBoundsException` foi traduzida de forma idiomática para `IndexError` no fatiamento de arrays.
  * A `UnsupportedEncodingException` do Java dispara um `ValueError` quando o Python não reconhece o nome do charset fornecido.
* **Resiliência a Bytes Corrompidos:** Diferente do comportamento do Python que lança um `UnicodeDecodeError`, o método foi configurado com `errors="replace"` para espelhar a especificação do Java, que substitui silenciosamente sequências malformadas pelo caractere padrão de substituição do Unicode (`\uFFFD`).

---

## 10. Métodos de Acesso e Tamanho - Parte 1 (JString)
* **Controlo de Fronteiras de Índices (`charAt`):** O Python suporta nativamente indexação negativa (ex: `-1` acede ao último elemento). Para garantir a paridade estrita com o comportamento do Java SE 8, que lança `IndexOutOfBoundsException` para qualquer valor fora do intervalo contido entre `0` e `length() - 1`, foi embutida uma validação explícita antes do fatiamento, convertendo o erro para `IndexError`.
* **Exportação Polimórfica de Bytes:** Unificou-se as duas assinaturas de `getBytes()` através de um argumento opcional padronizado como `None`. O método intercepta o `LookupError` do interpretador Python caso o utilizador passe um identificador de *charset* inválido, encapsulando-o num `ValueError` com o rótulo da exceção original (`UnsupportedEncodingException`).

---

## 11. Métodos de Acesso e Tamanho - Parte 2 (JString)
* **Equivalência de UTF-16 para UTF-8 Nativo (Code Points):** Em Java, strings internas usam codificação UTF-16, onde caracteres suplementares (como Emojis) ocupam dois *chars* (surrogate pairs). No Python, strings nativas são armazenadas usando uma estratégia dinâmica (PEP 393) onde cada elemento do fatiamento já representa um Code Point completo e isolado. Por conseguinte, os métodos `codePointAt`, `codePointBefore` e `codePointCount` puderam ser mapeados de forma simplificada através da função nativa `ord()`, mantendo a paridade de retornos numéricos dos pontos de código sem a necessidade de processar pares substitutos manualmente.
* **Mutação de Parâmetros Externos (`getChars`):** O método `getChars` quebra o paradigma de imutabilidade geral da classe ao alterar diretamente o estado de uma lista passada como argumento (`dst`). Isso foi implementado via fatiamento destrutivo *in-place* (`dst[begin:end] = ...`), mantendo a compatibilidade com a assinatura por referência do Java.