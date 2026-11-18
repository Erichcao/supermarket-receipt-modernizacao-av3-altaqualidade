import pytest

from promotions.promotion_factory import PromotionFactory


def test_rejeita_tipo_de_promocao_nao_suportado():
    with pytest.raises(ValueError, match="Tipo de promoção não suportado"):
        PromotionFactory.create_strategy("PROMOCAO_INVALIDA")