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
* **Justificativa:** Em Java, a igualdade estrutural e as tabelas de dispersão dependem de `equals` e `hashCode`. Para que o `JInteger` funcione de forma transparente em estruturas de dados do Python (como chaves de dicionários `dict` ou elementos de conjuntos `set`), é obrigatório implementar o protocolo de hashing do Python através dos *dunder methods*,

