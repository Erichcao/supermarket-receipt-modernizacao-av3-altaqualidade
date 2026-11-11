"""
Testes de caracterização do comportamento LEGADO do Supermarket Receipt.

Objetivo: congelar o que o sistema faz HOJE (inclusive comportamentos
estranhos), para detectar qualquer mudança acidental durante a refatoração.

Regra de ouro: estes testes NÃO dizem o que o sistema DEVERIA fazer, e sim
o que ele FAZ. Casos marcados com "QUIRK" são comportamentos questionáveis
do legado que foram preservados de propósito. Não "corrija" esses testes
durante a refatoração; se um deles falhar, o comportamento mudou.
"""
import pytest

from model_objects import Product, ProductUnit, SpecialOfferType
from shopping_cart import ShoppingCart
from teller import Teller
from tests.fake_catalog import FakeCatalog
from tests.receipt_printer import ReceiptPrinter


# --------------------------------------------------------------------------
# Fixtures e helpers
# --------------------------------------------------------------------------
@pytest.fixture
def toothbrush():
    return Product("toothbrush", ProductUnit.EACH)


@pytest.fixture
def toothpaste():
    return Product("toothpaste", ProductUnit.EACH)


@pytest.fixture
def apples():
    return Product("apples", ProductUnit.KILO)


@pytest.fixture
def catalog(toothbrush, toothpaste, apples):
    c = FakeCatalog()
    c.add_product(toothbrush, 0.99)
    c.add_product(toothpaste, 1.79)
    c.add_product(apples, 1.99)
    return c


@pytest.fixture
def teller(catalog):
    return Teller(catalog)


def checkout(teller, *compras):
    """compras = tuplas (produto, quantidade). Retorna o recibo."""
    cart = ShoppingCart()
    for produto, qtd in compras:
        cart.add_item_quantity(produto, qtd)
    return teller.checks_out_articles_from(cart)


def resumo_descontos(receipt):
    """Lista de (descricao, produto, valor) para facilitar os asserts."""
    return [(d.description, d.product.name, d.discount_amount) for d in receipt.discounts]


# --------------------------------------------------------------------------
# 1. Carrinho sem ofertas
# --------------------------------------------------------------------------
class TestCarrinhoSemOfertas:
    def test_carrinho_vazio(self, teller):
        receipt = checkout(teller)
        assert receipt.items == []
        assert receipt.discounts == []
        assert receipt.total_price() == 0

    def test_um_item_unitario(self, teller, toothbrush):
        receipt = checkout(teller, (toothbrush, 1.0))
        assert len(receipt.items) == 1
        item = receipt.items[0]
        assert item.product is toothbrush
        assert item.quantity == 1.0
        assert item.price == 0.99
        assert item.total_price == pytest.approx(0.99)
        assert receipt.total_price() == pytest.approx(0.99)

    def test_item_por_peso(self, teller, apples):
        receipt = checkout(teller, (apples, 2.5))
        assert receipt.items[0].total_price == pytest.approx(2.5 * 1.99)
        assert receipt.total_price() == pytest.approx(4.975)

    def test_varios_produtos_somam_total(self, teller, toothbrush, toothpaste, apples):
        receipt = checkout(teller, (toothbrush, 2.0), (toothpaste, 1.0), (apples, 0.5))
        esperado = 2 * 0.99 + 1.79 + 0.5 * 1.99
        assert len(receipt.items) == 3
        assert receipt.total_price() == pytest.approx(esperado)

    def test_add_item_adiciona_quantidade_1(self, teller, toothbrush):
        cart = ShoppingCart()
        cart.add_item(toothbrush)
        receipt = teller.checks_out_articles_from(cart)
        assert receipt.items[0].quantity == 1.0

    def test_mesmo_produto_duas_vezes_gera_duas_linhas(self, teller, toothbrush):
        # Contrato legado: cada add_item gera uma linha no recibo.
        receipt = checkout(teller, (toothbrush, 1.0), (toothbrush, 1.0))
        assert len(receipt.items) == 2
        assert receipt.total_price() == pytest.approx(1.98)

    def test_product_quantities_acumula_por_produto(self, toothbrush):
        cart = ShoppingCart()
        cart.add_item(toothbrush)
        cart.add_item_quantity(toothbrush, 2.0)
        assert cart.product_quantities[toothbrush] == 3.0
        assert len(cart.items) == 2

    def test_oferta_para_outro_produto_nao_afeta_carrinho(self, teller, toothbrush, apples):
        teller.add_special_offer(SpecialOfferType.TEN_PERCENT_DISCOUNT, toothbrush, 10.0)
        receipt = checkout(teller, (apples, 2.5))
        assert receipt.discounts == []
        assert receipt.total_price() == pytest.approx(4.975)

    def test_product_with_name(self, teller, toothbrush):
        assert teller.product_with_name("toothbrush") is toothbrush
        assert teller.product_with_name("inexistente") is None


