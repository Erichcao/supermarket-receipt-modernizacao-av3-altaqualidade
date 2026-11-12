from model_objects import Offer
from receipt import Receipt
# Importa as classes responsáveis pelas ofertas de combos.
from promotions.bundle_discount import BundleOffer


class Teller:

    def __init__(self, catalog):
        self.catalog = catalog
        self.offers = {}
        # Armazena separadamente as ofertas de combos.
        self.bundle_offers = []

    def add_special_offer(self, offer_type, product, argument):
        self.offers[product] = Offer(offer_type, product, argument)

    def add_bundle_offer(self, products, discount_percentage):
        # Cria uma oferta de combo com os produtos e o percentual informado.
        bundle_offer = BundleOffer(products, discount_percentage)

        # Armazena o combo para aplicação durante o checkout.
        self.bundle_offers.append(bundle_offer)

    def checks_out_articles_from(self, the_cart):
        receipt = Receipt()
        product_quantities = the_cart.items
        for pq in product_quantities:
            p = pq.product
            quantity = pq.quantity
            unit_price = self.catalog.unit_price(p)
            price = quantity * unit_price
            receipt.add_product(p, quantity, unit_price, price)

        # Aplica os combos e as promoções individuais durante o checkout.
        the_cart.handle_offers(
            receipt,
            self.offers,
            self.catalog,
            self.bundle_offers
        )

        return receipt

    def product_with_name(self, name):
        return self.catalog.products.get(name, None)
