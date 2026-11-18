# Registro da Preparação Inicial

## 1. Objetivo

Este documento registra as atividades realizadas na preparação do projeto de modernização do sistema legado de supermercado, antes de qualquer alteração funcional no código original.

Também apresenta a relação entre a preparação inicial e as etapas posteriores de desenvolvimento, permitindo acompanhar a evolução do projeto.

## 2. Código-base

- Projeto original: SupermarketReceipt-Refactoring-Kata
- Repositório de origem: https://github.com/emilybache/SupermarketReceipt-Refactoring-Kata
- Implementação selecionada: `python_pytest`
- Branch original: `main`
- Situação inicial: repositório original clonado localmente, com árvore de trabalho limpa.

## 3. Ambiente de desenvolvimento inicial

- Sistema operacional: Windows.
- Linguagem: Python.
- Gerenciador de pacotes: pip.
- Framework de testes: pytest 9.2.0.
- Ambiente virtual: `.venv`.

As dependências foram instaladas a partir do arquivo `requirements.txt` da implementação selecionada.

Durante o desenvolvimento, também foi utilizado um ambiente Ubuntu com Python 3.12.3 para executar os testes, realizar as alterações e registrar as evidências finais.

## 4. Organização inicial

Foram criadas as seguintes pastas:

- `docs/`: documentação técnica e registros do projeto.
- `evidencias/`: resultados de testes, ambiente e auditorias.
- `apresentacao/`: materiais para a apresentação final.

Também foram criados arquivos iniciais para diagnóstico, requisitos, plano de contingência, padrões de projeto, segurança e continuidade do trabalho.

## 5. Primeira execução dos testes

Comando executado:

```powershell
python -m pytest -v
```

Resultado observado:

- 1 teste coletado;
- 1 teste aprovado;
- nenhuma falha;
- tempo aproximado de execução: 0,10 segundo.

## 6. Interpretação do resultado

A execução confirmou que o ambiente inicial foi configurado corretamente e que o teste disponível no projeto original foi executado com sucesso.

Entretanto, apenas um teste aprovado não representava uma validação completa do sistema. Por isso, foi necessário compreender o código e desenvolver testes de caracterização para registrar o comportamento existente antes da refatoração.

## 7. Situação do código na preparação inicial

Na etapa registrada neste documento, nenhuma alteração funcional havia sido realizada no código original.

As atividades concluídas naquele momento foram a preparação do ambiente, a instalação das dependências, a organização inicial das pastas e a primeira execução dos testes.

## 8. Continuidade e evolução do projeto

Após a preparação inicial, o projeto avançou pelas seguintes etapas:

1. Análise dos arquivos principais, das responsabilidades e das dependências do sistema.
2. Elaboração do diagnóstico técnico e identificação de problemas de manutenção.
3. Definição dos requisitos funcionais, não funcionais e regras de negócio.
4. Elaboração do plano de contingência.
5. Criação de testes de caracterização para preservar o comportamento legado.
6. Execução e documentação das auditorias iniciais de segurança.
7. Refatoração das promoções utilizando os padrões Strategy e Factory Method.
8. Implementação da promoção de combos com desconto de 10% e regra de exclusividade por unidade.
9. Criação de testes automatizados para validar as funcionalidades originais e as novas regras.
10. Execução das auditorias finais e comparação dos resultados.
11. Atualização da documentação técnica e das evidências do projeto.

Ao final da implementação, a suíte automatizada passou a contar com 59 testes aprovados, abrangendo os comportamentos caracterizados e as novas funcionalidades.

Os resultados detalhados das etapas estão registrados nos documentos técnicos e nos arquivos da pasta `evidencias/`.