# --------------------------------------------------------------------------
# 2. TEN_PERCENT_DISCOUNT
# --------------------------------------------------------------------------
class TestDezPorCento:
    def test_desconto_sobre_toda_a_quantidade(self, teller, apples):
        teller.add_special_offer(SpecialOfferType.TEN_PERCENT_DISCOUNT, apples, 10.0)
        receipt = checkout(teller, (apples, 2.0))
        (desc, nome, valor), = resumo_descontos(receipt)
        assert desc == "10.0% off"
        assert nome == "apples"
        assert valor == pytest.approx(-0.398)
        assert receipt.total_price() == pytest.approx(2 * 1.99 * 0.9)

    def test_argumento_inteiro_muda_descricao(self, teller, apples):
        # QUIRK: a descrição usa str(argumento): 10 -> "10% off", 10.0 -> "10.0% off"
        teller.add_special_offer(SpecialOfferType.TEN_PERCENT_DISCOUNT, apples, 10)
        receipt = checkout(teller, (apples, 1.0))
        assert receipt.discounts[0].description == "10% off"

    def test_percentual_diferente(self, teller, toothbrush):
        teller.add_special_offer(SpecialOfferType.TEN_PERCENT_DISCOUNT, toothbrush, 20.0)
        receipt = checkout(teller, (toothbrush, 1.0))
        assert receipt.discounts[0].description == "20.0% off"
        assert receipt.discounts[0].discount_amount == pytest.approx(-0.198)

    def test_desconto_aplica_a_um_unico_item(self, teller, toothbrush):
        teller.add_special_offer(SpecialOfferType.TEN_PERCENT_DISCOUNT, toothbrush, 10.0)
        receipt = checkout(teller, (toothbrush, 1.0))
        assert receipt.total_price() == pytest.approx(0.891)


