import pytest
from entities.summary import Summary
from entities.fixtures import seller_1
from entities.fixtures import seller_2

class TestSummary:

    @pytest.mark.usefixtures("seller_1", "seller_2")
    @pytest.mark.parametrize(
        "seller, expected",
        [
            ("seller_1", 817),
            ("seller_2", 0)
        ])
    def test_summary_size(self, seller, expected, request):
        seller = request.getfixturevalue(seller)
        Summary.summary_size(seller)
        result = seller._summary_size
        assert result == expected
