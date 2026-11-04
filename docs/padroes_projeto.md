# Padrões de Projeto e Princípios de Qualidade

## 1. Objetivo

Aplicar padrões de projeto para reduzir o acoplamento, organizar as responsabilidades e facilitar a manutenção e a evolução do sistema de checkout.

## 2. Padrão Strategy

**Problema identificado:**

A classe `ShoppingCart`, principalmente no método `handle_offers`, concentra a lógica de cálculo das promoções. Diferentes tipos de ofertas são tratados por meio de várias condições, dificultando a manutenção e a inclusão de novas regras.

**Aplicação proposta:**

Utilizar o padrão Strategy para representar cada tipo de promoção por meio de uma estratégia independente de cálculo.

Exemplos de estratégias:

- `TenPercentDiscountStrategy`: calcula descontos percentuais.
- `ThreeForTwoStrategy`: calcula a promoção de três produtos pelo preço de dois.
- `TwoForAmountStrategy`: calcula a promoção de dois produtos por um valor definido.
- `FiveForAmountStrategy`: calcula a promoção de cinco produtos por um valor definido.
- `BundleDiscountStrategy`: calcula o desconto de 10% dos combos completos.

**Benefícios esperados:**

- Separação das regras de cálculo.
- Redução de condicionais na classe `ShoppingCart`.
- Facilidade para adicionar novas promoções.
- Maior facilidade para testar cada estratégia individualmente.

## 3. Padrão Factory Method

**Problema identificado:**

A seleção e a criação dos objetos responsáveis pelas promoções podem ficar misturadas com a lógica de execução do checkout.

**Aplicação proposta:**

Utilizar uma fábrica para identificar o tipo de promoção e criar a estratégia correspondente.

A fábrica receberá o tipo de oferta e retornará a estratégia adequada, mantendo a criação dos objetos separada da execução dos cálculos.

**Benefícios esperados:**

- Centralização da criação das estratégias.
- Redução do acoplamento entre as classes.
- Facilidade para incluir novos tipos de promoção.
- Organização do processo de seleção das regras.

## 4. Princípios SOLID relacionados

- **SRP (Responsabilidade Única):** cada estratégia será responsável pelo cálculo de um tipo de promoção.
- **OCP (Aberto/Fechado):** novas estratégias poderão ser adicionadas sem precisar modificar toda a lógica das promoções existentes.
- **DIP (Inversão de Dependência):** a lógica de aplicação das ofertas deverá depender de uma abstração comum, e não diretamente de implementações específicas.

## 5. Relação com Clean Code

A modernização também buscará:

- Utilizar nomes claros para classes, métodos e variáveis.
- Evitar métodos extensos e com múltiplas responsabilidades.
- Reduzir duplicações de código.
- Manter funções pequenas e objetivas.
- Facilitar a leitura e a compreensão das regras de negócio.

## 6. Validação

Os padrões serão considerados aplicados quando estiverem implementados no código e acompanhados de testes automatizados.

A implementação deverá preservar o comportamento das promoções antigas e permitir a inclusão da nova promoção de combos sem comprometer as funcionalidades existentes.