# --------------------------------------------------------------------------
# 3. THREE_FOR_TWO
# --------------------------------------------------------------------------
class TestLeveTresPagueDois:
    @pytest.mark.parametrize("qtd", [1.0, 2.0])
    def test_abaixo_do_limite_sem_desconto(self, teller, toothbrush, qtd):
        teller.add_special_offer(SpecialOfferType.THREE_FOR_TWO, toothbrush, 0)
        receipt = checkout(teller, (toothbrush, qtd))
        assert receipt.discounts == []
        assert receipt.total_price() == pytest.approx(qtd * 0.99)

    def test_exatamente_tres(self, teller, toothbrush):
        teller.add_special_offer(SpecialOfferType.THREE_FOR_TWO, toothbrush, 0)
        receipt = checkout(teller, (toothbrush, 3.0))
        (desc, nome, valor), = resumo_descontos(receipt)
        assert desc == "3 for 2"
        assert nome == "toothbrush"
        assert valor == pytest.approx(-0.99)
        assert receipt.total_price() == pytest.approx(2 * 0.99)

    def test_quatro_itens_paga_um_extra(self, teller, toothbrush):
        teller.add_special_offer(SpecialOfferType.THREE_FOR_TWO, toothbrush, 0)
        receipt = checkout(teller, (toothbrush, 4.0))
        assert receipt.discounts[0].discount_amount == pytest.approx(-0.99)
        assert receipt.total_price() == pytest.approx(3 * 0.99)

    def test_seis_itens_dois_grupos(self, teller, toothbrush):
        teller.add_special_offer(SpecialOfferType.THREE_FOR_TWO, toothbrush, 0)
        receipt = checkout(teller, (toothbrush, 6.0))
        assert receipt.discounts[0].discount_amount == pytest.approx(-1.98)
        assert receipt.total_price() == pytest.approx(4 * 0.99)

    def test_quantidade_acumulada_em_linhas_separadas(self, teller, toothbrush):
        # 1 + 1 + 1 em chamadas separadas = 3 no carrinho => desconto aplica
        teller.add_special_offer(SpecialOfferType.THREE_FOR_TWO, toothbrush, 0)
        receipt = checkout(teller, (toothbrush, 1.0), (toothbrush, 1.0), (toothbrush, 1.0))
        assert len(receipt.items) == 3
        assert len(receipt.discounts) == 1
        assert receipt.total_price() == pytest.approx(2 * 0.99)

    def test_quirk_quantidade_fracionaria_abaixo_de_3_sem_desconto(self, teller, apples):
        # int(2.9) == 2 => não atinge o limite
        teller.add_special_offer(SpecialOfferType.THREE_FOR_TWO, apples, 0)
        receipt = checkout(teller, (apples, 2.9))
        assert receipt.discounts == []

    def test_quirk_quantidade_fracionaria_desconto_inclui_fracao(self, teller, apples):
        # 3.5 kg: desconto = 3.5*1.99 - (1*2*1.99 + 0) = 1.5 * 1.99
        teller.add_special_offer(SpecialOfferType.THREE_FOR_TWO, apples, 0)
        receipt = checkout(teller, (apples, 3.5))
        assert receipt.discounts[0].discount_amount == pytest.approx(-1.5 * 1.99)


# --------------------------------------------------------------------------
# 4. TWO_FOR_AMOUNT
# --------------------------------------------------------------------------
class TestDoisPorValor:
    def test_um_item_sem_desconto(self, teller, toothbrush):
        teller.add_special_offer(SpecialOfferType.TWO_FOR_AMOUNT, toothbrush, 1.5)
        receipt = checkout(teller, (toothbrush, 1.0))
        assert receipt.discounts == []

    def test_dois_itens(self, teller, toothbrush):
        teller.add_special_offer(SpecialOfferType.TWO_FOR_AMOUNT, toothbrush, 1.5)
        receipt = checkout(teller, (toothbrush, 2.0))
        (desc, nome, valor), = resumo_descontos(receipt)
        assert desc == "2 for 1.5"
        assert valor == pytest.approx(-(2 * 0.99 - 1.5))
        assert receipt.total_price() == pytest.approx(1.5)

    def test_quatro_itens_dois_grupos(self, teller, toothbrush):
        teller.add_special_offer(SpecialOfferType.TWO_FOR_AMOUNT, toothbrush, 1.5)
        receipt = checkout(teller, (toothbrush, 4.0))
        assert receipt.total_price() == pytest.approx(3.0)

    def test_quirk_tres_itens_usa_divisao_float(self, teller, toothbrush):
        # QUIRK: total = 1.5 * (3/2) + 1*0.99 = 3.24  (divisão float, não inteira).
        # O recibo cobra 3.24 por 3 itens que valem 2.97 => o "desconto" é POSITIVO.
        teller.add_special_offer(SpecialOfferType.TWO_FOR_AMOUNT, toothbrush, 1.5)
        receipt = checkout(teller, (toothbrush, 3.0))
        assert receipt.discounts[0].discount_amount == pytest.approx(+0.27)
        assert receipt.total_price() == pytest.approx(3.24)

    def test_quirk_cinco_itens_tambem_usa_divisao_float(self, teller, toothbrush):
        # total = 1.5 * (5/2) + 1*0.99 = 4.74 ; sem oferta seria 4.95
        teller.add_special_offer(SpecialOfferType.TWO_FOR_AMOUNT, toothbrush, 1.5)
        receipt = checkout(teller, (toothbrush, 5.0))
        assert receipt.total_price() == pytest.approx(4.74)


