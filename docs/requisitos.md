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

**RF14 – Geração e conteúdo do recibo**
O sistema deve gerar um recibo contendo os produtos, quantidades, preços unitários, valores totais por item, descontos aplicados e total final da compra. Os descontos de combo devem ser identificáveis no recibo sem alterar indevidamente os itens originais da compra.

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

**Critérios verificáveis dos RNF**

- RNF01: responsabilidades de catálogo, carrinho, checkout, recibo e estratégias devem estar separadas em módulos identificáveis; verificar pela estrutura de `src/`.
- RNF02: uma nova estratégia individual deve poder ser adicionada como classe própria, com registro correspondente na `PromotionFactory`; a limitação do mapeamento deve permanecer documentada.
- RNF03: os cálculos de promoções devem ser executáveis por estratégias isoladas e cobertos por testes específicos.
- RNF04: os cenários de comportamento legado cobertos em `tests/test_legacy_behavior.py` devem continuar aprovados após alterações.
- RNF05: `python -m pytest -v` deve concluir com todos os testes aprovados; a suíte final contém 70 testes automatizados aprovados, conforme registrado em `evidencias/testes_final.txt`.
- RNF06: os valores de descontos e totais devem ser verificados por asserts numéricos, usando tolerância para cálculos de ponto flutuante.
- RNF07: Bandit, pip-audit e Safety devem ser executados sobre os escopos documentados, com versões, comandos e resultados registrados.
- RNF08: cada requisito funcional deve apontar para implementação, teste e evidência na rastreabilidade do projeto.

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

- **CA01 — Cadastro e consulta:** produtos cadastrados devem ser recuperáveis pelo catálogo; validar com `test_product_with_name`.
- **CA02 — Carrinho e total:** quantidades e preços devem compor o total sem ofertas; validar com `test_varios_produtos_somam_total` e testes de recibo.
- **CA03 — Promoções existentes:** 10%, 3 por 2, 2 por valor e 5 por valor devem preservar os resultados caracterizados; validar pelas classes `TestDezPorCento`, `TestLeveTresPagueDois`, `TestDoisPorValor` e `TestCincoPorValor`.
- **CA04 — Combo completo:** 1 escova + 1 pasta deve receber 10% sobre o valor dos dois produtos; validar com `test_aplica_desconto_em_um_combo_completo`.
- **CA05 — Combo incompleto:** somente escova, sem pasta, não deve gerar desconto; validar com `test_nao_aplica_desconto_em_combo_incompleto`.
- **CA06 — Múltiplos combos:** 2 escovas + 2 pastas devem formar dois combos; validar com `test_aplica_desconto_em_dois_combos_completos`.
- **CA07 — Produto repetido na composição:** um combo que exige 2 escovas + 1 pasta só pode ser formado quando as três unidades estiverem disponíveis; validar com `test_combo_com_produto_repetido_exige_quantidade_correta`.
- **CA08 — Excedentes:** unidades não reservadas pelo combo devem continuar elegíveis à promoção individual; validar com `test_unidades_excedentes_continuam_elegiveis_a_promocao_individual`.
- **CA09 — Sem duplicidade:** uma unidade não pode ser reservada por dois combos nem receber simultaneamente desconto de combo e individual; validar pelos testes de interação de combos.
- **CA10 — Produto por peso:** produtos `KILO` não podem integrar combos; validar com `test_produtos_vendidos_por_peso_nao_participam_de_combos`.
- **CA11 — Percentual inválido:** percentuais menores/iguais a zero, acima de 100 ou não numéricos devem ser rejeitados; validar com `test_rejeita_percentuais_de_desconto_invalidos`.
- **CA12 — Recibo:** o recibo deve exibir itens, descontos e total; validar com os testes de `TestReciboImpresso` e o teste de recibo de combo.
- **CA13 — Regressão:** a suíte completa deve passar; a execução final registra 70 testes automatizados aprovados em `evidencias/testes_final.txt`.