# Evidências de Testes — Antes e Depois da Modernização

**Projeto:** Supermarket Receipt – Modernização de Software
**Disciplina:** Alta Qualidade de Software
**Branch de referência:** `fix/dependency-hygiene`

Este documento compara a suíte de testes da linha de base (código original) com a suíte final, registra a cobertura e descreve como reproduzir as execuções.

---

## 1. Comparativo antes e depois

| Item | Antes (linha de base) | Depois (final) |
|---|---|---|
| Testes coletados | 1 | 61 |
| Testes aprovados | 1 | 61 |
| Falhas | 0 | 0 |
| Arquivo de evidência | `evidencias/testes_originais.txt` | `evidencias/testes_final.txt` |
| Sistema e Python registrados | Windows, Python 3.15.1 | Windows, Python 3.14.7 |
| pytest | 9.2.0 | 9.2.0 |
| Teste cobrindo combos | nenhum | 14 |
| Teste cobrindo a fábrica de promoções | nenhum | 1 |

Os ambientes das duas execuções não foram idênticos (versão do Python e pasta de trabalho diferentes). A comparação mostra a evolução da suíte, e não uma medição sob condições idênticas.

## 2. Composição da suíte final (61 testes)

| Arquivo | Testes | Objetivo |
|---|---:|---|
| `tests/test_supermarket.py` | 1 | Teste original do repositório-base (`test_ten_percent_discount`). |
| `tests/test_legacy_behavior.py` | 45 | Testes de caracterização do comportamento legado. |
| `tests/test_bundle_discount.py` | 14 | Promoção de combos: casos normais, de borda e validação. |
| `tests/test_promotion_factory.py` | 1 | Rejeição de tipos de promoção não suportados pela fábrica. |

### 2.1. Testes de caracterização (`test_legacy_behavior.py`)

| Classe de teste | Testes | O que protege |
|---|---:|---|
| `TestCarrinhoSemOfertas` | 9 | Carrinho vazio, itens unitários e por peso, acumulação de quantidades. |
| `TestDezPorCento` | 4 | Desconto percentual sobre toda a quantidade. |
| `TestLeveTresPagueDois` | 8 | Limite abaixo de 3 unidades, múltiplos de 3, resto e quantidades fracionárias (comportamento peculiar do legado registrado como `quirk`). |
| `TestDoisPorValor` | 5 | Duas unidades por valor fixo, grupos e resto; inclui os casos de 3 e 5 itens que usam divisão decimal no legado (`quirk`). |
| `TestCincoPorValor` | 5 | Cinco unidades por valor fixo e unidades excedentes. |
| `TestInteracaoEntreOfertas` | 5 | Ofertas diferentes em produtos diferentes, ordem dos descontos, substituição de oferta no mesmo produto e oferta sem produto no carrinho. |
| `TestReciboImpresso` | 5 | Formato e valores exibidos no recibo. |
| `TestContratoPublico` | 4 | Contrato público: cópias de itens e descontos do recibo, sinal negativo dos descontos, tipos de oferta existentes e chamada de `handle_offers`. |

### 2.2. Testes dos combos (`test_bundle_discount.py`)

| Cenário | Teste |
|---|---|
| Combo completo | `test_aplica_desconto_em_um_combo_completo` |
| Múltiplos combos | `test_aplica_desconto_em_dois_combos_completos` |
| Combo incompleto | `test_nao_aplica_desconto_em_combo_incompleto` |
| Unidades excedentes | `test_unidades_excedentes_continuam_elegiveis_a_promocao_individual` |
| Produtos por peso | `test_produtos_vendidos_por_peso_nao_participam_de_combos` |
| Percentuais inválidos (-10, 0, 101, `True`, texto `"10"`, `None`) | `test_rejeita_percentuais_de_desconto_invalidos[...]` (6 casos) |
| Produto repetido no combo | `test_combo_com_produto_repetido_exige_quantidade_correta` |
| Combos diferentes na mesma compra | `test_aplica_dois_combos_diferentes_na_mesma_compra` |
| Combo sem produtos | `test_nao_aplica_desconto_em_combo_sem_produtos` |

## 3. Preservação do comportamento legado

Os testes de caracterização e o teste original (46 no total) validam o comportamento do sistema original e do refatorado. Para reproduzir a verificação sobre o código original:

1. Crie uma cópia de trabalho da branch final.
2. Substitua a pasta `src/` pela da branch `main`, que contém o código original sem alterações.
3. Remova `tests/test_bundle_discount.py` e `tests/test_promotion_factory.py`, pois dependem da nova estrutura.
4. Execute `python -m pytest -v`.

Resultado esperado: os 46 testes aprovados. Em seguida, execute a suíte completa na branch final (61 aprovados). Se os mesmos 46 testes passam nos dois códigos, as regras de preço, desconto e recibo cobertas por eles não foram alteradas pela refatoração.

Limite desta evidência: ela vale apenas para os cenários cobertos pelos testes.

## 4. Cobertura

Arquivo: `evidencias/cobertura_final.txt` (cobertura de linhas e ramos, escopo `src`).

| Métrica | Resultado |
|---|---|
| Comandos em `src` | 213 |
| Comandos sem cobertura | 3 |
| Ramos de decisão | 40 |
| Ramos parcialmente cobertos | 0 |
| Cobertura total | 99% |

Arquivos abaixo de 100%:

| Arquivo | Cobertura | Linhas sem cobertura | Motivo |
|---|---:|---|---|
| `src/catalog.py` | 60% | 5, 8 | `raise` das operações que simulam acesso a banco de dados; os testes usam um catálogo falso. |
| `src/promotions/promotion_strategy.py` | 80% | 12 | Corpo do método abstrato da interface. |

Arquivo complementar: `evidencias/cobertura_testes.txt` (somente linhas, incluindo os arquivos de teste: 636 comandos, 3 sem cobertura, 99%).

Limitação: cobertura alta indica que o código foi executado pelos testes, mas não prova que as verificações estejam corretas ou completas.

## 5. Como reproduzir

Com o ambiente virtual do projeto ativado e as dependências instaladas (`python -m pip install -r requirements.txt`):

```bash
python -m pytest -v
python -m coverage run --branch --source=src -m pytest
python -m coverage report -m
```

## 6. Rastreabilidade

| Regra | Testes | Evidência |
|---|---|---|
| Preservação das promoções existentes | `test_legacy_behavior.py` | `evidencias/testes_final.txt` |
| Recibo e contrato público inalterados | `TestReciboImpresso`, `TestContratoPublico` | `evidencias/testes_final.txt` |
| Combos com 10% apenas em conjuntos completos | `test_bundle_discount.py` | `evidencias/testes_final.txt` |
| Exclusividade por unidade e excedentes | `test_unidades_excedentes_continuam_elegiveis_a_promocao_individual`, `TestInteracaoEntreOfertas` | `evidencias/testes_final.txt` |
| Seleção de estratégias pela fábrica | `test_promotion_factory.py` | `evidencias/testes_final.txt` |
