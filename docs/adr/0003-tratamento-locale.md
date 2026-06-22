# ADR 0003: Tratamento de Locale e Charsets Complexos

* **Status:** Approved
* **Contexto:** Métodos de formatação e codificação como `getBytes(String charset)` e transformações baseadas em regiões geográficas exigem uma infraestrutura pesada de internacionalização incompatível com o escopo ágil do projeto.
* **Decisão:** Conforme permissão explícita prevista no § 3 do edital do projeto, esses métodos complexos foram implementados como Stubs inteligentes que utilizam por padrão a codificação e localização nativa `UTF-8` estável do runtime do Python.
* **Consequências:** Código limpo e simplificado, documentando de forma consciente os limites da plataforma CPython adotada.