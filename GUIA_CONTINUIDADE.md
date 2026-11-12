# GUIA DE CONTINUIDADE — MODERNIZAÇÃO DO SUPERMARKET RECEIPT

## 1. Objetivo do projeto

Modernizar incrementalmente o sistema legado Supermarket Receipt, utilizando boas práticas de Engenharia de Software, refatoração, padrões de projeto, testes automatizados e análise de segurança.

O objetivo não é reescrever o sistema do zero, mas compreender seu funcionamento original, preservar suas regras de negócio e melhorar sua estrutura de forma segura.

A implementação foi baseada no código original do repositório oficial, utilizando a versão Python com pytest (`python_pytest`).

Repositório do projeto:
https://github.com/Erichcao/supermarket-receipt-modernizacao-av3-altaqualidade

## 2. Requisitos e regras obrigatórias

As principais diretrizes da modernização foram:

1. Preservar o código e as regras de negócio originais.
2. Desenvolver testes de caracterização para registrar o comportamento anterior à refatoração.
3. Utilizar pytest para os testes automatizados.
4. Preservar as promoções existentes e seus contratos públicos.
5. Aplicar pelo menos dois padrões de projeto, justificando sua utilização.
6. Implementar a promoção de combos com desconto de 10%.
7. Impedir descontos duplicados sobre as mesmas unidades.
8. Executar Bandit, pip-audit e Safety antes e depois das alterações.
9. Registrar evidências reais de testes e auditorias.
10. Manter o projeto executável e documentado.

## 3. Funcionalidades implementadas

### 3.1. Promoções existentes

Foram preservadas as regras das promoções originais:

- Desconto percentual.
- Três unidades pelo preço de duas.
- Duas unidades por valor fixo.
- Cinco unidades por valor fixo.

A modernização buscou manter o comportamento legado protegido pelos testes de caracterização.

### 3.2. Promoção de combos

Foi implementada uma nova promoção que concede 10% de desconto sobre os produtos que formam um combo completo.

Regras implementadas:

- Cada oferta define os produtos e as quantidades necessárias para formar o combo.
- O desconto é aplicado somente quando todos os produtos e quantidades exigidos estão disponíveis.
- É possível formar múltiplos combos quando existem quantidades suficientes.
- Combos incompletos não recebem desconto.
- Uma mesma unidade não pode participar de mais de um combo.
- Unidades utilizadas nos combos não recebem simultaneamente promoções individuais incompatíveis.
- Produtos excedentes permanecem elegíveis às promoções individuais, respeitando suas regras originais.
- Produtos vendidos por peso não participam dos combos.
- Percentuais de desconto inválidos são rejeitados no cadastro das ofertas.

A política adotada é a **exclusividade por unidade**, evitando a acumulação indevida de descontos.

## 4. Padrões de projeto aplicados

Foram implementados dois padrões principais:

**Strategy**

Encapsula as regras de cálculo das promoções em estratégias independentes, permitindo organizar e testar cada tipo de oferta separadamente.

**Factory Method**

Centraliza a criação e a seleção das estratégias de promoção por meio da classe `PromotionFactory`.

Os padrões estão documentados em `docs/padroes_projeto.md`.

## 5. Testes automatizados

O projeto conta com 61 testes automatizados aprovados na validação registrada (execução com Python 3.14.7 e pytest 9.2.0):

- 46 testes relacionados ao comportamento legado: 45 de caracterização (`test_legacy_behavior.py`) e 1 teste original (`test_supermarket.py`).
- 14 testes da promoção de combos (`test_bundle_discount.py`).
- 1 teste da fábrica de promoções (`test_promotion_factory.py`).

Comando utilizado:

```bash
python -m pytest -v
```

Os testes verificam o comportamento original, as promoções existentes e as novas regras de formação e aplicação dos combos.

Antes de novas alterações, a suíte completa deverá ser executada novamente.

### 5.1. Cobertura

Comandos:

```powershell
python -m coverage run --branch --source=src -m pytest
python -m coverage report -m
```

Resultado da primeira execução (cobertura de linhas, incluindo os arquivos de teste no total): 99%. Considerando apenas `src`, são 213 comandos e 3 sem cobertura, aproximadamente 98,6%.

Arquivos de `src` abaixo de 100%:

| Arquivo | Cobertura | Linhas sem cobertura |
|---|---:|---|
| `src/catalog.py` | 60% | 5, 8 |
| `src/promotions/promotion_strategy.py` | 80% | 12 |

Essas linhas devem ser conferidas no código; a hipótese é que sejam corpos de métodos abstratos das interfaces, que não são executados diretamente. `shopping_cart.py`, `teller.py` e `bundle_discount.py` têm 100%.

Limitação: a primeira execução mediu apenas linhas, e não ramos de decisão. Cobertura alta não prova que os testes verifiquem o comportamento correto. A evidência final fica em `evidencias/cobertura_final.txt`.

## 6. Dependências e ambientes

### 6.1. Dependências do projeto

