# Importa a classe que representa os itens adicionados ao carrinho.
from model_objects import ProductQuantity, ProductUnit

# Importa a fábrica responsável por selecionar as estratégias individuais.
from promotions.promotion_factory import PromotionFactory

# Importa a estratégia responsável pelo cálculo dos combos.
from promotions.bundle_discount import BundleDiscountStrategy


class ShoppingCart:

    def __init__(self):
        self._items = []
        self._product_quantities = {}

    @property
    def items(self):
        return self._items

    def add_item(self, product):
        self.add_item_quantity(product, 1.0)

    @property
    def product_quantities(self):
        return self._product_quantities

    def add_item_quantity(self, product, quantity):
        self._items.append(ProductQuantity(product, quantity))

        if product in self._product_quantities.keys():
            self._product_quantities[product] += quantity
        else:
            self._product_quantities[product] = quantity

    def handle_offers(self, receipt, offers, catalog, bundle_offers=None):
        # Cria uma cópia das quantidades para controlar as unidades disponíveis.
        available_quantities = self._product_quantities.copy()

        # Utiliza uma lista vazia quando não existem combos cadastrados.
        if bundle_offers is None:
            bundle_offers = []

        # Cria a estratégia responsável pelo cálculo dos combos.
        bundle_strategy = BundleDiscountStrategy()

        # Percorre os combos cadastrados.
        for bundle_offer in bundle_offers:

            # Verifica se todos os produtos do combo são vendidos por unidade.
            if any(
                product.unit != ProductUnit.EACH
                for product in bundle_offer.products
            ):
                continue

            # Calcula o desconto e as quantidades reservadas pelo combo.
            discount, reserved_quantities = bundle_strategy.calculate(
                bundle_offer,
                available_quantities,
                catalog
            )

            # Registra o desconto quando existe um combo completo.
            if discount is not None:
                receipt.add_discount(discount)

                # Retira as unidades utilizadas dos produtos disponíveis.
                for product, quantity in reserved_quantities.items():
                    available_quantities[product] -= quantity

        # Percorre os produtos na mesma ordem em que foram acumulados.
        for product in self._product_quantities.keys():

            # Recupera somente a quantidade que não foi utilizada em combos.
            quantity = available_quantities[product]

            # Ignora produtos sem unidades disponíveis para outras promoções.
            if quantity <= 0:
                continue

            # Verifica se existe uma promoção individual cadastrada.
            if product in offers.keys():

                # Recupera a oferta associada ao produto.
                offer = offers[product]

                # Consulta o preço unitário no catálogo.
                unit_price = catalog.unit_price(product)

                # Solicita à fábrica a estratégia correspondente à promoção.
                strategy = PromotionFactory.create_strategy(offer.offer_type)

                # Calcula o desconto sobre as unidades restantes.
                discount = strategy.calculate(
                    product,
                    quantity,
                    unit_price,
                    offer.argument
                )

                # Adiciona o desconto somente quando a estratégia retorna um.
                if discount is not None:
                    receipt.add_discount(discount)
