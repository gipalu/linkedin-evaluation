import pytest
from entities.hard_skills import HardSkills
from entities.fixtures import seller_1
from entities.fixtures import seller_2
from entities.fixtures import seller_4

class TestHardSkills:

    @pytest.mark.usefixtures("seller_1", "seller_2")
    @pytest.mark.parametrize(
        "seller, expected",
        [
            ("seller_1", {'profile_title': 1, 'summary': 0}),
            ("seller_2", {'profile_title': 0, 'summary': 0})
        ])
    def test_get_hard_skills_in_summary_and_profile_title(self, seller, expected, request):
        seller = request.getfixturevalue(seller)
        hard_skills = HardSkills()
        hard_skills.build(seller)
        result = hard_skills.get_hard_skills_in_summary_and_profile_title(seller)
        assert result == expected

    @pytest.mark.usefixtures("seller_1", "seller_2", "seller_4")
    @pytest.mark.parametrize(
        "seller, expected",
        [
            ("seller_1", {'experiences_description': 0}),
            ("seller_2", {'experiences_description': 0}),
            ("seller_4", {'experiences_description': 0})
        ])
    def test_get_hard_skills_in_experiences(self, seller, expected, request):
        seller = request.getfixturevalue(seller)
        hard_skills = HardSkills()
        hard_skills.build(seller)
        result = hard_skills.get_hard_skills_in_experiences(seller)
        assert result == expected

    @pytest.mark.usefixtures("seller_1", "seller_2", "seller_4")
    @pytest.mark.parametrize(
        "seller, expected",
        [
            ("seller_1", {'profile_title': 1, 'summary': 0, 'experiences_description': 0}),
            ("seller_2", {'profile_title': 0, 'summary': 0, 'experiences_description': 0}),
            ("seller_4", {'profile_title': 1, 'summary': 0, 'experiences_description': 0})
        ])
    def test_join_fields(self, seller, expected, request):
        seller = request.getfixturevalue(seller)
        hard_skills = HardSkills()
        hard_skills.build(seller)
        hard_skills.join_fields(seller)
        result = seller._hard_skills_quantity_in_fields
        assert  result == expected