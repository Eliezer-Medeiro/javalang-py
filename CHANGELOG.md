# Changelog - javalang-py

Todas as alterações notáveis neste projeto serão documentadas neste ficheiro, seguindo o padrão [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) e Versionamento Semântico.

## [1.0.0] - v1.0.0 (Baseline Product) - 2026-06-21
### Added
- Classe `JString` concluída com os métodos estáticos (*Factories*).
- Integração da pipeline de automação completa com geração de artefato `coverage.xml`.
- Documentação final de Auditoria Interna (`auditoria.md`) e Relatório de Status (`status-v1.0.md`).

## [0.4.0] - v0.4-jstring (Baseline Allocated) - 2026-06-15
### Added
- Implementação da classe `JString` cobrindo Acesso, Comparação, Busca, Transformação e Expressões Regulares.
- Suíte de testes em `tests/test_jstring.py`, `test_jstring_transform.py` e `test_jstring_regex.py`.

## [0.3.0] - v0.3-jfloat (Baseline Allocated) - 2026-05-20
### Added
- Implementação da classe `JFloat` com suporte estrito a IEEE 754, NaNs e Infinitos.
- Testes de interoperabilidade binária e numérica com `JInteger`.

## [0.2.0] - v0.2-jinteger (Baseline Allocated) - 2026-04-15
### Added
- Implementação da classe `JInteger` (Wrappers, Parsing e Operações Bit-a-Bit).

## [0.1.0] - v0.1-functional (Baseline Functional) - 2026-03-10
### Added
- Setup inicial do repositório, configuração do CI com Ruff e proteção da branch `main`.
- Documentação inicial: Itens de Configuração e ADRs 0001, 0002 e 0003.