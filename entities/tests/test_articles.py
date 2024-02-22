import pytest

from entities.articles import Articles
from entities.fixtures import seller_1
from entities.fixtures import seller_2

class TestArticles:

    @pytest.mark.usefixtures("seller_1", "seller_2")
    @pytest.mark.parametrize(
            "seller, expected",
            [
                ("seller_1", 2),
                ("seller_2", 0)
            ])
    def test_get_articles_number(self, seller, expected, request):
        seller = request.getfixturevalue(seller)
        Articles.get_articles_number(seller)
        result = seller._articles_quantity
        assert result == expected
