# Supermarket Receipt – Modernização de Software

Projeto acadêmico da disciplina Alta Qualidade de Software.

O objetivo é analisar, testar e refatorar um sistema legado de checkout de supermercado, aplicando boas práticas de engenharia de software, padrões de projeto, testes automatizados e análise de segurança.

## Situação atual

**Etapa de preparação e diagnóstico inicial concluída.**

Até o momento, foram realizados:
- Configuração do ambiente Python e instalação das dependências originais.
- Execução dos testes originais: 1 teste aprovado.
- Análise técnica do código legado.
- Levantamento dos requisitos funcionais e não funcionais.
- Definição inicial dos padrões de projeto a aplicar.
- Elaboração do plano de contingência.
- Execução das análises iniciais de segurança com Bandit, pip-audit e Safety.
- Organização das evidências e documentação.

A refatoração e a implementação da promoção de combos ainda estão pendentes.

## Estrutura do projeto

- `src/`: código-fonte original do sistema.
- `tests/`: testes automatizados.
- `docs/`: diagnóstico, requisitos, padrões, contingência e segurança.
- `evidencias/`: registros das execuções e análises.
- `apresentacao/`: materiais da apresentação.
- `GUIA_CONTINUIDADE.md`: orientações para continuidade do trabalho.

## Como executar

Crie e ative um ambiente virtual:

```bash
python -m venv .venv
```

No Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Instale as dependências:

```powershell
python -m pip install -r requirements.txt
```

Execute os testes:

```powershell
python -m pytest -v
```

## Próximas atividades

1. Criar testes de caracterização para registrar o comportamento atual.
2. Refatorar gradualmente o código legado.
3. Aplicar pelo menos dois padrões de projeto, com justificativa documentada.
4. Implementar a promoção de combos com desconto de 10% nos itens pertencentes a combinações completas.
5. Garantir a coexistência correta das promoções existentes.
6. Ampliar os testes de regressão.
7. Corrigir e reavaliar os problemas de segurança encontrados.
8. Atualizar a documentação e preparar a apresentação.

## Organização do desenvolvimento

As alterações devem ser feitas em branches específicas, evitando trabalhar diretamente na `main`.

Antes de integrar alterações:
- Executar os testes.
- Conferir o funcionamento do sistema.
- Revisar o código.
- Abrir um Pull Request para a `main`.

Consulte `GUIA_CONTINUIDADE.md` para as orientações detalhadas.