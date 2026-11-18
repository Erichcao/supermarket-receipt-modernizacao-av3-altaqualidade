
# Importa os tipos de promoção definidos no sistema legado.
from model_objects import SpecialOfferType

# Importa as estratégias concretas de promoção.
from promotions.ten_percent_discount import TenPercentDiscountStrategy
from promotions.three_for_two import ThreeForTwoStrategy
from promotions.two_for_amount import TwoForAmountStrategy
from promotions.five_for_amount import FiveForAmountStrategy


# Centraliza a criação das estratégias de promoção.
class PromotionFactory:

    # Cria e retorna a estratégia correspondente ao tipo informado.
    @staticmethod
    def create_strategy(offer_type):

        # Relaciona cada tipo de promoção à sua respectiva estratégia.
        strategies = {
            SpecialOfferType.TEN_PERCENT_DISCOUNT: TenPercentDiscountStrategy,
            SpecialOfferType.THREE_FOR_TWO: ThreeForTwoStrategy,
            SpecialOfferType.TWO_FOR_AMOUNT: TwoForAmountStrategy,
            SpecialOfferType.FIVE_FOR_AMOUNT: FiveForAmountStrategy,
        }

        # Procura a estratégia correspondente ao tipo recebido.
        strategy_class = strategies.get(offer_type)

        # Informa quando o tipo de promoção não possui estratégia cadastrada.
        if strategy_class is None:
            raise ValueError(
                f"Tipo de promoção não suportado: {offer_type}"
            )

        # Instancia e retorna a estratégia encontrada.
        return strategy_class()
