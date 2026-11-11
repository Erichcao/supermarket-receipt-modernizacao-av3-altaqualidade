# Requisitos do Sistema

## 1. Requisitos Funcionais (RF)

**RF01 – Cadastro de produtos**
O sistema deve permitir o cadastro de produtos com nome, preço e unidade de venda.

**RF02 – Consulta de produtos**
O sistema deve permitir consultar os produtos disponíveis no catálogo.

**RF03 – Criação de carrinho de compras**
O sistema deve permitir criar um carrinho contendo os produtos selecionados pelo cliente e suas respectivas quantidades.

**RF04 – Cálculo do valor total**
O sistema deve calcular o valor total da compra considerando os produtos e suas quantidades.

**RF05 – Aplicação de promoções individuais**
O sistema deve aplicar as promoções individuais disponíveis, respeitando suas regras e condições.

**RF06 – Promoção de três unidades pelo preço de duas**
O sistema deve permitir aplicar a promoção em que, a cada três unidades elegíveis do mesmo produto, o cliente paga apenas duas.

**RF07 – Promoção de duas unidades por valor fixo**
O sistema deve permitir aplicar uma promoção em que duas unidades de determinado produto são vendidas por um valor promocional fixo.

**RF08 – Promoção de cinco unidades por valor fixo**
O sistema deve permitir aplicar uma promoção em que cinco unidades de determinado produto são vendidas por um valor promocional fixo.

**RF09 – Desconto de 10% em combos de produtos**
O sistema deve permitir cadastrar ofertas de combos compostos por diferentes produtos e aplicar 10% de desconto sobre o valor total dos produtos que formam cada combo completo.

**RF10 – Verificação de combos completos**
O sistema deve verificar se o carrinho possui as quantidades necessárias de cada produto para formar um ou mais combos completos. Combos incompletos não devem receber o desconto.

**RF11 – Controle de utilização dos produtos nos combos**
O sistema deve impedir que uma mesma unidade de produto seja utilizada em mais de um combo ou receba simultaneamente o desconto do combo e uma promoção individual.

**RF12 – Aproveitamento de unidades excedentes**
As unidades que não forem utilizadas na formação de combos devem permanecer elegíveis para as promoções individuais, desde que atendam às condições dessas promoções.

**RF13 – Restrição por unidade de venda**
O sistema não deve permitir que produtos vendidos por peso participem da composição dos combos. Apenas produtos vendidos por unidade podem ser utilizados nessas ofertas.

## 2. Requisitos Não Funcionais (RNF)

**RNF01 – Organização do código**
O código deve ser organizado em módulos, facilitando a manutenção e a evolução do sistema.

**RNF02 – Manutenibilidade**
O sistema deve permitir a inclusão de novas promoções sem exigir alterações significativas na estrutura existente.

**RNF03 – Reutilização**
As funcionalidades devem ser implementadas de forma que possam ser reutilizadas em diferentes partes do sistema.

**RNF04 – Compatibilidade**
As alterações devem preservar o funcionamento das funcionalidades já existentes no sistema.

**RNF05 – Testabilidade**
O sistema deve possuir testes automatizados que verifiquem o comportamento das funcionalidades originais e das novas implementações.

**RNF06 – Confiabilidade**
O sistema deve calcular corretamente os valores das compras e aplicar os descontos de acordo com as regras estabelecidas.

**RNF07 – Segurança**
O projeto deve ser submetido a ferramentas de análise de segurança de código e de dependências, permitindo identificar e documentar possíveis vulnerabilidades.

**RNF08 – Documentação**
O projeto deve possuir documentação sobre sua estrutura, requisitos, decisões de implementação, padrões de projeto utilizados e resultados das análises realizadas.

## 3. Regras de Negócio dos Combos

### 3.1. Composição dos combos

- Cada combo deve possuir uma composição identificável, permitindo reconhecer os produtos participantes e representar o desconto correspondente no recibo.
- A composição deve especificar os produtos e as respectivas quantidades necessárias para formar o combo.
- O desconto de 10% deve ser aplicado somente quando todos os produtos e quantidades exigidos estiverem presentes no carrinho.
- Apenas produtos vendidos por unidade podem participar dos combos.
- Produtos vendidos por peso não devem ser considerados elegíveis para essas ofertas.

### 3.2. Aplicação do desconto

- O desconto de 10% deve ser calculado sobre o valor total dos produtos que compõem cada combo completo.
- O desconto deve ser aplicado somente às unidades efetivamente utilizadas na formação do combo.
- Combos incompletos não devem receber desconto.
- O sistema deve permitir a formação de mais de um combo quando houver quantidades suficientes de produtos.

### 3.3. Exclusividade por unidade

- Cada unidade de produto pode participar de apenas um combo.
- Uma unidade utilizada em um combo não pode receber simultaneamente uma promoção individual.
- As unidades excedentes, que não forem utilizadas na formação de combos, permanecem elegíveis para as promoções individuais, desde que atendam às condições correspondentes.
- O sistema deve controlar as quantidades utilizadas para impedir a duplicidade de descontos.

### 3.4. Validação das ofertas

- O sistema deve validar o percentual de desconto informado no cadastro da oferta.
- Percentuais inválidos, incluindo valores iguais ou inferiores a zero e superiores a 100%, não devem ser aceitos.
- Valores que não sejam numéricos também devem ser rejeitados.

## 4. Critérios de Aceitação

A implementação será considerada adequada quando:

1. O sistema cadastrar e consultar produtos corretamente.
2. O carrinho calcular corretamente o valor total da compra.
3. As promoções individuais existentes continuarem funcionando conforme o comportamento original.
4. O sistema aplicar o desconto de 10% somente em combos completos.
5. O sistema permitir a formação de múltiplos combos quando houver produtos suficientes.
6. O sistema impedir que uma mesma unidade receba descontos duplicados.
7. As unidades excedentes continuarem elegíveis às promoções individuais.
8. Combos incompletos não receberem desconto.
9. Produtos vendidos por peso não participarem dos combos.
10. O sistema rejeitar percentuais de desconto inválidos no cadastro das ofertas.
11. Os testes automatizados validarem os comportamentos originais e as novas funcionalidades.
12. A documentação apresentar os requisitos, as decisões de implementação e os resultados das análises de segurança.