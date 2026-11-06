# Levantamento de Requisitos

## 1. Objetivo

Modernizar incrementalmente o sistema legado de checkout de supermercado, preservando as funcionalidades existentes e melhorando sua organização, manutenção, testabilidade e segurança.

A modernização deverá incluir uma nova funcionalidade de promoção de combos, permitindo conceder descontos de 10% sobre produtos que participem de combinações completas previamente definidas.

## 2. Requisitos funcionais (RF)

| ID | Requisito |
|---|---|
| RF01 | Cadastrar e consultar produtos e seus preços. |
| RF02 | Adicionar produtos e quantidades ao carrinho de compras. |
| RF03 | Calcular o preço total dos produtos adicionados. |
| RF04 | Aplicar as promoções existentes: 10% de desconto, 3 por 2, 2 por determinado valor e 5 por determinado valor. |
| RF05 | Gerar o recibo com os produtos, quantidades, preços e descontos aplicados. |
| RF06 | Permitir o cadastro de promoções de combos compostos por produtos previamente definidos, suas respectivas quantidades e percentual de desconto. |
| RF07 | Aplicar 10% de desconto somente às unidades dos produtos que fazem parte de combos completos. |
| RF08 | Permitir a formação de mais de um combo quando houver quantidade suficiente de produtos. |
| RF09 | Não aplicar o desconto de combo quando os produtos necessários estiverem incompletos. |
| RF10 | Garantir que produtos excedentes não recebam desconto de combo. |
| RF11 | Impedir que uma mesma unidade de produto receba simultaneamente o desconto de combo e outra promoção incompatível. |
| RF12 | Permitir que unidades excedentes, não utilizadas na formação de combos, continuem elegíveis às promoções antigas, conforme suas regras originais. |

## 3. Regras de negócio dos combos

### 3.1. Cadastro e composição

- Cada combo deverá possuir uma identificação ou nome.
- Cada combo será formado por um conjunto previamente definido de produtos e suas respectivas quantidades.
- O percentual de desconto será de 10%.
- A quantidade de cada produto necessária para formar o combo deverá ser respeitada.
- O sistema deverá identificar automaticamente quantos combos completos podem ser formados a partir das quantidades disponíveis no carrinho.

### 3.2. Aplicação dos descontos

- Quando todos os produtos e quantidades necessários estiverem presentes no carrinho, será aplicado desconto de 10% somente às unidades que compõem os combos completos.
- A quantidade disponível deverá determinar quantos combos completos podem ser formados.
- Produtos excedentes ou pertencentes a combinações incompletas não receberão desconto de combo.
- Produtos excedentes poderão receber outras promoções válidas, desde que respeitadas as regras originais dessas promoções.
- Uma mesma unidade de produto não poderá participar de mais de um combo na mesma compra.
- Uma mesma unidade não poderá receber simultaneamente o desconto de combo e outra promoção incompatível.

### 3.3. Regra de coexistência com as promoções antigas

Será adotada a regra de **exclusividade por unidade**.

Isso significa que:

1. As unidades utilizadas na formação de combos completos receberão exclusivamente o desconto de 10% do combo.
2. Essas mesmas unidades não participarão de outras promoções individuais.
3. As unidades excedentes, que não forem utilizadas na formação dos combos, continuarão elegíveis às promoções antigas, respeitando as condições e os limites de cada oferta.
4. Os descontos deverão ser calculados sem contabilizar uma mesma unidade mais de uma vez.
5. A aplicação dos descontos deverá respeitar a separação entre unidades participantes de combos e unidades excedentes.

Essa regra tem como objetivo impedir a acumulação indevida de descontos e preservar a possibilidade de aplicação das promoções antigas aos produtos que não participarem de combos.

### 3.4. Exemplos

Considerando um combo formado por uma escova de dentes e uma pasta de dentes:

| Compra | Combos completos | Resultado esperado |
|---|---:|---|
| 1 escova + 1 pasta | 1 | 10% de desconto nos dois produtos. |
| 2 escovas + 1 pasta | 1 | 10% em uma escova e uma pasta; a escova excedente permanece sem desconto de combo. |
| 2 escovas + 2 pastas | 2 | 10% de desconto nos quatro produtos. |
| 3 escovas + 1 pasta | 1 | 10% em uma escova e uma pasta; duas escovas excedentes permanecem elegíveis às promoções antigas. |
| 1 escova + 0 pastas | 0 | Nenhum desconto de combo. |
| 0 escovas + 2 pastas | 0 | Nenhum desconto de combo. |

## 4. Requisitos não funcionais (RNF)

| ID | Requisito |
|---|---|
| RNF01 | Preservar o comportamento das funcionalidades existentes durante a modernização, incluindo os contratos públicos e os comportamentos registrados nos testes de caracterização. |
| RNF02 | Manter o código organizado, legível e dividido em responsabilidades bem definidas. |
| RNF03 | Aplicar pelo menos dois padrões de projeto adequados ao problema. |
| RNF04 | Permitir testes automatizados das funcionalidades e regras de negócio. |
| RNF05 | Evitar dependências desnecessárias entre as classes e facilitar futuras alterações. |
| RNF06 | Avaliar vulnerabilidades e dependências utilizando Bandit, pip-audit e Safety. |
| RNF07 | Documentar a instalação, execução, testes e estrutura do projeto. |
| RNF08 | Garantir que a aplicação dos descontos seja determinística, evitando duplicidade de descontos sobre as mesmas unidades de produtos. |

## 5. Critérios de aceitação

- Os testes das funcionalidades originais devem continuar passando após as alterações.
- Os contratos públicos existentes devem ser preservados.
- Os descontos antigos devem manter seus comportamentos registrados nos testes de caracterização.
- Combos completos devem receber 10% de desconto somente nas unidades participantes.
- Combos incompletos não devem gerar desconto.
- Quantidades excedentes não devem receber desconto indevido de combo.
- Quantidades suficientes devem permitir a formação de múltiplos combos.
- Uma mesma unidade não poderá receber simultaneamente o desconto de combo e outra promoção incompatível.
- Produtos excedentes deverão continuar elegíveis às promoções antigas, respeitando as regras dessas ofertas.
- Os descontos deverão ser calculados sem duplicidade ou contabilização repetida de unidades.
- Os testes automatizados deverão validar os principais cenários, incluindo casos de limite, quantidades excedentes e interação entre promoções.
- A impressão do recibo deverá continuar apresentando corretamente produtos, quantidades, descontos e total da compra.
- As ferramentas de segurança deverão ser executadas antes e depois da modernização, com seus resultados registrados.