O `requirements.txt` passou a fixar versões exatas, para garantir reprodutibilidade:

```text
approvaltests==20.0.1
coverage==7.17.2
pytest==9.2.0
pytest-approvaltests==0.2.4
```

O `pytest==9.2.0` está acima da faixa indicada no alerta de segurança (`<9.0.3`).

### 6.2. Dois ambientes virtuais separados

- **`.venv` (dentro do repositório):** contém apenas as dependências do projeto. Não deve receber Bandit, pip-audit nem Safety. Não é enviado ao GitHub.
- **`auditoria-venv` (fora do repositório, em `C:\AV3-AQ\`):** contém as ferramentas de auditoria (Bandit, pip-audit e Safety).

A separação evita que dependências das ferramentas de segurança, como o `filelock` instalado junto com o Safety, entrem no ambiente do projeto e apareçam nos relatórios.

### 6.3. Comandos (Windows / PowerShell)

Ambiente do projeto:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pytest -v
```

Ambiente de auditoria:

```powershell
cd C:\AV3-AQ
python -m venv auditoria-venv
.\auditoria-venv\Scripts\Activate.ps1
python -m pip install --upgrade pip bandit pip-audit safety
cd supermarket-receipt-modernizacao-av3-altaqualidade
```

Se o PowerShell bloquear a ativação, execute uma vez:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

No Ubuntu, a ativação é `source .venv/bin/activate`.

## 7. Auditorias de segurança

Foram utilizadas três ferramentas:

- **Bandit:** análise estática de possíveis problemas de segurança no código Python.
- **pip-audit:** identificação de vulnerabilidades conhecidas nas dependências analisadas.
- **Safety:** verificação de alertas relacionados a dependências e políticas de segurança.

### 7.1. Resultados em três momentos

| Ferramenta | Inicial | Intermediário | Final |
|---|---|---|---|
| Bandit | 133 linhas, 0 problemas | não executado | 291 linhas, 0 problemas, 0 arquivos ignorados |
| pip-audit | Nenhuma vulnerabilidade conhecida | não executado | Nenhuma vulnerabilidade conhecida, com versões fixadas |
| Safety | 80 dependências, 14 alertas, 14 ignorados | 29 dependências, 1 alerta (`pip` 26.2.1), 1 ignorado | 29 dependências, 0 alertas, 0 correções sugeridas |

Nenhuma ferramenta apontou problemas no código-fonte (`src`). Os alertas do Safety estavam em dependências e no ambiente de desenvolvimento.

### 7.2. Tratamento dos alertas do Safety

| Alerta | Causa | Tratamento |
|---|---|---|
| `pytest` sem versão fixada (1 alerta, `unpinned-specification`) | `requirements.txt` sem versões | Versões fixadas; `pytest==9.2.0` |
| `filelock` (13 alertas, `environment-dependency`) | Instalado no `.venv` junto com o Safety; não faz parte do projeto | `.venv` recriado só com o `requirements.txt`; ferramentas movidas para `auditoria-venv` |
| `pip` 26.2.1 (1 alerta, `environment-dependency`) | `pip` abaixo da faixa corrigida (`<26.2.2`) | `pip` atualizado para a versão 26.3 |

A melhoria só foi afirmada após a nova execução do Safety, que reportou 0 alertas.

### 7.3. Limitações

- A queda de 80 para 29 dependências testadas decorre da mudança de escopo (as ferramentas de auditoria ficaram fora do ambiente do projeto), e não da remoção de pacotes do projeto.
- Os ambientes das execuções não foram idênticos: o relatório inicial foi gerado em outro clone no Windows, uma execução intermediária no Ubuntu e a final no Windows 11, com as ferramentas em Python 3.14.7.
- O `pip` não consta no `requirements.txt`; a atualização vale para o ambiente em que foi feita. Por isso a instalação deve começar com `python -m pip install --upgrade pip`.
- O resultado vale para a data e as versões registradas (Safety 3.8.1, execução de 12/11/2026).
- Alertas ignorados por política não significam corrigidos. Nenhum resultado deve ser descrito como vulnerabilidade corrigida sem uma nova execução que o confirme.

Detalhes em `docs/seguranca_antes_depois.md`.

## 8. Estrutura do projeto

A organização principal inclui:

```text
supermarket-receipt-modernizacao-av3-altaqualidade/
│
├── src/
│   ├── promotions/
│   ├── catalog.py
│   ├── model_objects.py
│   ├── receipt.py
│   ├── shopping_cart.py
│   └── teller.py
│
├── tests/
│   ├── test_supermarket.py
│   ├── test_legacy_behavior.py
│   ├── test_bundle_discount.py
│   ├── fake_catalog.py
│   └── receipt_printer.py
│
├── docs/
│   ├── diagnostico_tecnico.md
│   ├── requisitos.md
│   ├── plano_contingencia.md
│   ├── padroes_projeto.md
│   └── seguranca_antes_depois.md
│
├── evidencias/
│   ├── bandit_antes.txt / bandit_depois.txt / bandit_final.txt
│   ├── pip_audit_antes.txt / pip_audit_depois.txt / pip_audit_final.txt
│   ├── safety_antes.json / safety_depois.json
│   ├── safety_intermediario_pip_26.2.1.json
│   └── safety_final.json
│
├── README.md
├── GUIA_CONTINUIDADE.md
└── requirements.txt
```

## 9. Como executar o projeto

Com o ambiente virtual ativado e as dependências instaladas, execute os testes:

```powershell
python -m pytest -v
```

Para executar o sistema, utilize o fluxo de execução disponibilizado pelo projeto original e consulte o README para orientações adicionais.

## 10. Organização do Git

O fluxo de branches utilizado pelo grupo é:

- `main`: branch principal, destinada à versão estável.
- `develop`: branch de integração das funcionalidades.
- `feature/*`: branches destinadas ao desenvolvimento de funcionalidades específicas.
- `docs/*`: branches destinadas a alterações de documentação.
- `fix/*`: branches destinadas a correções, como a higiene de dependências (`fix/dependency-hygiene`).

As alterações devem ser desenvolvidas em branches próprias e integradas por meio de Pull Requests, após revisão e validação. Não há commits diretos na `main`.

Os commits seguem o padrão Conventional Commits, com descrições em português:

```text
feat: adiciona nova funcionalidade
fix: corrige regra de negócio
test: adiciona testes automatizados
docs: atualiza documentação
refactor: reorganiza implementação
chore: atualiza configuração do projeto
```

Último registro de segurança: commit `chore: fixa dependências e atualiza evidências de segurança`, na branch `fix/dependency-hygiene`, com Pull Request aberto para a `develop`. **Pendente:** revisão por outro integrante e merge.

## 11. Orientações para continuidade

Qualquer pessoa ou ferramenta de IA que dê continuidade ao projeto deverá:

1. Ler este guia e a documentação relacionada antes de propor alterações.
2. Inspecionar o código real antes de recomendar refatorações.
3. Não inventar nomes de classes, métodos, arquivos ou resultados de execução.
4. Não presumir que os testes passaram sem executar ou receber evidências.
5. Não modificar regras de negócio existentes sem justificativa.
6. Não implementar padrões de projeto artificialmente.
7. Explicar cada alteração, indicando os arquivos afetados e como testar.
8. Preferir mudanças pequenas, rastreáveis e reversíveis.
9. Atualizar a documentação e os testes junto com as alterações.
10. Sinalizar claramente o que ainda não foi realizado.
11. Não instalar ferramentas de auditoria no `.venv` do projeto.
12. Usar comandos compatíveis com o sistema do integrante (PowerShell no Windows, bash no Ubuntu).
13. Conferir, antes de commitar arquivos de evidência, se não contêm dados pessoais.

## 12. Checklist de conclusão

- [x] Repositório independente criado e publicado.
- [x] Testes de caracterização adicionados.
- [x] Padrões Strategy e Factory Method implementados e documentados.
- [x] Promoção de combos implementada, com testes específicos.
- [x] Bandit, pip-audit e Safety executados antes e depois.
- [x] Dependências fixadas no `requirements.txt`.
- [x] Ferramentas de auditoria isoladas em ambiente separado.
- [x] Evidências de segurança atualizadas.
- [x] `docs/seguranca_antes_depois.md` atualizado.
- [x] Commit e Pull Request de segurança criados.
- [ ] Revisão e merge do Pull Request de segurança na `develop`.
- [x] Análise de cobertura de testes executada.
- [ ] Evidência de cobertura (`evidencias/cobertura_final.txt`) commitada.
- [ ] Bandit executado novamente se o código de `src` mudar após a última auditoria.
- [ ] Revisão final da documentação e das evidências.
- [ ] README finalizado.
- [ ] Apresentação de 10 a 15 minutos preparada.
- [ ] Integração final validada em `develop` e `main`.

## 13. Situação e atividades de finalização

A implementação principal, a documentação técnica, os testes automatizados e as auditorias de segurança foram realizados e registrados.

Na etapa mais recente, os alertas do Safety foram tratados: versões fixadas, ambiente do projeto separado do ambiente de auditoria e `pip` atualizado. O Safety final testou 29 dependências e não reportou alertas; o Bandit analisou 291 linhas sem problemas; o pip-audit não encontrou vulnerabilidades conhecidas.

As atividades de finalização incluem:

- Obter a revisão e fazer o merge do Pull Request de segurança.
- Salvar e commitar a evidência de cobertura e de testes.
- Revisar a documentação e as evidências.
- Conferir a integridade final do repositório.
- Atualizar o README.
- Integrar a documentação final à branch de desenvolvimento por Pull Request.
- Preparar a apresentação de 10 a 15 minutos.

A entrega deverá permitir que o grupo explique as decisões técnicas, os padrões utilizados, as regras de negócio, os testes e os resultados das análises de segurança, incluindo as limitações de escopo e de ambiente.
