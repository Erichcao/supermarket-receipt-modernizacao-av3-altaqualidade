# Padrões de Projeto e Princípios de Qualidade

## 1. Objetivo

Aplicar padrões de projeto e princípios de qualidade para reduzir o acoplamento, organizar as responsabilidades e facilitar a manutenção e a evolução do sistema legado de checkout.

A modernização foi realizada de forma incremental, preservando o comportamento das funcionalidades existentes e permitindo a inclusão de novas regras de negócio, especialmente a promoção de combos.

Foram aplicados os padrões Strategy e Factory Method, considerando os problemas identificados durante a análise da arquitetura original.

## 2. Padrão Strategy

### Problema identificado

A classe `ShoppingCart`, principalmente no método `handle_offers`, concentrava a lógica de cálculo e aplicação das promoções.

Os diferentes tipos de ofertas eram identificados por meio de estruturas condicionais, tornando o método extenso e aumentando sua complexidade conforme novas regras eram adicionadas.

Essa organização dificultava a manutenção, os testes isolados e a inclusão de novos tipos de promoção.

### Aplicação realizada

O padrão Strategy foi utilizado para encapsular cada regra de cálculo de promoção em uma estratégia independente.

As estratégias implementam uma abstração comum, permitindo que o sistema execute diferentes regras sem precisar conhecer os detalhes internos de cada cálculo.

Foram implementadas as seguintes estratégias:

- `TenPercentDiscountStrategy`: calcula descontos percentuais.
- `ThreeForTwoStrategy`: calcula a promoção de três produtos pelo preço de dois.
- `TwoForAmountStrategy`: calcula a promoção de dois produtos por um valor definido.
- `FiveForAmountStrategy`: calcula a promoção de cinco produtos por um valor definido.
- `BundleDiscountStrategy`: identifica unidades participantes de combos completos e calcula o desconto correspondente.

A estratégia de combos considera as quantidades necessárias para formar cada combinação, permitindo a formação de múltiplos combos e evitando que unidades excedentes recebam indevidamente o desconto.

Também respeita a regra de exclusividade por unidade definida nos requisitos: unidades utilizadas em combos não recebem simultaneamente promoções individuais incompatíveis, enquanto unidades excedentes continuam elegíveis às ofertas antigas, desde que atendam às suas condições.

### Benefícios obtidos

- Separação das regras de cálculo das promoções.
- Redução de condicionais na lógica central do carrinho.
- Maior isolamento das responsabilidades.
- Facilidade para adicionar novos tipos de promoção.
- Possibilidade de testar cada estratégia individualmente.
- Melhor organização da implementação da nova promoção de combos.

## 3. Padrão Factory Method

### Problema identificado

A seleção e a criação dos objetos responsáveis pelas promoções poderiam ficar misturadas com a lógica de execução do checkout.

Quando diferentes estratégias são adicionadas diretamente à lógica principal, o sistema passa a conhecer detalhes de criação e implementação de cada tipo de promoção, aumentando o acoplamento.

### Aplicação realizada

O padrão Factory Method foi aplicado por meio da classe `PromotionFactory`, responsável por centralizar a criação e a seleção das estratégias de promoção.

A fábrica recebe as informações necessárias sobre o tipo de oferta e retorna a estratégia correspondente, mantendo a criação dos objetos separada da execução dos cálculos.

Essa estrutura trabalha em conjunto com a abstração comum definida para as estratégias.

### Benefícios obtidos

- Centralização da criação das estratégias.
- Separação entre criação e execução das promoções.
- Redução do acoplamento entre as classes.
- Facilidade para incluir novos tipos de promoção.
- Organização do processo de seleção das regras.

## 4. Princípios SOLID relacionados

A modernização buscou aplicar os seguintes princípios:

- **SRP (Responsabilidade Única):** cada estratégia é responsável por uma regra específica de promoção, evitando a concentração de diferentes cálculos em uma única classe.
- **OCP (Aberto/Fechado):** novas estratégias podem ser adicionadas por meio da abstração comum, reduzindo a necessidade de modificar a lógica central de execução das promoções.
- **DIP (Inversão de Dependência):** a execução das promoções trabalha com uma abstração comum de estratégia, em vez de depender diretamente dos detalhes de cada implementação.

A aplicação desses princípios é demonstrada pela estrutura implementada e pelos testes automatizados.

## 5. Relação com Clean Code

A modernização também buscou seguir práticas de Clean Code:

- Utilizar nomes claros e significativos para classes, métodos e variáveis.
- Evitar métodos extensos e com múltiplas responsabilidades.
- Reduzir duplicações de código.
- Manter funções pequenas e objetivas.
- Evitar condicionais desnecessárias.
- Organizar as responsabilidades de cada classe.
- Facilitar a leitura, os testes e a compreensão das regras de negócio.

## 6. Validação

A aplicação dos padrões foi validada por meio da implementação no código e de testes automatizados.

A validação contempla:

- Testes individuais das estratégias de promoção.
- Testes de seleção e criação das estratégias pela fábrica.
- Preservação dos comportamentos das promoções antigas.
- Aplicação correta dos descontos em combos completos.
- Ausência de descontos em combos incompletos.
- Tratamento correto de múltiplos combos e unidades excedentes.
- Respeito à regra de exclusividade por unidade.
- Aprovação dos testes de regressão do sistema.

A implementação busca reduzir o acoplamento e melhorar a organização interna do sistema sem comprometer os contratos públicos e o comportamento legado protegido pelos testes de caracterização.