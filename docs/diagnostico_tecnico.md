# Diagnóstico Técnico — Sistema Legado de Supermercado

## 1. Visão geral do sistema

O projeto implementa um sistema simplificado de caixa de supermercado. Sua responsabilidade é registrar produtos e quantidades, consultar preços, aplicar ofertas promocionais, calcular o valor final da compra e disponibilizar os dados necessários para a geração de um recibo.

A implementação está organizada em Python, com separação entre modelos, carrinho de compras, caixa, catálogo e recibo.

A análise foi realizada considerando o código original, os testes existentes e os testes de caracterização desenvolvidos pelo grupo antes do início da refatoração.

## 2. Estrutura e responsabilidades identificadas

### `catalog.py`

Define a classe `SupermarketCatalog`, responsável pelas operações de cadastro e consulta de preços.

Os métodos `add_product()` e `unit_price()` possuem implementações que lançam exceções, indicando que acessariam o banco de dados.

Nos testes, essa dependência é substituída pela implementação `FakeCatalog`, que permite cadastrar produtos e consultar seus preços em memória.

### `model_objects.py`

Contém as estruturas utilizadas pelo sistema:

- `Product`: representa um produto e sua unidade de medida.
- `ProductQuantity`: associa um produto à quantidade.
- `ProductUnit`: define as unidades disponíveis, como unidade (`EACH`) e quilo (`KILO`).
- `SpecialOfferType`: define os tipos de promoção existentes.
- `Offer`: representa uma oferta associada a um produto.
- `Discount`: representa um desconto aplicado a um produto.

Os tipos de promoção originalmente implementados são:

- `THREE_FOR_TWO`: promoção leve três, pague dois.
- `TEN_PERCENT_DISCOUNT`: desconto percentual.
- `TWO_FOR_AMOUNT`: dois produtos por um valor fixo.
- `FIVE_FOR_AMOUNT`: cinco produtos por um valor fixo.

### `shopping_cart.py`

A classe `ShoppingCart` é responsável por armazenar os produtos adicionados à compra e suas respectivas quantidades.

O atributo `_items` mantém os registros individuais de cada adição ao carrinho, enquanto `_product_quantities` acumula as quantidades por produto.

O método `add_item()` adiciona uma unidade de determinado produto, delegando a operação ao método `add_item_quantity()`.

O método `handle_offers()` concentra a lógica de aplicação das promoções. Ele percorre os produtos do carrinho, consulta as ofertas cadastradas e calcula os descontos de acordo com o tipo de promoção.

Essa concentração de responsabilidades representa um dos principais pontos de atenção para a modernização.

### `teller.py`

A classe `Teller` coordena o processo de fechamento da compra.

O método `add_special_offer()` cadastra uma oferta para determinado produto.

O método `checks_out_articles_from()` percorre os itens do carrinho, consulta os preços no catálogo, adiciona os produtos ao recibo e solicita ao carrinho que processe as ofertas.

O método `product_with_name()` permite localizar produtos pelo nome no catálogo.

As ofertas são armazenadas em um dicionário cuja chave é o produto. Consequentemente, o cadastro de uma nova oferta para um produto que já possui uma promoção substitui a oferta anterior.

### `receipt.py`

Contém as classes `ReceiptItem` e `Receipt`.

A classe `ReceiptItem` representa um item individual do recibo, armazenando produto, quantidade, preço unitário e preço total.

A classe `Receipt` mantém listas separadas para os produtos e descontos da compra.

O método `total_price()` calcula o valor final somando os preços dos produtos e os valores dos descontos.

No comportamento original, os descontos convencionais são representados por valores negativos, que são somados ao total para reduzir o valor da compra.

As propriedades `items` e `discounts` retornam cópias das respectivas listas internas.

### `tests/receipt_printer.py`

A classe `ReceiptPrinter` está localizada na pasta `tests/`, e não na pasta `src/`.

É responsável por formatar os dados do recibo para apresentação textual, incluindo produtos, quantidades, descontos e valor total.

A implementação utiliza largura padrão de 40 caracteres, permite personalização dessa largura e apresenta os preços com duas casas decimais.

As quantidades de produtos vendidos por peso são apresentadas com três casas decimais.

Embora esteja localizada na pasta de testes, sua saída é importante para a preservação do comportamento original do sistema.

## 3. Fluxo geral de execução

O fluxo observado no código é:

1. O catálogo disponibiliza os preços dos produtos.
2. O `Teller` recebe o carrinho de compras.
3. O caixa percorre os registros individuais dos produtos adicionados.
4. Os preços unitários são consultados no catálogo.
5. Os produtos são adicionados ao recibo com suas quantidades e valores.
6. O método `handle_offers()` do carrinho verifica as ofertas cadastradas.
7. Os descontos identificados são adicionados ao recibo.
8. O recibo calcula o valor final da compra.
9. O `ReceiptPrinter` pode formatar os dados do recibo para apresentação.

