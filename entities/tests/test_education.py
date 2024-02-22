import pytest
from entities.education import Education
from entities.fixtures import seller_1
from entities.fixtures import seller_2
from entities.fixtures import seller_4


class TestEducation:

    @pytest.mark.usefixtures("seller_1", "seller_2", "seller_4")
    @pytest.mark.parametrize(
            "seller, expected",
            [
                ("seller_1", 1),
                ("seller_2", 0),
                ("seller_4", 1)
            ])
    def test_get_valid_education(self, seller, expected, request):
        seller = request.getfixturevalue(seller)
        Education.get_valid_education(seller)
        result = seller._education_validity
        assert result == expected