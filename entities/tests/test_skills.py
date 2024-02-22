import pytest
from entities.skills import Skills
from entities.fixtures import seller_1
from entities.fixtures import seller_2
from entities.fixtures import seller_4
from entities.hard_skills import HardSkills

class TestSkills:

    @pytest.mark.usefixtures("seller_1", "seller_2", "seller_4")
    @pytest.mark.parametrize(
        "seller, expected",
        [
            ("seller_1", [{
            "stack": "react",
            "endorsed_quantity": 7,
            "endorsed_by_others": 0,
            "endorsed_by_colleagues": 1,
            "endorsed_by_linkedin": 1
          },
          {
            "stack": "c#",
            "endorsed_quantity": 9,
            "endorsed_by_others": 1,
            "endorsed_by_colleagues": 1,
            "endorsed_by_linkedin": 0
          },
          {
            "stack": "java",
            "endorsed_quantity": 0,
            "endorsed_by_others": 0,
            "endorsed_by_colleagues": 0,
            "endorsed_by_linkedin": 0
          },
          {
            "stack": "s.o.l.i.d",
            "endorsed_quantity": 0,
            "endorsed_by_others": 0,
            "endorsed_by_colleagues": 0,
            "endorsed_by_linkedin": 0
          },
          {
            "stack": "ttd",
            "endorsed_quantity": 0,
            "endorsed_by_others": 0,
            "endorsed_by_colleagues": 0,
            "endorsed_by_linkedin": 0
          }]),
            ("seller_2", []),
            ("seller_4", [{
            "stack": "react",
            "endorsed_quantity": 7,
            "endorsed_by_others": 0,
            "endorsed_by_colleagues": 1,
            "endorsed_by_linkedin": 1
          }])
        ])
    def test_set_formated_skills(self, seller, expected, request):
        seller = request.getfixturevalue(seller)
        Skills.set_formated_skills(seller)
        result = seller.skills
        assert  result == expected

    @pytest.mark.usefixtures("seller_1", "seller_2", "seller_4")
    @pytest.mark.parametrize(
        "seller, expected",
        [
            ("seller_1", {
            'react': {
            "stack": "react",
            "endorsed_quantity": 7,
            "endorsed_by_others": 0,
            "endorsed_by_colleagues": 1,
            "endorsed_by_linkedin": 1
          }}),
            ("seller_2", {}),
            ("seller_4", {
            'react': {
            "stack": "react",
            "endorsed_quantity": 7,
            "endorsed_by_others": 0,
            "endorsed_by_colleagues": 1,
            "endorsed_by_linkedin": 1
          }})
        ])
    def test_get_skills_filtered_by_primary_stack(self, seller, expected, request):
        seller = request.getfixturevalue(seller)
        Skills.set_formated_skills(seller)
        Skills.get_skills_filtered_by_primary_stack(seller)
        result = seller._stacks_in_skills
        assert result == expected

    @pytest.mark.usefixtures("seller_1", "seller_2", "seller_4")
    @pytest.mark.parametrize(
        "seller, expected",
        [
            ("seller_1", 2),
            ("seller_2", 0),
            ("seller_4", 0),
        ])
    def test_get_hard_skills_in_skills(self, seller, expected, request):
        seller = request.getfixturevalue(seller)
        hard_skills = HardSkills()
        hard_skills.build(seller)
        Skills.set_formated_skills(seller)
        Skills.get_hard_skills_in_skills(seller, hard_skills)
        result = seller._hard_skills_quantity_in_skills
        assert result == expected