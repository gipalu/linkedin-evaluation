import pytest
from loguru import logger

from entities.key_words import KeyWords
from entities.fixtures import seller_1
from entities.fixtures import seller_2
from entities.fixtures import seller_4

class TestKeyWords:

    @pytest.mark.usefixtures("seller_1", "seller_2", "seller_4")
    @pytest.mark.parametrize(
        "seller, expected",
        [
            ("seller_1", {'leadership': 2, 'pleno': 0, 'senior': 2, 'technical_coordination': 0}),
            ("seller_2", {'leadership': 0, 'pleno': 0, 'senior': 0, 'technical_coordination': 0}),
            ("seller_4", {'leadership': 2, 'pleno': 0, 'senior': 1, 'technical_coordination': 0})
        ])
    def test_set_sellers_key_words_count(self, seller,expected, request):
        seller = request.getfixturevalue(seller)
        KeyWords.set_sellers_key_words_count(seller)
        result = seller._key_words_count
        assert result == expected

