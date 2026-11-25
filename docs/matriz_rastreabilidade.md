# Matriz de rastreabilidade

A matriz relaciona os requisitos do projeto à implementação, aos testes e às evidências disponíveis na entrega.

| Requisito | Implementação | Teste(s) relacionado(s) | Evidência |
|---|---|---|---|
| RF01–RF02 — cadastro e consulta de produtos | FakeCatalog, Teller.product_with_name | test_product_with_name | evidencias/testes_final.txt |
| RF03–RF04 — carrinho, quantidades e total | ShoppingCart, Teller.checks_out_articles_from, Receipt.total_price | TestCarrinhoSemOfertas | evidencias/testes_final.txt |
| RF05–RF08 — promoções individuais existentes | PromotionFactory e estratégias em src/promotions/ | TestDezPorCento, TestLeveTresPagueDois, TestDoisPorValor, TestCincoPorValor | evidencias/testes_final.txt |
| RF09–RF10 — cadastro e identificação de combos completos | Teller.add_bundle_offer, BundleOffer, BundleDiscountStrategy | test_aplica_desconto_em_um_combo_completo, test_nao_aplica_desconto_em_combo_incompleto | evidencias/testes_final.txt |
| RF11–RF12 — exclusividade por unidade e excedentes | ShoppingCart.handle_offers e quantidades reservadas | test_unidades_excedentes_continuam_elegiveis_a_promocao_individual, test_combo_sobreposto_respeita_ordem_de_cadastro | evidencias/testes_final.txt |
| RF13 — restrição a produtos por unidade | validação de ProductUnit.EACH em ShoppingCart.handle_offers | test_produtos_vendidos_por_peso_nao_participam_de_combos | evidencias/testes_final.txt |
| RF14 — geração e conteúdo do recibo | Teller.checks_out_articles_from, Receipt, ReceiptPrinter | TestReciboImpresso e test_combo_e_desconto_aparecem_no_recibo_impresso | evidencias/testes_final.txt |
| RNF01–RNF03 — organização, manutenibilidade e reutilização | módulos de carrinho, checkout, recibo e estratégias | testes das estratégias e da fábrica | estrutura de src/ e evidencias/testes_final.txt |
| RNF04–RNF06 — compatibilidade, testabilidade e confiabilidade | suíte de caracterização e regressão | tests/test_legacy_behavior.py | evidencias/testes_final.txt, evidencias/cobertura_final.txt |
| RNF07 — segurança | configuração de dependências e auditorias | Bandit, pip-audit e Safety | docs/seguranca_antes_depois.md, relatórios em evidencias/ |
| RNF08 — documentação | arquivos em docs/ e README | revisão documental | este documento e README |

## Observação sobre evidências históricas

evidencias/testes_originais.txt registra um teste aprovado no código original. A suíte final contém 45 casos de caracterização, mas o repositório não contém um log que comprove que esses 45 casos foram executados antes da refatoração. A rastreabilidade não atribui a eles uma execução prévia sem evidência.


A suíte foi ampliada com testes de convivência entre combo e cada modalidade individual (10%, 3 por 2, 2 por valor e 5 por valor), teste de combos sobrepostos, recibo impresso de combo e quantidades zero/negativa com desconto percentual.
