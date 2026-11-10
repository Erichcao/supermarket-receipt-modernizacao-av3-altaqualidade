# Importa a classe que representa os itens adicionados ao carrinho.
from model_objects import ProductQuantity

# Importa a fábrica responsável por selecionar as estratégias de promoção.
from promotions.promotion_factory import PromotionFactory

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
            self._product_quantities[product] = self._product_quantities[product] + quantity
        else:
            self._product_quantities[product] = quantity


    def handle_offers(self, receipt, offers, catalog):
        # Percorre os produtos na mesma ordem em que foram acumulados no carrinho.
        for product in self._product_quantities.keys():

            # Recupera a quantidade total daquele produto.
            quantity = self._product_quantities[product]

            # Verifica se existe uma promoção cadastrada para o produto.
            if product in offers.keys():

                # Recupera a oferta associada ao produto.
                offer = offers[product]

                # Consulta o preço unitário no catálogo.
                unit_price = catalog.unit_price(product)

                # Solicita à fábrica a estratégia correspondente à promoção.
                strategy = PromotionFactory.create_strategy(offer.offer_type)

                # Delega o cálculo do desconto à estratégia selecionada.
                discount = strategy.calculate(
                    product,
                    quantity,
                    unit_price,
                    offer.argument
                )

                # Adiciona o desconto somente quando a estratégia retorna um.
                if discount is not None:
                    receipt.add_discount(discount)
