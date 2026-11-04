# Diagnóstico Técnico — Sistema Legado de Supermercado

## 1. Visão geral do sistema

O projeto implementa um sistema simplificado de caixa de supermercado. Sua responsabilidade é registrar produtos e quantidades, consultar preços, aplicar ofertas promocionais, calcular o valor final da compra e disponibilizar os dados necessários para a geração de um recibo.

A implementação analisada está organizada em Python, com separação entre modelos, carrinho de compras, caixa, catálogo e recibo.

## 2. Estrutura e responsabilidades identificadas

### `catalog.py`

Define a classe `SupermarketCatalog`, responsável pelas operações de cadastro e consulta de preços.

Os métodos `add_product()` e `unit_price()` possuem implementações que lançam exceções indicando que acessariam o banco de dados. Nos testes, essa dependência é substituída pela implementação `FakeCatalog`.

### `model_objects.py`

Contém as estruturas utilizadas pelo sistema:

- `Product`: representa um produto e sua unidade.
- `ProductQuantity`: associa um produto à quantidade.
- `ProductUnit`: define as unidades disponíveis, como unidade e quilo.
- `SpecialOfferType`: define os tipos de promoção.
- `Offer`: representa uma oferta.
- `Discount`: representa um desconto aplicado.

### `shopping_cart.py`

A classe `ShoppingCart` armazena os produtos e suas quantidades.

O método `add_item_quantity()` registra os itens e acumula as quantidades de cada produto.

O método `handle_offers()` concentra a lógica de aplicação das promoções. Ele consulta as ofertas, identifica seus tipos e calcula os descontos correspondentes.

### `teller.py`

A classe `Teller` coordena o processo de fechamento da compra.

O método `checks_out_articles_from()` percorre os produtos do carrinho, consulta os preços no catálogo, adiciona os itens ao recibo e solicita ao carrinho que processe as ofertas.

### `receipt.py`

Contém as classes `ReceiptItem` e `Receipt`.

A classe `Receipt` armazena os itens e descontos da compra e calcula o valor final somando os preços dos produtos e os valores dos descontos.

### `receipt_printer.py`

A classe `ReceiptPrinter` é responsável por formatar os dados do recibo, incluindo produtos, quantidades, descontos e total.

## 3. Fluxo geral de execução

O fluxo observado no código é:

1. O catálogo disponibiliza os preços dos produtos.
2. O `Teller` recebe o carrinho.
3. O caixa percorre os produtos e consulta seus preços.
4. Os produtos são adicionados ao recibo.
5. O método `handle_offers()` do carrinho verifica as ofertas cadastradas.
6. Os descontos identificados são adicionados ao recibo.
7. O recibo calcula o total da compra.
8. O `ReceiptPrinter` pode formatar os dados para apresentação.

## 4. Problemas e pontos de atenção identificados

### 4.1. Concentração da lógica de promoções

Arquivo: `src/shopping_cart.py`

Método: `handle_offers()`

O método reúne a verificação de diferentes tipos de promoção e o cálculo de seus respectivos descontos.

Isso concentra diferentes regras de negócio em um único método, tornando sua manutenção e expansão mais difíceis.

A inclusão de uma nova promoção, como os combos exigidos na atividade, poderá aumentar ainda mais a quantidade de condições e a complexidade desse método.

### 4.2. Uso de várias condições para selecionar promoções

Arquivo: `src/shopping_cart.py`

O método `handle_offers()` utiliza várias verificações condicionais para tratar os tipos de oferta.

Esse formato pode dificultar a extensão do sistema quando novas políticas de desconto forem adicionadas.

É necessário avaliar uma estrutura que permita separar as regras de cada promoção.

### 4.3. Dependência do carrinho em relação às regras de desconto

Arquivo: `src/shopping_cart.py`

O carrinho importa `SpecialOfferType` e `Discount` e conhece diretamente os tipos de promoção existentes.

Isso aumenta o conhecimento que a classe precisa ter sobre as regras comerciais do sistema.

A refatoração deve avaliar uma separação mais clara entre o armazenamento dos produtos e a aplicação das políticas de desconto.

### 4.4. Cobertura de testes limitada

Arquivo: `tests/test_supermarket.py`

Foi identificado apenas um teste automatizado no arquivo analisado.

O teste configura uma oferta de 10% para escovas, mas adiciona maçãs ao carrinho. Portanto, ele valida que a oferta não afeta um produto diferente, mas não comprova o funcionamento efetivo do desconto.

Ainda precisam ser testados os demais tipos de promoção, os cálculos, os recibos e os diferentes cenários de compra.

### 4.5. Dependência de catálogo substituída nos testes

Arquivos: `src/catalog.py` e `tests/fake_catalog.py`

A classe `SupermarketCatalog` indica que suas operações acessariam um banco de dados e lança exceções quando chamadas diretamente.

Nos testes, `FakeCatalog` substitui essa implementação por uma estrutura em memória.

Essa substituição permite testar o comportamento do sistema sem depender de uma conexão real com banco de dados.

## 5. Consequências para a manutenção

Os pontos identificados podem dificultar a inclusão de novas promoções, a alteração de regras comerciais e a validação de comportamentos existentes.

A concentração da lógica de descontos no carrinho aumenta o risco de modificar uma promoção e afetar outra.

A quantidade reduzida de testes também dificulta identificar regressões durante a modernização.

## 6. Recomendações iniciais

1. Ampliar os testes automatizados antes de modificar o comportamento existente.
2. Separar as responsabilidades de armazenamento do carrinho e cálculo das promoções.
3. Avaliar padrões de projeto que permitam organizar as diferentes políticas de desconto.
4. Preservar as regras antigas durante a refatoração.
5. Implementar os combos como uma funcionalidade independente e testável.
6. Validar os resultados com testes de regressão.

## 7. Limitações desta análise

Este diagnóstico foi elaborado a partir dos arquivos `catalog.py`, `model_objects.py`, `shopping_cart.py`, `teller.py`, `receipt.py`, `test_supermarket.py`, `fake_catalog.py` e `receipt_printer.py`.

As constatações devem ser complementadas pela execução de novos testes e pela revisão do restante do projeto.

Ainda não foram realizadas refatorações, implementações de combos ou auditorias de segurança.