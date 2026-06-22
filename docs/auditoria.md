# Relatório de Auditoria Interna de Processo

Este documento valida o nível de conformidade do grupo com as regras estritas de Gerência de Configuração de Software (GCS) definidas no edital.

## 1. Verificação de Regras de Governança
* **Granularidade Fina (Anti-Atalho):** Auditado com sucesso. Nenhum commit na linha do tempo acumulou mais do que 3 métodos da API Java e nenhum Pull Request integrou mais do que 7 métodos de uma única vez.
* **Code Review Obrigatório:** Todas as integrações na branch `main` foram realizadas via Pull Requests que contaram com a aprovação de pelo menos um par da equipe com revisão assinada via painel do GitHub, impedindo o bypass das travas de ramificação.

## 2. Registro e Conciliação de Conflitos de Merge Provocados
Conforme exigido na especificação do trabalho, a equipe simulou cenários concorrentes de alteração para validar a capacidade de resolução de conflitos sem destruição de histórico.

* Conflito 1 (docs/adaptacoes.md): Alteração concorrente na mesma seção de histórico de engines de Regex por duas branches distintas.

* Conflito 2 (CHANGELOG.md): Inserção simultânea de notas de versão na mesma linha de cabeçalho da release final.

* Conflito 3 (docs/itens-de-configuracao.md): Edição concorrente na tabela de descrição dos ativos controlados.

*Evidência Física de Resolução Global de Conflitos de Mudança:* [Acesse o PR #46 no GitHub](https://github.com/Eliezer-Medeiro/javalang-py/pull/46)