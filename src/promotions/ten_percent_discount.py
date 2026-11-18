
# Importa a classe abstrata que define a interface das promoções.
from promotions.promotion_strategy import PromotionStrategy

# Importa a classe Discount, responsável por representar um desconto.
from model_objects import Discount


# Implementa a estratégia de desconto percentual.
class TenPercentDiscountStrategy(PromotionStrategy):

    # Calcula o desconto percentual aplicado à quantidade comprada.
    def calculate(self, product, quantity, unit_price, argument):

        # Calcula o valor total dos produtos antes do desconto.
        total = quantity * unit_price

        # Calcula o valor do desconto com base no percentual informado.
        discount_amount = total * argument / 100.0

        # Retorna o desconto com valor negativo, conforme o padrão legado.
        return Discount(
            product,
            str(argument) + "% off",
            -discount_amount
        )