## 4. Problemas e pontos de atenção identificados

### 4.1. Concentração da lógica de promoções

Arquivo: `src/shopping_cart.py`

Método: `handle_offers()`

O método reúne a verificação de diferentes tipos de promoção e o cálculo de seus respectivos descontos.

Isso concentra diferentes regras de negócio em um único método, tornando sua manutenção e expansão mais difíceis.

A inclusão de uma nova promoção, como os combos exigidos na atividade, poderá aumentar ainda mais a quantidade de condições e a complexidade desse método.

### 4.2. Uso de várias condições para selecionar promoções

Arquivo: `src/shopping_cart.py`

O método `handle_offers()` utiliza diversas verificações condicionais para tratar os tipos de oferta existentes.

Esse formato dificulta a extensão do sistema quando novas políticas de desconto são adicionadas, pois cada nova modalidade pode exigir alterações na lógica já existente.

É necessário avaliar uma estrutura que permita separar as regras de cada promoção.

### 4.3. Dependência do carrinho em relação às regras de desconto

Arquivo: `src/shopping_cart.py`

A classe `ShoppingCart` importa `SpecialOfferType` e `Discount` e conhece diretamente os tipos de promoção existentes.

Isso aumenta o conhecimento que a classe precisa ter sobre as regras comerciais do sistema.

A refatoração deve avaliar uma separação mais clara entre o armazenamento dos produtos e o cálculo e aplicação das políticas de desconto.

### 4.4. Ampliação da cobertura de testes

Arquivos: `tests/test_supermarket.py` e `tests/test_legacy_behavior.py`

O projeto original possuía apenas um teste automatizado no arquivo `test_supermarket.py`.

Esse teste configura uma oferta de 10% para escovas de dentes, mas adiciona maçãs ao carrinho. Portanto, verifica que uma oferta cadastrada para determinado produto não afeta outro produto, mas não comprova diretamente o funcionamento efetivo do desconto.

Para ampliar a proteção do comportamento legado, o grupo desenvolveu o arquivo `test_legacy_behavior.py`, contendo testes de caracterização organizados por categorias.

A suíte atual possui 46 testes automatizados:

- 1 teste original em `test_supermarket.py`;
- 45 testes de caracterização em `test_legacy_behavior.py`.

A execução de `python -m pytest -v` apresentou 46 testes aprovados.

Os novos testes contemplam cenários de carrinho vazio, inclusão de produtos, cálculo de valores, promoções existentes, interação entre ofertas, contratos da API pública e impressão do recibo.

Essa ampliação permite identificar alterações acidentais no comportamento do sistema durante a modernização.

### 4.5. Dependência de catálogo substituída nos testes

Arquivos: `src/catalog.py` e `tests/fake_catalog.py`

A classe `SupermarketCatalog` indica que suas operações acessariam um banco de dados e lança exceções quando chamadas diretamente.

Nos testes, `FakeCatalog` substitui essa implementação por uma estrutura em memória.

Essa substituição permite testar o comportamento do sistema sem depender de uma conexão real com banco de dados, tornando os testes mais rápidos e controlados.

### 4.6. Comportamentos peculiares identificados nos testes de caracterização

Arquivo: `tests/test_legacy_behavior.py`

Durante a análise do código e a elaboração dos testes de caracterização, foram identificados comportamentos particulares do sistema legado.

Esses comportamentos foram registrados intencionalmente para evitar alterações acidentais durante a refatoração.

Os principais casos identificados são:

**a) Conversão de quantidades para inteiro**

Nas promoções `THREE_FOR_TWO`, `TWO_FOR_AMOUNT` e `FIVE_FOR_AMOUNT`, a implementação utiliza `int(quantity)` para determinar a quantidade inteira considerada nos grupos promocionais.

Entretanto, em determinados cálculos, a quantidade original, inclusive sua parte fracionária, continua sendo utilizada.

**b) Comportamento da promoção `THREE_FOR_TWO` com quantidades fracionárias**

O sistema utiliza a parte inteira da quantidade para verificar se o limite da promoção foi atingido, mas considera a quantidade original no cálculo do desconto.

Por exemplo, uma quantidade de 2,9 não atinge o limite de três unidades, enquanto 3,5 pode gerar um desconto calculado sobre toda a quantidade.

**c) Divisão de ponto flutuante na promoção `TWO_FOR_AMOUNT`**

O cálculo da promoção utiliza divisão convencional (`/`) em vez de divisão inteira.

Em determinadas quantidades ímpares, esse comportamento pode gerar um valor de desconto positivo, aumentando o total da compra em vez de reduzi-lo.

