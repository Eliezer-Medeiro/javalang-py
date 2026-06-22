# Identificação dos Itens de Configuração (IC)

Este documento identifica e estabelece o controle sobre os ativos de software cruciais do projeto `javalang-py`, conforme definido no ciclo de vida de GCS.

| Código IC | Nome do Item | Responsável (Papel) | Formato | Periodicidade de Mudança | Dependências |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **IC-01** | Módulo `JInteger` (`jinteger.py`) | Desenvolvedores | Código (.py) | Baixa (Consolidado) | IC-01 (Conversões) |
| **IC-02** | Módulo `JFloat` (`jfloat.py`) | Desenvolvedores | Código (.py) | Baixa (Consolidado) | IC-01 (Conversões) |
| **IC-03** | Módulo `JString` (`jstring.py`) | Desenvolvedores | Código (.py) | Alta (Sprints de String) | IC-01 (Conversões) |
| **IC-04** | Suítes de Testes (`tests/`) | Eng. de Qualidade | Código (.py) | Alta (A cada novo método) |  |
| **IC-05** | Configuração do Pipeline (`ci.yml`) | Eng. de Qualidade | Config (.yml) | Baixa (Apenas no Setup) | Ambiente GitHub Actions |
| **IC-06** | Diretrizes de Arquitetura (`adr/`) | Gerente de Config. | Texto (.md) | Baixa (Apenas decisões) | Nenhuma |
| **IC-07** | Matriz de Adaptações (`adaptacoes.md`)| Gerente de Config. | Texto (.md) | Média (A cada desvio) | Especificação Java SE 8 |
| **IC-08** | Relatórios de Status (`relatorios/`) | Relator | Texto (.md) | Por Baseline alcançada | Progresso dos Sprints |
<<<<<<< HEAD
IC controlado pela Branch B
=======
IC controlado pela Branch A
>>>>>>> branch-a
