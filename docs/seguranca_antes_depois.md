# Análise de Segurança — Antes e Depois

## 1. Objetivo

Avaliar a segurança do sistema legado antes e depois da modernização, identificando possíveis vulnerabilidades no código-fonte e nas dependências utilizadas.

## 2. Ferramentas utilizadas

| Ferramenta | Finalidade |
|---|---|
| Bandit | Identificar possíveis problemas de segurança no código Python. |
| pip-audit | Verificar vulnerabilidades conhecidas nas dependências Python. |
| Safety | Analisar dependências e identificar pacotes com problemas de segurança conhecidos. |

## 3. Análise inicial — Antes da modernização

A análise inicial será realizada sobre a versão original do sistema, antes das alterações estruturais e da implementação dos combos.

**Resultados:**

- Bandit: pendente de execução.
- pip-audit: pendente de execução.
- Safety: pendente de execução.

Os resultados completos serão armazenados na pasta `evidencias/`.

## 4. Análise final — Depois da modernização

Após a refatoração e a implementação das novas funcionalidades, as três ferramentas serão executadas novamente.

**Resultados:**

- Bandit: pendente de execução.
- pip-audit: pendente de execução.
- Safety: pendente de execução.

## 5. Comparação e conclusão

Os resultados das análises inicial e final serão comparados para identificar:

- Vulnerabilidades identificadas antes e depois.
- Problemas corrigidos durante a modernização.
- Dependências que precisam de atualização.
- Riscos que permaneceram e justificativas para sua manutenção.

A modernização deverá buscar reduzir os riscos identificados, sem comprometer o funcionamento do sistema.