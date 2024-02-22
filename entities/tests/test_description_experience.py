import pytest
from entities.description_experience import DescriptionExperience
from entities.fixtures import seller_1
from entities.fixtures import seller_2
from entities.fixtures import seller_4

class TestDescriptionExperience:

    @pytest.mark.usefixtures("seller_1", "seller_2", "seller_4")
    @pytest.mark.parametrize(
            "seller, expected",
            [
                ("seller_1", 1),
                ("seller_2", 0),
                ("seller_4", 1)
            ])
    def test_set_description_experience_size(self, seller, expected, request):
        seller = request.getfixturevalue(seller)
        DescriptionExperience.set_description_experience_size(seller)
        result = seller._percent_description_experience_size
        assert result == expected

    @pytest.mark.usefixtures("seller_1", "seller_2", "seller_4")
    @pytest.mark.parametrize(
            "seller, expected",
            [
                ("seller_1", 160),
                ("seller_2", 0),
                ("seller_4", 160)
            ])
    def test_set_last_experience_size(self,  seller, expected, request):
        seller = request.getfixturevalue(seller)
        DescriptionExperience.set_last_experience_size(seller)
        result = seller._last_description_experience_size
        assert result == expected
