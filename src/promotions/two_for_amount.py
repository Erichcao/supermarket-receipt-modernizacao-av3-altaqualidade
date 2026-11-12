
# Importa a interface comum das estratégias de promoção.
from promotions.promotion_strategy import PromotionStrategy

# Importa a classe responsável por representar os descontos.
from model_objects import Discount


# Implementa a promoção de duas unidades por um valor fixo.
class TwoForAmountStrategy(PromotionStrategy):

    # Calcula o desconto considerando os pares completos de produtos.
    def calculate(self, product, quantity, unit_price, argument):

        # Converte a quantidade para inteiro, seguindo a regra legada.
        quantity_as_int = int(quantity)

        # Inicializa o desconto como inexistente.
        discount = None

        # A promoção só é aplicada quando existem pelo menos duas unidades.
        if quantity_as_int >= 2:

            # Calcula o valor dos pares pelo preço promocional.
            # A divisão por 2.0 preserva o comportamento original.
            total = argument * (quantity_as_int / 2.0) + (
                quantity_as_int % 2 * unit_price
            )

            # Calcula a diferença entre o preço normal e o promocional.
            discount_amount = unit_price * quantity - total

            # Cria o desconto com valor negativo, conforme o padrão legado.
            discount = Discount(
                product,
                "2 for " + str(argument),
                -discount_amount
            )

        # Retorna None quando não há quantidade suficiente para a promoção.
        return discount