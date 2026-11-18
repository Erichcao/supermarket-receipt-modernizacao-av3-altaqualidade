
# Importa a interface comum das estratégias de promoção.
from promotions.promotion_strategy import PromotionStrategy

# Importa a classe responsável por representar os descontos.
from model_objects import Discount

# Importa math para calcular os grupos completos.
import math


# Implementa a promoção de cinco unidades por um valor fixo.
class FiveForAmountStrategy(PromotionStrategy):

    # Calcula o desconto considerando grupos completos de cinco unidades.
    def calculate(self, product, quantity, unit_price, argument):

        # Converte a quantidade para inteiro, seguindo a regra legada.
        quantity_as_int = int(quantity)

        # Calcula a quantidade de grupos completos de cinco produtos.
        number_of_groups = math.floor(quantity_as_int / 5)

        # Inicializa o desconto como inexistente.
        discount = None

        # A promoção só é aplicada a partir de cinco unidades.
        if quantity_as_int >= 5:

            # Calcula o valor total com a promoção e as unidades excedentes.
            total = (
                argument * number_of_groups
                + quantity_as_int % 5 * unit_price
            )

            # Calcula a diferença entre o preço normal e o promocional.
            discount_total = unit_price * quantity - total

            # Cria o desconto com valor negativo, conforme o padrão legado.
            discount = Discount(
                product,
                "5 for " + str(argument),
                -discount_total
            )

        # Retorna None quando não há quantidade suficiente para a promoção.
        return discount