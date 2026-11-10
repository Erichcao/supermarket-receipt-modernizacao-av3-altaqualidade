
# Importa a interface comum das estratégias de promoção.
from promotions.promotion_strategy import PromotionStrategy

# Importa a classe responsável por representar os descontos.
from model_objects import Discount

# Importa math para calcular os grupos completos.
import math


# Implementa a promoção de três produtos pelo preço de dois.
class ThreeForTwoStrategy(PromotionStrategy):

    # Calcula o desconto considerando os grupos completos de três produtos.
    def calculate(self, product, quantity, unit_price, argument):

        # Converte a quantidade para inteiro, seguindo a regra legada.
        quantity_as_int = int(quantity)

        # Não cria desconto quando não existem três unidades.
        if quantity_as_int <= 2:
            return None

        # Calcula a quantidade de grupos completos de três produtos.
        number_of_groups = math.floor(quantity_as_int / 3)

        # Calcula o desconto preservando a fórmula original.
        discount_amount = quantity * unit_price - (
            (number_of_groups * 2 * unit_price)
            + quantity_as_int % 3 * unit_price
        )

        # Retorna o desconto com valor negativo, conforme o padrão legado.
        return Discount(
            product,
            "3 for 2",
            -discount_amount
        )
