import pytest
from entities.recommendations import Recommendations
from entities.fixtures import seller_1
from entities.fixtures import seller_2
from entities.fixtures import seller_4

class TestRecommendations:

    @pytest.mark.usefixtures("seller_1", "seller_2", "seller_4")
    @pytest.mark.parametrize(
        "seller, expected",
        [
            ("seller_1", 8),
            ("seller_2", 0),
            ("seller_4", 1)
        ])
    def test_get_recommendations_quantity(self, seller, expected, request):
        seller = request.getfixturevalue(seller)
        Recommendations.set_recommendations_quantity(seller)
        result = seller._recommendations_quantity
        assert result == expected

    @pytest.mark.usefixtures("seller_1", "seller_2", "seller_4")
    @pytest.mark.parametrize(
        "seller, expected",
        [
            ("seller_1", 0.875),
            ("seller_2", 0),
            ("seller_4", 1),
        ])
    def test_set_recommendations_size(self, seller, expected, request):
        seller = request.getfixturevalue(seller)
        Recommendations.set_recommendations_size(seller)
        result = seller._percent_recommendations_right_size
        assert result == expected

    @pytest.mark.usefixtures("seller_1", "seller_2", "seller_4")
    @pytest.mark.parametrize(
        "seller, expected",
        [
            ("seller_1", 1),
            ("seller_2", 1),
            ("seller_2", 1),
        ])
    def test_compare_recommendations_received_and_sent(self, seller,expected, request):
        seller = request.getfixturevalue(seller)
        Recommendations.compare_recommendations_received_and_sent(seller)
        result = seller._recommendations_multiplier
        assert result == expected