# Análise de Segurança — Antes e Depois da Modernização

## 1. Objetivo

Avaliar aspectos da segurança do sistema legado antes e depois da modernização, utilizando ferramentas de análise estática do código e verificação de vulnerabilidades conhecidas nas dependências Python.

A análise busca identificar possíveis problemas, comparar os resultados das execuções e registrar os riscos que permaneceram.

## 2. Ferramentas utilizadas

Foram utilizadas três ferramentas complementares:

- **Bandit:** identifica padrões potencialmente inseguros no código Python por meio de análise estática.
- **pip-audit:** verifica vulnerabilidades conhecidas nas dependências Python declaradas.
- **Safety:** identifica alertas de segurança relacionados às dependências e aplica políticas de classificação e ignorar alertas.

Cada ferramenta possui um escopo específico. Portanto, seus resultados devem ser interpretados separadamente.

## 3. Análise inicial — Antes da modernização

A análise inicial foi realizada sobre a versão original do projeto.

### 3.1 Bandit

Resultado registrado:

- Linhas de código analisadas: 133.
- Problemas identificados: 0.
- Arquivos ignorados: 0.

A ferramenta não identificou problemas de segurança no código analisado.

### 3.2 pip-audit

Resultado registrado:

**No known vulnerabilities found.**

Isso significa que a ferramenta não encontrou vulnerabilidades conhecidas nas dependências verificadas naquela execução.

### 3.3 Safety

O relatório inicial identificou 14 alertas, todos ignorados pelas políticas aplicadas.

Os registros estavam relacionados a:

- **pytest:** um alerta associado à especificação sem versão fixada, classificado pela política `unpinned-specification`.
- **filelock:** 13 alertas associados à versão 3.32.7, classificados pela política `environment-dependency`.

Os alertas ignorados permaneceram registrados no relatório, não significando que foram corrigidos ou eliminados.

## 4. Análise final — Depois da modernização

Após a refatoração e a implementação dos descontos por combos, as três ferramentas foram executadas novamente.

### 4.1 Bandit

Resultado registrado:

- Linhas de código analisadas: 291.
- Problemas identificados: 0.
- Arquivos ignorados: 0.

A ferramenta não identificou problemas de segurança no código analisado.

### 4.2 pip-audit

Resultado registrado:

**No known vulnerabilities found.**

Não foram encontradas vulnerabilidades conhecidas nas dependências declaradas em `requirements.txt`.

### 4.3 Safety

O relatório final registrou:

- Dependências testadas: 80.
- Alertas encontrados: 14.
- Alertas ignorados pelas políticas: 14.
- Alertas não ignorados: 0.
- Correções sugeridas: 0.

Os alertas estavam relacionados aos mesmos pacotes identificados na análise inicial:

- **pytest:** um alerta associado à especificação sem versão fixada (`unpinned-specification`).
- **filelock:** 13 alertas associados à versão 3.32.7 (`environment-dependency`).

Os mesmos identificadores de alertas foram encontrados nos relatórios inicial e final.

## 5. Comparação dos resultados

| Ferramenta | Antes | Depois |
|---|---|---|
| Bandit | 133 linhas; 0 problemas | 291 linhas; 0 problemas |
| pip-audit | Nenhuma vulnerabilidade conhecida encontrada | Nenhuma vulnerabilidade conhecida encontrada |
| Safety | 14 alertas, todos ignorados | 14 alertas, todos ignorados |

### 5.1 Comparação do Bandit

O volume de código analisado aumentou de 133 para 291 linhas. Mesmo com o crescimento do código decorrente da modernização, a ferramenta continuou sem identificar problemas.

Esse resultado indica que não foram introduzidos padrões inseguros detectáveis pelo Bandit dentro do escopo analisado.

### 5.2 Comparação do pip-audit

A ferramenta apresentou o mesmo resultado antes e depois: nenhuma vulnerabilidade conhecida encontrada nas dependências verificadas.

Isso representa um resultado positivo para o conjunto de dependências declarado no arquivo `requirements.txt`.

### 5.3 Comparação do Safety

O Safety identificou 14 alertas nos dois momentos, todos ignorados pelas políticas padrão.

Não houve redução no número de alertas registrados. Também não foram sugeridas correções na análise final.

É importante destacar que um alerta ignorado não significa que a vulnerabilidade foi corrigida. Significa que ele foi classificado como ignorado conforme a política aplicada.

## 6. Interpretação dos alertas do Safety

### 6.1 Alerta relacionado ao pytest

O alerta `SFTY-20260122-20373` está associado à ausência de uma versão fixada na especificação da dependência.

A classificação `unpinned-specification` indica que a dependência não possui uma versão explicitamente fixada naquela especificação analisada.

Fixar versões contribui para a reprodutibilidade do ambiente, pois reduz diferenças entre instalações realizadas em momentos distintos.

### 6.2 Alertas relacionados ao filelock

Foram registrados 13 alertas associados à versão `filelock==3.32.7`.

A classificação `environment-dependency` indica que o pacote foi identificado como dependência do ambiente analisado, e não como dependência diretamente declarada no arquivo `requirements.txt`.

Por esse motivo, os alertas foram ignorados pela política padrão correspondente.

## 7. Limitações da comparação

Os resultados devem ser interpretados considerando algumas limitações:

- O relatório inicial do Safety foi gerado em um clone do projeto no Windows.
- O relatório final foi gerado no Ubuntu, utilizando a branch `test/security-audits`.
- Os ambientes de execução não eram rigorosamente idênticos.
- A instalação do Safety no ambiente virtual alterou dependências desse ambiente, incluindo o pacote `filelock`.
- O Bandit analisou o diretório `src`.
- O pip-audit verificou as dependências declaradas em `requirements.txt`.
- O Safety também identificou dependências presentes no ambiente virtual.

Assim, a comparação representa os resultados registrados em cada execução, mas não uma avaliação experimental realizada em ambientes completamente controlados e idênticos.

Além disso, nenhuma dessas ferramentas, isoladamente, garante que o sistema esteja livre de todas as vulnerabilidades.

## 8. Conclusão

As auditorias realizadas permitiram avaliar diferentes aspectos da segurança do projeto antes e depois da modernização.

O Bandit não identificou problemas nas duas execuções, mesmo com o aumento do código analisado. O pip-audit também apresentou resultados positivos nos dois momentos, sem encontrar vulnerabilidades conhecidas nas dependências declaradas.

O Safety manteve 14 alertas nos dois relatórios, todos classificados como ignorados pelas políticas padrão. Portanto, esses alertas foram documentados, mas não devem ser considerados corrigidos.

De maneira geral, os resultados indicam que a modernização não introduziu problemas detectáveis pelas ferramentas utilizadas dentro dos respectivos escopos analisados. A documentação dos resultados e de suas limitações permite manter a transparência e facilita futuras verificações de segurança.

## 9. Evidências

Os resultados completos das auditorias estão disponíveis no diretório `evidencias/`:

- `bandit_antes.txt`
- `bandit_depois.txt`
- `pip_audit_antes.txt`
- `pip_audit_depois.txt`
- `safety_antes.json`
- `safety_depois.json`

As evidências finais foram registradas no GitHub e integradas à branch `develop` por meio do Pull Request #2.