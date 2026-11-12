
# Define a interface comum para as estratégias de promoção.
# As subclasses devem implementar o método calculate.
from abc import ABC, abstractmethod


class PromotionStrategy(ABC):

    @abstractmethod
    def calculate(self, product, quantity, unit_price, argument):
        """Calcula o desconto de acordo com a estratégia."""
        pass
