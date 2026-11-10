
# Testes da funcionalidade de desconto por combos.
import pytest

from model_objects import Product, ProductUnit, SpecialOfferType
from shopping_cart import ShoppingCart
from teller import Teller
from tests.fake_catalog import FakeCatalog


# Cria os produtos utilizados nos testes.
@pytest.fixture
def toothbrush():
    return Product("toothbrush", ProductUnit.EACH)


@pytest.fixture
def toothpaste():
    return Product("toothpaste", ProductUnit.EACH)


# Prepara o catálogo com os preços dos produtos.
@pytest.fixture
def catalog(toothbrush, toothpaste):
    fake_catalog = FakeCatalog()
    fake_catalog.add_product(toothbrush, 0.99)
    fake_catalog.add_product(toothpaste, 1.79)
    return fake_catalog


# Inicializa o Teller utilizado nos testes.
@pytest.fixture
def teller(catalog):
    return Teller(catalog)


# Realiza uma compra e retorna o recibo.
def checkout(teller, *purchases):
    cart = ShoppingCart()

    for product, quantity in purchases:
        cart.add_item_quantity(product, quantity)

    return teller.checks_out_articles_from(cart)


class TestBundleDiscount:

    def test_aplica_desconto_em_um_combo_completo(
        self, teller, toothbrush, toothpaste
    ):
        # Cadastra um combo com uma escova e uma pasta.
        teller.add_bundle_offer(
            products=[toothbrush, toothpaste],
            discount_percentage=10
        )

        # Realiza a compra de um combo completo.
        receipt = checkout(
            teller,
            (toothbrush, 1),
            (toothpaste, 1)
        )

        # O desconto corresponde a 10% do valor dos dois produtos.
        assert sum(
            discount.discount_amount for discount in receipt.discounts
        ) == pytest.approx(-0.278)

        assert receipt.total_price() == pytest.approx(2.502)

    def test_aplica_desconto_em_dois_combos_completos(
        self, teller, toothbrush, toothpaste
    ):
        # Cadastra o combo com desconto de 10%.
        teller.add_bundle_offer(
            products=[toothbrush, toothpaste],
            discount_percentage=10
        )

        # Compra duas unidades de cada produto.
        receipt = checkout(
            teller,
            (toothbrush, 2),
            (toothpaste, 2)
        )

        # Cada combo concede R$ 0,278 de desconto.
        assert sum(
            discount.discount_amount for discount in receipt.discounts
        ) == pytest.approx(-0.556)

        assert receipt.total_price() == pytest.approx(5.004)

    def test_nao_aplica_desconto_em_combo_incompleto(
        self, teller, toothbrush, toothpaste
    ):
        # Cadastra o combo.
        teller.add_bundle_offer(
            products=[toothbrush, toothpaste],
            discount_percentage=10
        )

        # Compra apenas a escova, sem a pasta.
        receipt = checkout(
            teller,
            (toothbrush, 1)
        )

        # Não deve existir desconto de combo.
        assert receipt.discounts == []

        assert receipt.total_price() == pytest.approx(0.99)

    def test_unidades_excedentes_continuam_elegiveis_a_promocao_individual(
        self, teller, toothbrush, toothpaste
    ):
        # Cadastra um combo com desconto de 10%.
        teller.add_bundle_offer(
            products=[toothbrush, toothpaste],
            discount_percentage=10
        )

        # Cadastra a promoção individual de três por dois para escovas.
        teller.add_special_offer(
            SpecialOfferType.THREE_FOR_TWO,
            toothbrush,
            None
        )

        # Compra quatro escovas e uma pasta.
        # Uma escova e uma pasta formam o combo.
        # As três escovas restantes participam da promoção individual.
        receipt = checkout(
            teller,
            (toothbrush, 4),
            (toothpaste, 1)
        )

        # Desconto do combo: R$ 0,278.
        # Desconto de três por dois: R$ 0,99.
        assert sorted(
            discount.discount_amount for discount in receipt.discounts
        ) == pytest.approx([-0.99, -0.278])

        # Confere o total após os descontos do combo e da promoção individual.
        assert receipt.total_price() == pytest.approx(4.482)

    
    def test_produtos_vendidos_por_peso_nao_participam_de_combos(
        self, teller, toothbrush
    ):
        # Cria um produto vendido por peso.
        apples = Product("apples", ProductUnit.KILO)

        # Cadastra o produto no catálogo.
        teller.catalog.add_product(apples, 1.99)

        # Cadastra um combo com escova e maçã.
        teller.add_bundle_offer(
            products=[toothbrush, apples],
            discount_percentage=10
        )

        # Compra os dois produtos.
        receipt = checkout(
            teller,
            (toothbrush, 1),
            (apples, 1.0)
        )

        # Produtos vendidos por peso não devem formar combos.
        assert receipt.discounts == []

        # O total deve permanecer sem descontos.
        assert receipt.total_price() == pytest.approx(2.98)

    # Define percentuais e tipos de valores que devem ser rejeitados.
    @pytest.mark.parametrize(
        "discount_percentage",
        [-10, 0, 101, True, "10", None]
    )

    def test_rejeita_percentuais_de_desconto_invalidos(
        self, teller, toothbrush, toothpaste, discount_percentage
    ):
        # Tenta cadastrar um combo com percentual inválido.
        with pytest.raises(ValueError):
            teller.add_bundle_offer(
                products=[toothbrush, toothpaste],
                discount_percentage=discount_percentage
            )

    
    def test_combo_com_produto_repetido_exige_quantidade_correta(
        self, teller, toothbrush, toothpaste
    ):
        # Cadastra um combo que exige duas escovas e uma pasta.
        teller.add_bundle_offer(
            products=[toothbrush, toothbrush, toothpaste],
            discount_percentage=10
        )

        # Compra apenas uma escova e uma pasta.
        receipt = checkout(
            teller,
            (toothbrush, 1),
            (toothpaste, 1)
        )

        # Não deve existir desconto, pois falta uma escova.
        assert receipt.discounts == []

        # Compra duas escovas e uma pasta.
        receipt = checkout(
            teller,
            (toothbrush, 2),
            (toothpaste, 1)
        )

        # O desconto deve corresponder a 10% de R$ 3,77.
        assert sum(
            discount.discount_amount for discount in receipt.discounts
        ) == pytest.approx(-0.377)

        assert receipt.total_price() == pytest.approx(3.393)


    def test_aplica_dois_combos_diferentes_na_mesma_compra(
        self, teller, toothbrush, toothpaste
    ):
        # Cria um terceiro produto vendido por unidade.
        mouthwash = Product("mouthwash", ProductUnit.EACH)

        # Cadastra o terceiro produto no catálogo.
        teller.catalog.add_product(mouthwash, 2.00)

        # Cadastra o primeiro combo: escova + pasta.
        teller.add_bundle_offer(
            products=[toothbrush, toothpaste],
            discount_percentage=10
        )

        # Cadastra o segundo combo: pasta + enxaguante.
        teller.add_bundle_offer(
            products=[toothpaste, mouthwash],
            discount_percentage=10
        )

        # Compra os produtos necessários para os dois combos.
        receipt = checkout(
            teller,
            (toothbrush, 1),
            (toothpaste, 2),
            (mouthwash, 1)
        )

        # Confirma que os dois combos receberam desconto.
        assert len(receipt.discounts) == 2

        # Desconto do primeiro combo: R$ 0,278.
        # Desconto do segundo combo: R$ 0,379.
        assert sum(
            discount.discount_amount for discount in receipt.discounts
        ) == pytest.approx(-0.657)

        # Confere o total após os descontos dos dois combos.
        assert receipt.total_price() == pytest.approx(5.913)