# --------------------------------------------------------------------------
# 5. FIVE_FOR_AMOUNT
# --------------------------------------------------------------------------
class TestCincoPorValor:
    @pytest.mark.parametrize("qtd", [1.0, 4.0])
    def test_abaixo_do_limite_sem_desconto(self, teller, toothbrush, qtd):
        teller.add_special_offer(SpecialOfferType.FIVE_FOR_AMOUNT, toothbrush, 4.0)
        receipt = checkout(teller, (toothbrush, qtd))
        assert receipt.discounts == []

    def test_exatamente_cinco(self, teller, toothbrush):
        teller.add_special_offer(SpecialOfferType.FIVE_FOR_AMOUNT, toothbrush, 4.0)
        receipt = checkout(teller, (toothbrush, 5.0))
        (desc, nome, valor), = resumo_descontos(receipt)
        assert desc == "5 for 4.0"
        assert valor == pytest.approx(-(5 * 0.99 - 4.0))
        assert receipt.total_price() == pytest.approx(4.0)

    def test_sete_itens_um_grupo_mais_dois_avulsos(self, teller, toothbrush):
        teller.add_special_offer(SpecialOfferType.FIVE_FOR_AMOUNT, toothbrush, 4.0)
        receipt = checkout(teller, (toothbrush, 7.0))
        assert receipt.total_price() == pytest.approx(4.0 + 2 * 0.99)

    def test_dez_itens_dois_grupos(self, teller, toothbrush):
        teller.add_special_offer(SpecialOfferType.FIVE_FOR_AMOUNT, toothbrush, 4.0)
        receipt = checkout(teller, (toothbrush, 10.0))
        assert receipt.total_price() == pytest.approx(8.0)


# --------------------------------------------------------------------------
# 6. Interação entre ofertas / carrinho com múltiplos produtos
# --------------------------------------------------------------------------
class TestInteracaoEntreOfertas:
    def test_ofertas_diferentes_em_produtos_diferentes(self, teller, toothbrush, toothpaste, apples):
        teller.add_special_offer(SpecialOfferType.THREE_FOR_TWO, toothbrush, 0)
        teller.add_special_offer(SpecialOfferType.TEN_PERCENT_DISCOUNT, apples, 10.0)
        receipt = checkout(teller, (toothbrush, 3.0), (toothpaste, 1.0), (apples, 1.0))
        assert len(receipt.discounts) == 2
        esperado = 2 * 0.99 + 1.79 + 1.99 * 0.9
        assert receipt.total_price() == pytest.approx(esperado)

    def test_ordem_dos_descontos_segue_ordem_de_insercao_no_carrinho(self, teller, toothbrush, apples):
        teller.add_special_offer(SpecialOfferType.THREE_FOR_TWO, toothbrush, 0)
        teller.add_special_offer(SpecialOfferType.TEN_PERCENT_DISCOUNT, apples, 10.0)
        r1 = checkout(teller, (apples, 1.0), (toothbrush, 3.0))
        r2 = checkout(teller, (toothbrush, 3.0), (apples, 1.0))
        assert [d.product.name for d in r1.discounts] == ["apples", "toothbrush"]
        assert [d.product.name for d in r2.discounts] == ["toothbrush", "apples"]

    def test_segunda_oferta_no_mesmo_produto_substitui_a_primeira(self, teller, toothbrush):
        # Contrato legado: no máximo UMA oferta por produto (a última cadastrada vence).
        teller.add_special_offer(SpecialOfferType.TEN_PERCENT_DISCOUNT, toothbrush, 10.0)
        teller.add_special_offer(SpecialOfferType.THREE_FOR_TWO, toothbrush, 0)
        receipt = checkout(teller, (toothbrush, 3.0))
        assert [d.description for d in receipt.discounts] == ["3 for 2"]

    def test_oferta_sem_produto_no_carrinho_nao_gera_desconto(self, teller, toothbrush, toothpaste):
        teller.add_special_offer(SpecialOfferType.THREE_FOR_TWO, toothbrush, 0)
        receipt = checkout(teller, (toothpaste, 3.0))
        assert receipt.discounts == []

    def test_ofertas_nao_alteram_itens_do_recibo(self, teller, toothbrush):
        teller.add_special_offer(SpecialOfferType.THREE_FOR_TWO, toothbrush, 0)
        receipt = checkout(teller, (toothbrush, 3.0))
        assert receipt.items[0].total_price == pytest.approx(0.99 * 3)


