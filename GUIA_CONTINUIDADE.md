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

O projeto conta com 59 testes automatizados aprovados na validação registrada:

- 46 testes relacionados ao comportamento legado e à caracterização.
- 13 testes relacionados à implementação dos combos.

Comando utilizado:

```bash
python -m pytest -v
```

Os testes verificam o comportamento original, as promoções existentes e as novas regras de formação e aplicação dos combos.

Antes de novas alterações, a suíte completa deverá ser executada novamente.

## 6. Auditorias de segurança

Foram utilizadas três ferramentas:

- **Bandit:** análise estática de possíveis problemas de segurança no código Python.
- **pip-audit:** identificação de vulnerabilidades conhecidas nas dependências analisadas.
- **Safety:** verificação de alertas relacionados a dependências e políticas de segurança.

Resultados registrados:

| Ferramenta | Resultado final |
|---|---|
| Bandit | 0 problemas identificados |
| pip-audit | Nenhuma vulnerabilidade conhecida encontrada nas dependências analisadas |
| Safety | 14 alertas encontrados, todos ignorados por políticas de classificação |

Os alertas do Safety não devem ser interpretados como vulnerabilidades corrigidas. Eles foram identificados e classificados como ignorados pelas políticas aplicadas.

Os ambientes utilizados nas análises inicial e final não eram idênticos. Essa limitação está detalhada em `docs/seguranca_antes_depois.md`.

As evidências estão armazenadas na pasta `evidencias/`.

## 7. Estrutura do projeto

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
│
├── README.md
├── GUIA_CONTINUIDADE.md
└── requirements.txt
```

## 8. Como executar o projeto

Com o ambiente virtual ativado e as dependências instaladas, execute os testes:

```bash
python -m pytest -v
```

Para executar o sistema, utilize o fluxo de execução disponibilizado pelo projeto original e consulte o README para orientações adicionais.

## 9. Organização do Git

O fluxo de branches utilizado pelo grupo é:

- `main`: branch principal, destinada à versão estável.
- `develop`: branch de integração das funcionalidades.
- `feature/*`: branches destinadas ao desenvolvimento de funcionalidades específicas.
- `docs/*`: branches destinadas a alterações de documentação.

As alterações devem ser desenvolvidas em branches próprias e integradas por meio de Pull Requests, após revisão e validação.

Os commits devem utilizar mensagens claras e seguir o padrão Conventional Commits, por exemplo:

```text
feat: adiciona nova funcionalidade
fix: corrige regra de negócio
test: adiciona testes automatizados
docs: atualiza documentação
refactor: reorganiza implementação
```

## 10. Orientações para continuidade

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

## 11. Situação e atividades de finalização

A implementação principal, a documentação técnica, os testes automatizados e as auditorias de segurança já foram realizados e registrados.

As atividades de finalização incluem:

- Revisar a documentação e as evidências.
- Executar e registrar a análise de cobertura dos testes.
- Conferir a integridade final do repositório.
- Integrar a documentação final à branch de desenvolvimento por Pull Request.
- Preparar a apresentação de 10 a 15 minutos.

A entrega deverá permitir que o grupo explique as decisões técnicas, os padrões utilizados, as regras de negócio, os testes e os resultados das análises de segurança.