Esse comportamento foi identificado e documentado nos testes como uma particularidade do sistema legado.

**d) Descrição das ofertas conforme o tipo do argumento**

A descrição do desconto utiliza a conversão direta do argumento para string.

Consequentemente, valores numericamente equivalentes podem gerar descrições diferentes. Por exemplo, `10` produz `10% off`, enquanto `10.0` produz `10.0% off`.

**e) Comportamento de ponto flutuante na apresentação dos preços**

O cálculo dos valores utiliza números de ponto flutuante. Em determinados casos, como o cálculo de 2,5 kg de um produto com preço de R$ 1,99 por quilo, o resultado pode apresentar pequenas diferenças de representação.

Isso pode influenciar a formatação final com duas casas decimais.

**f) Ordem de apresentação dos descontos**

A ordem dos descontos no recibo acompanha a ordem de inserção dos produtos no carrinho, conforme o comportamento dos dicionários utilizados na implementação.

**g) Substituição de ofertas**

O cadastro de uma segunda oferta para o mesmo produto substitui a oferta anteriormente cadastrada.

**h) Separação entre itens individuais e quantidades acumuladas**

O carrinho mantém cada adição de produto como um registro individual em `_items`, mas acumula as quantidades por produto em `_product_quantities`.

Assim, duas adições do mesmo produto podem gerar duas linhas no recibo, mesmo que a quantidade total seja considerada conjuntamente para o cálculo das promoções.

Essas particularidades devem ser consideradas durante a refatoração. Qualquer alteração intencional nesses comportamentos deverá ser justificada e acompanhada de testes e documentação, evitando mudanças acidentais nas regras existentes.

### 4.7. Dependência entre promoções e estrutura do carrinho

Arquivos: `src/shopping_cart.py` e `src/teller.py`

As ofertas existentes são associadas individualmente a produtos e processadas a partir das quantidades acumuladas no carrinho.

Esse modelo atende às promoções originais, mas não representa naturalmente uma promoção que dependa da combinação de produtos diferentes.

A nova promoção de combos exige identificar simultaneamente os produtos participantes, calcular a quantidade de combinações completas e aplicar o desconto somente aos produtos que efetivamente compõem cada combo.

Portanto, sua implementação exige avaliar uma lógica capaz de considerar múltiplos produtos, sem prejudicar as promoções existentes.

## 5. Consequências para a manutenção

Os pontos identificados podem dificultar a inclusão de novas promoções, a alteração de regras comerciais e a validação dos comportamentos existentes.

A concentração da lógica de descontos no carrinho aumenta o risco de modificar uma promoção e afetar outra.

A associação de ofertas a produtos individuais também limita a implementação de regras promocionais que dependem da combinação de diferentes produtos.

Além disso, as particularidades identificadas no comportamento legado exigem atenção durante a refatoração, pois alterações aparentemente simples podem modificar resultados financeiros ou a apresentação dos recibos.

A ampliação dos testes de caracterização reduz esse risco, fornecendo uma referência automatizada para verificar a preservação do comportamento original.

## 6. Recomendações iniciais

1. Manter e ampliar os testes automatizados antes de modificar o comportamento existente.
2. Separar as responsabilidades de armazenamento do carrinho e cálculo das promoções.
3. Avaliar padrões de projeto que permitam organizar e encapsular as diferentes políticas de desconto.
4. Preservar as regras antigas e os contratos públicos durante a refatoração.
5. Implementar os combos como uma funcionalidade independente e testável, considerando a participação de múltiplos produtos.
6. Definir e documentar como os descontos de combos coexistirão com as promoções antigas, evitando descontos duplicados ou indevidos.
7. Validar os resultados com testes de regressão, incluindo os cenários de caracterização já existentes.
8. Verificar se a formatação do recibo e os cálculos originais permanecem compatíveis após as alterações.
9. Realizar novas análises de segurança após a modernização e comparar os resultados com a avaliação inicial.

## 7. Limitações desta análise

Este diagnóstico foi elaborado a partir da análise dos arquivos:

- `src/catalog.py`;
- `src/model_objects.py`;
- `src/shopping_cart.py`;
- `src/teller.py`;
- `src/receipt.py`;
- `tests/test_supermarket.py`;
- `tests/test_legacy_behavior.py`;
- `tests/fake_catalog.py`;
- `tests/receipt_printer.py`.

Também foram considerados os resultados da execução da suíte de testes automatizados, que apresentou 46 testes aprovados no ambiente analisado.

As constatações representam o comportamento observado antes da refatoração.

Ainda não foram realizadas alterações no código de produção, implementação da promoção de combos ou auditorias de segurança posteriores à modernização.

As decisões de arquitetura e implementação deverão ser complementadas pela análise dos requisitos, dos padrões de projeto e dos testes de regressão.