# --------------------------------------------------------------------------
# 7. Contrato da API pública
# --------------------------------------------------------------------------
class TestContratoPublico:
    def test_receipt_items_e_discounts_retornam_copias(self, teller, toothbrush):
        receipt = checkout(teller, (toothbrush, 1.0))
        receipt.items.clear()
        assert len(receipt.items) == 1

    def test_discount_amount_negativo_representa_abatimento(self, teller, toothbrush):
        teller.add_special_offer(SpecialOfferType.THREE_FOR_TWO, toothbrush, 0)
        receipt = checkout(teller, (toothbrush, 3.0))
        assert receipt.discounts[0].discount_amount < 0

    def test_enum_de_ofertas_existentes(self):
        assert {t.name for t in SpecialOfferType} >= {
            "THREE_FOR_TWO", "TEN_PERCENT_DISCOUNT", "TWO_FOR_AMOUNT", "FIVE_FOR_AMOUNT",
        }

    def test_handle_offers_recebe_receipt_offers_catalog(self, catalog, toothbrush):
        # Assinatura pública que a refatoração deve preservar.
        t = Teller(catalog)
        t.add_special_offer(SpecialOfferType.THREE_FOR_TWO, toothbrush, 0)
        cart = ShoppingCart()
        cart.add_item_quantity(toothbrush, 3.0)
        from receipt import Receipt
        receipt = Receipt()
        cart.handle_offers(receipt, t.offers, catalog)
        assert len(receipt.discounts) == 1


# --------------------------------------------------------------------------
# 8. Recibo impresso (texto exato, 40 colunas)
# --------------------------------------------------------------------------
class TestReciboImpresso:
    def test_recibo_sem_ofertas(self, teller, toothbrush, apples):
        # QUIRK: 2.5 * 1.99 = 4.975 (em float fica 4.97499...), então "%.2f" imprime 4.97
        receipt = checkout(teller, (toothbrush, 1.0), (apples, 2.5))
        texto = ReceiptPrinter().print_receipt(receipt)
        esperado = (
            "toothbrush                          0.99\n"
            "apples                              4.97\n"
            "  1.99 * 2.500\n"
            "\n"
            "Total:                              5.96\n"
        )
        assert texto == esperado

    def test_recibo_com_tres_por_dois(self, teller, toothbrush):
        teller.add_special_offer(SpecialOfferType.THREE_FOR_TWO, toothbrush, 0)
        receipt = checkout(teller, (toothbrush, 3.0))
        texto = ReceiptPrinter().print_receipt(receipt)
        esperado = (
            "toothbrush                          2.97\n"
            "  0.99 * 3.0\n"
            "3 for 2 (toothbrush)               -0.99\n"
            "\n"
            "Total:                              1.98\n"
        )
        assert texto == esperado

    def test_recibo_com_dez_por_cento(self, teller, apples):
        teller.add_special_offer(SpecialOfferType.TEN_PERCENT_DISCOUNT, apples, 10.0)
        receipt = checkout(teller, (apples, 2.0))
        texto = ReceiptPrinter().print_receipt(receipt)
        assert "10.0% off (apples)" in texto
        assert "-0.40" in texto
        assert texto.endswith("Total:                              3.58\n")

    def test_recibo_vazio(self):
        texto = ReceiptPrinter().print_receipt(Teller(FakeCatalog()).checks_out_articles_from(ShoppingCart()))
        assert texto == "\nTotal:                              0.00\n"

    def test_colunas_customizadas(self, teller, toothbrush):
        receipt = checkout(teller, (toothbrush, 1.0))
        texto = ReceiptPrinter(columns=20).print_receipt(receipt)
        assert texto.splitlines()[0] == "toothbrush      0.99"
