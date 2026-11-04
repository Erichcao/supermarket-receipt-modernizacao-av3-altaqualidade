# Levantamento de Requisitos

## 1. Objetivo

Modernizar incrementalmente o sistema legado de checkout de supermercado, preservando as funcionalidades existentes e melhorando sua organização, manutenção, testabilidade e segurança.

## 2. Requisitos funcionais (RF)

| ID | Requisito |
|---|---|
| RF01 | Cadastrar e consultar produtos e seus preços. |
| RF02 | Adicionar produtos e quantidades ao carrinho de compras. |
| RF03 | Calcular o preço total dos produtos adicionados. |
| RF04 | Aplicar as promoções existentes: 10% de desconto, 3 por 2, 2 por determinado valor e 5 por determinado valor. |
| RF05 | Gerar o recibo com os produtos, quantidades, preços e descontos aplicados. |
| RF06 | Permitir o cadastro de promoções de combos compostos por produtos definidos. |
| RF07 | Aplicar 10% de desconto somente aos produtos que fazem parte de combos completos. |
| RF08 | Permitir a formação de mais de um combo quando houver quantidade suficiente de produtos. |
| RF09 | Não aplicar o desconto de combo quando os produtos necessários estiverem incompletos. |
| RF10 | Garantir que produtos excedentes não recebam desconto de combo. |

## 3. Regras de negócio dos combos

- Cada combo será formado por um conjunto previamente definido de produtos e quantidades.
- Quando todos os produtos necessários estiverem presentes no carrinho, será aplicado desconto de 10% somente nos itens que compõem o combo.
- A quantidade disponível deverá determinar quantos combos completos podem ser formados.
- Produtos excedentes ou pertencentes a combos incompletos serão cobrados pelo preço normal, salvo outra promoção válida.
- O mesmo item não poderá receber descontos incompatíveis ou ser contabilizado duas vezes no mesmo combo.
- A convivência entre a promoção de combo e as promoções antigas deverá ser definida e documentada antes da implementação.

**Exemplos:**

| Compra | Resultado esperado |
|---|---|
| 1 escova + 1 pasta | 1 combo com 10% de desconto nos dois produtos. |
| 2 escovas + 1 pasta | 1 combo com desconto; 1 escova sem desconto de combo. |
| 2 escovas + 2 pastas | 2 combos, com desconto nos quatro produtos. |
| 1 escova + 0 pastas | Nenhum desconto de combo. |

## 4. Requisitos não funcionais (RNF)

| ID | Requisito |
|---|---|
| RNF01 | Preservar o comportamento das funcionalidades existentes durante a modernização. |
| RNF02 | Manter o código organizado, legível e dividido em responsabilidades bem definidas. |
| RNF03 | Aplicar pelo menos dois padrões de projeto adequados ao problema. |
| RNF04 | Permitir testes automatizados das funcionalidades e regras de negócio. |
| RNF05 | Evitar dependências desnecessárias entre as classes e facilitar futuras alterações. |
| RNF06 | Avaliar vulnerabilidades e dependências utilizando Bandit, pip-audit e Safety. |
| RNF07 | Documentar a instalação, execução, testes e estrutura do projeto. |

## 5. Critérios de aceitação

- Os testes das funcionalidades originais devem continuar passando após as alterações.
- Os descontos antigos devem manter seus comportamentos esperados.
- Combos completos devem receber 10% de desconto somente nos itens participantes.
- Combos incompletos não devem gerar desconto.
- Quantidades excedentes não devem receber desconto indevido.
- A aplicação não deve acumular descontos incompatíveis sobre os mesmos itens.
- Os testes automatizados devem validar os principais cenários, inclusive casos de limite.
- As ferramentas de segurança devem ser executadas antes e depois da modernização, com seus resultados registrados.