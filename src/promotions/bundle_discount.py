# Importa Counter para contar os produtos necessários em cada combo.
from collections import Counter
from model_objects import Discount, Product, ProductUnit


class BundleOffer:
    """Representa uma oferta composta por vários produtos."""

    def __init__(self, products, discount_percentage):
        # Verifica se o percentual é numérico e está entre 0 e 100.
        if (
            isinstance(discount_percentage, bool)
            or not isinstance(discount_percentage, (int, float))
            or not 0 < discount_percentage <= 100
        ):
            raise ValueError(
                "O percentual de desconto deve ser maior que 0 e menor ou igual a 100."
            )

        # Armazena os produtos que formam o combo.
        self.products = list(products)

        # Armazena o percentual de desconto validado.
        self.discount_percentage = discount_percentage


class BundleDiscountStrategy:
    """Calcula o desconto dos combos completos."""

    def calculate(self, offer, product_quantities, catalog):
        # Conta quantas unidades de cada produto são necessárias por combo.
        required_quantities = Counter(offer.products)

        # Impede a criação de combos sem produtos.
        if not required_quantities:
            return None, {}

        # Calcula quantos combos completos podem ser formados.
        number_of_bundles = min(
            int(product_quantities.get(product, 0) // required_quantity)
            for product, required_quantity in required_quantities.items()
        )

        # Não concede desconto quando não existe combo completo.
        if number_of_bundles <= 0:
            return None, {}

        # Calcula o valor total dos produtos utilizados nos combos.
        bundle_total = sum(
            catalog.unit_price(product) * required_quantity
            for product, required_quantity in required_quantities.items()
        )

        # Considera a quantidade de combos completos encontrados.
        bundle_total *= number_of_bundles

        # Calcula o desconto percentual sobre o valor dos combos.
        discount_amount = (
            bundle_total * offer.discount_percentage / 100
        )

        # Cria um nome que identifica todos os produtos do combo.
        bundle_name = " + ".join(
            product.name for product in offer.products
        )

        # Cria um produto representativo para identificar o combo no recibo.
        bundle_product = Product(
            f"Combo: {bundle_name}",
            ProductUnit.EACH
        )

        # Cria o desconto com valor negativo para reduzir o total.
        discount = Discount(
            bundle_product,
            f"{offer.discount_percentage}% off combo",
            -discount_amount
        )

        # Registra as quantidades reservadas para os combos completos.
        reserved_quantities = {
            product: required_quantity * number_of_bundles
            for product, required_quantity in required_quantities.items()
        }

        # Retorna o desconto e as quantidades que não poderão receber
        # outras promoções individuais.
        return discount, reserved_quantities
