# Supermarket Receipt – Modernização de Software

Projeto acadêmico desenvolvido para a disciplina de Alta Qualidade de Software.

O objetivo é modernizar gradualmente um sistema legado de checkout de supermercado, preservando seu comportamento original e aplicando boas práticas de engenharia de software, padrões de projeto, testes automatizados e auditorias de segurança.

## 1. Objetivos do projeto

- Analisar e documentar o funcionamento do sistema legado.
- Criar testes de caracterização para preservar o comportamento original.
- Refatorar o código de forma incremental.
- Aplicar padrões de projeto para melhorar a organização e a manutenção do sistema.
- Implementar uma nova funcionalidade de descontos por combos de produtos.
- Garantir a compatibilidade com as promoções existentes.
- Realizar testes de regressão e auditorias de segurança.

## 2. Funcionalidades implementadas

O sistema possui funcionalidades de checkout e aplicação de promoções, incluindo:

- Desconto percentual.
- Promoção de três produtos pelo preço de dois.
- Promoção de dois produtos por um valor determinado.
- Promoção de cinco produtos por um valor determinado.
- Desconto de 10% para combos completos de produtos.

### Regra dos descontos por combos

A implementação dos combos segue a política de exclusividade por unidade:

- Somente combinações completas recebem o desconto.
- Os produtos utilizados em um combo não recebem simultaneamente promoções individuais.
- Unidades excedentes continuam elegíveis às promoções individuais existentes.
- Uma mesma unidade não pode ser utilizada em mais de um combo.
- Produtos vendidos por peso não participam dos combos.

## 3. Padrões de projeto aplicados

Foram implementados dois padrões de projeto:

**Strategy**

Permite encapsular cada modalidade de promoção em uma estratégia independente, facilitando a manutenção e a inclusão de novas regras de desconto.

**Factory Method**

Centraliza a criação das estratégias de promoção, evitando que a lógica de seleção das promoções fique espalhada pelo sistema.

As implementações estão organizadas no diretório `src/promotions/`.

## 4. Testes automatizados

Foram desenvolvidos testes para preservar o comportamento legado e validar as novas funcionalidades.

Resultados registrados:

- 45 testes de caracterização, além do teste original.
- 13 testes específicos para os descontos por combos.
- 59 testes aprovados na execução completa da suíte.

Para executar os testes:

```bash
python -m pytest -v
```

## 5. Auditorias de segurança

Foram utilizadas três ferramentas para analisar diferentes aspectos do projeto:

**Bandit:** análise estática do código Python.

**pip-audit:** verificação de vulnerabilidades conhecidas nas dependências declaradas.

**Safety:** identificação de alertas de segurança relacionados às dependências e aplicação das políticas de análise.

Resultados finais registrados:

- Bandit: nenhum problema identificado na análise do diretório `src`.
- pip-audit: nenhuma vulnerabilidade conhecida encontrada nas dependências declaradas em `requirements.txt`.
- Safety: 14 alertas encontrados, todos ignorados pelas políticas padrão.

Os resultados anteriores e posteriores à modernização estão documentados em `docs/seguranca_antes_depois.md`, com as evidências originais disponíveis no diretório `evidencias/`.

**Observação:** alertas ignorados pelo Safety não devem ser considerados vulnerabilidades corrigidas. As limitações e diferenças entre os ambientes das execuções estão documentadas no comparativo de segurança.

## 6. Estrutura do projeto

```text
supermarket-receipt-modernizacao-av3-altaqualidade/
│
├── docs/
│   ├── diagnostico_tecnico.md
│   ├── requisitos.md
│   ├── plano_contingencia.md
│   ├── padroes_projeto.md
│   ├── seguranca_antes_depois.md
│   └── registro_preparacao.md
│
├── evidencias/
│   ├── ambiente_inicial.txt
│   ├── bandit_antes.txt
│   ├── bandit_depois.txt
│   ├── pip_audit_antes.txt
│   ├── pip_audit_depois.txt
│   ├── safety_antes.json
│   ├── safety_depois.json
│   └── testes_originais.txt
│
├── src/
│   ├── catalog.py
│   ├── model_objects.py
│   ├── receipt.py
│   ├── shopping_cart.py
│   ├── teller.py
│   └── promotions/
│
├── tests/
│   ├── test_supermarket.py
│   ├── test_legacy_behavior.py
│   ├── test_bundle_discount.py
│   ├── fake_catalog.py
│   └── receipt_printer.py
│
├── GUIA_CONTINUIDADE.md
├── README.md
├── README_ORIGINAL.md
├── requirements.txt
└── pytest.ini
```

## 7. Como configurar o ambiente

Clone o repositório:

```bash
git clone https://github.com/Erichcao/supermarket-receipt-modernizacao-av3-altaqualidade.git
```

Acesse a pasta:

```bash
cd supermarket-receipt-modernizacao-av3-altaqualidade
```

Crie um ambiente virtual:

```bash
python -m venv .venv
```

Ative o ambiente virtual.

No Linux:

```bash
source .venv/bin/activate
```

No Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Instale as dependências:

```bash
python -m pip install -r requirements.txt
```

## 8. Execução e validação

Para executar a suíte completa de testes:

```bash
python -m pytest -v
```

Para executar a análise de segurança com Bandit:

```bash
bandit -r src
```

Para verificar as dependências declaradas:

```bash
python -m pip_audit -r requirements.txt
```

Para executar o Safety:

```bash
python -m safety scan
```

Os resultados das auditorias e os registros das execuções estão disponíveis no diretório `evidencias/`.

## 9. Organização do desenvolvimento

O desenvolvimento utiliza branches específicas para separar as atividades e facilitar a integração.

A branch `main` é mantida como referência estável, enquanto `develop` funciona como branch de integração.

As alterações são realizadas em branches de trabalho e integradas à `develop` por meio de Pull Requests, após revisão e validação.

## 10. Documentação complementar

Os detalhes técnicos e os registros do projeto estão organizados nos seguintes documentos:

- `docs/diagnostico_tecnico.md`: análise do sistema legado.
- `docs/requisitos.md`: requisitos funcionais e não funcionais.
- `docs/plano_contingencia.md`: planejamento de contingência.
- `docs/padroes_projeto.md`: justificativa e aplicação dos padrões de projeto.
- `docs/seguranca_antes_depois.md`: comparação das auditorias de segurança.
- `GUIA_CONTINUIDADE.md`: orientações para continuidade do desenvolvimento.

## 11. Situação do projeto

A caracterização do comportamento legado, a refatoração, a implementação dos descontos por combos, os testes de regressão e as auditorias de segurança foram concluídos.

O projeto encontra-se na etapa de revisão da documentação, análise de cobertura dos testes, organização das evidências e preparação da apresentação final.

---

**Projeto acadêmico — Alta Qualidade de Software**