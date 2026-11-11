# Padrões de Projeto e Princípios de Qualidade

## 1. Objetivo

Aplicar padrões de projeto e princípios de qualidade para reduzir o acoplamento, organizar as responsabilidades e facilitar a manutenção e a evolução do sistema legado de checkout.

A modernização será realizada de forma incremental, preservando o comportamento das funcionalidades existentes e permitindo a inclusão de novas regras de negócio, especialmente a promoção de combos.

Os padrões escolhidos foram Strategy e Factory Method, considerando os problemas identificados durante a análise da arquitetura atual.

## 2. Padrão Strategy

### Problema identificado

A classe `ShoppingCart`, principalmente no método `handle_offers`, concentra a lógica de cálculo e aplicação das promoções.

Atualmente, os diferentes tipos de ofertas são identificados por meio de estruturas condicionais, tornando o método extenso e aumentando sua complexidade conforme novas regras são adicionadas.

Essa organização dificulta a manutenção, os testes isolados e a inclusão de novos tipos de promoção.

### Aplicação proposta

Utilizar o padrão Strategy para encapsular cada regra de cálculo de promoção em uma estratégia independente.

Cada estratégia deverá implementar uma abstração comum, permitindo que o sistema execute diferentes regras sem precisar conhecer os detalhes internos de cada cálculo.

Exemplos de estratégias previstas:

- `TenPercentDiscountStrategy`: calcula descontos percentuais.
- `ThreeForTwoStrategy`: calcula a promoção de três produtos pelo preço de dois.
- `TwoForAmountStrategy`: calcula a promoção de dois produtos por um valor definido.
- `FiveForAmountStrategy`: calcula a promoção de cinco produtos por um valor definido.
- `BundleDiscountStrategy`: identifica unidades participantes de combos completos e calcula o desconto de 10% correspondente.

A estratégia de combos deverá considerar as quantidades necessárias para formar cada combinação, permitindo múltiplos combos e evitando que unidades excedentes recebam indevidamente o desconto.

Também deverá respeitar a regra de exclusividade por unidade definida nos requisitos: unidades utilizadas em combos não poderão receber simultaneamente promoções individuais incompatíveis, enquanto unidades excedentes continuarão elegíveis às ofertas antigas.

### Benefícios esperados

- Separação das regras de cálculo das promoções.
- Redução de condicionais na lógica central do carrinho.
- Maior isolamento das responsabilidades.
- Facilidade para adicionar novos tipos de promoção.
- Possibilidade de testar cada estratégia individualmente.
- Melhor organização da implementação da nova promoção de combos.

## 3. Padrão Factory Method

### Problema identificado

A seleção e a criação dos objetos responsáveis pelas promoções podem ficar misturadas com a lógica de execução do checkout.

Quando diferentes estratégias são adicionadas diretamente à lógica principal, o sistema passa a conhecer detalhes de criação e implementação de cada tipo de promoção, aumentando o acoplamento.

### Aplicação proposta

Utilizar o padrão Factory Method para centralizar a criação e a seleção das estratégias de promoção.

A fábrica receberá as informações necessárias sobre o tipo de oferta e retornará a estratégia correspondente, mantendo a criação dos objetos separada da execução dos cálculos.

A estrutura deverá trabalhar em conjunto com a abstração comum definida para as estratégias.

### Benefícios esperados

- Centralização da criação das estratégias.
- Separação entre criação e execução das promoções.
- Redução do acoplamento entre as classes.
- Facilidade para incluir novos tipos de promoção.
- Organização do processo de seleção das regras.

## 4. Princípios SOLID relacionados

A modernização buscará aplicar os seguintes princípios:

- **SRP (Responsabilidade Única):** cada estratégia será responsável por uma regra específica de promoção, evitando a concentração de diferentes cálculos em uma única classe.
- **OCP (Aberto/Fechado):** novas estratégias poderão ser adicionadas por meio da abstração comum, reduzindo a necessidade de modificar a lógica central de execução das promoções.
- **DIP (Inversão de Dependência):** o componente responsável por executar as promoções deverá depender de uma abstração comum de estratégia, em vez de depender diretamente de implementações específicas.

A aplicação desses princípios deverá ser demonstrada pela estrutura efetivamente implementada, não apenas pela existência das classes correspondentes aos padrões.

## 5. Relação com Clean Code

A modernização também buscará seguir práticas de Clean Code:

- Utilizar nomes claros e significativos para classes, métodos e variáveis.
- Evitar métodos extensos e com múltiplas responsabilidades.
- Reduzir duplicações de código.
- Manter funções pequenas e objetivas.
- Evitar condicionais desnecessárias.
- Organizar as responsabilidades de cada classe.
- Facilitar a leitura, os testes e a compreensão das regras de negócio.

## 6. Validação

Os padrões serão considerados efetivamente aplicados quando estiverem implementados no código e acompanhados de testes automatizados que demonstrem seu funcionamento.

A validação deverá contemplar:

- Testes individuais das estratégias de promoção.
- Testes de seleção e criação das estratégias pela fábrica.
- Preservação dos comportamentos das promoções antigas.
- Aplicação correta dos descontos em combos completos.
- Ausência de descontos em combos incompletos.
- Tratamento correto de múltiplos combos e unidades excedentes.
- Respeito à regra de exclusividade por unidade.
- Aprovação dos testes de regressão do sistema.

A implementação deverá reduzir o acoplamento e melhorar a organização interna do sistema sem comprometer os contratos públicos e o comportamento legado protegido pelos testes de caracterização.