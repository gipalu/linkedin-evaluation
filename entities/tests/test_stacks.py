import pytest
from entities.stacks import Stacks
from entities.fixtures import seller_1
from entities.fixtures import seller_2
from entities.fixtures import seller_4
from entities.experience import Experience

class TestStacks:

    @pytest.mark.parametrize(
        "field, expected",
        [
            ('Trabalho com react, react native além de node.js', {
                'Angular': 0,
                'C#/.Net': 0,
                'Node': 1,
                'React': 2,
                'React Native': 1,
                'Vue':0}),
            ('trabalho com REACT react E NODE', {
                'Angular': 0,
                'C#/.Net': 0,
                'Node': 1,
                'React': 2,
                'React Native': 0,
                'Vue':0}),
            ('trabalho com C#/.Net, .net, DOT NET', {
                'Angular': 0,
                'C#/.Net': 3,
                'Node': 0,
                'React': 0,
                'React Native': 0,
                'Vue':0}),
            ('', {
                'Angular': 0,
                'C#/.Net': 0,
                'Node': 0,
                'React': 0,
                'React Native': 0,
                'Vue': 0}),
        ]
        )
    def test_check_stacks_in_field(self, field, expected):
        result = Stacks.check_stacks_in_field(field)
        assert result == expected

    @pytest.mark.usefixtures("seller_1", "seller_2", "seller_4")
    @pytest.mark.parametrize(
        "seller, expected",
        [
            ("seller_1", {
                        'React': [{'time_experience': 457,
                         'stack': 'React'
                         }]}),
            ("seller_2", {}),
            ("seller_4", {
                        'React': [{'time_experience': 457,
                         'stack': 'React'
                         }]})
        ])
    def test_check_if_stack_exists_in_experience(self, seller, expected, request):
        seller = request.getfixturevalue(seller)
        Experience.set_experience(seller)
        Experience.title_validity(seller)
        result = Stacks.check_if_stack_exists_in_experience(seller)
        assert result == expected

    @pytest.mark.usefixtures("seller_1", "seller_2", "seller_4")
    @pytest.mark.parametrize(
            "seller, expected",
            [
                ("seller_1", [
                    {'stack': 'C#/.Net', 'time_experience_with_stack': 0.0},
                    {'stack': 'React', 'time_experience_with_stack': 0.682089552238806}]),
                ("seller_2", [
                    {'stack': 'C#/.Net', 'time_experience_with_stack': 0},
                    {'stack': 'React', 'time_experience_with_stack': 0}]),
                ("seller_4", [
                    {'stack': 'C#/.Net', 'time_experience_with_stack': 0.0},
                    {'stack': 'React', 'time_experience_with_stack': 1}])
            ])
    def test_get_percent_of_time_experience_with_each_stack(self, seller, expected, request):
        seller = request.getfixturevalue(seller)
        Experience.set_experience(seller)
        Experience.title_validity(seller)
        result = Stacks.get_percent_of_time_experience_with_each_stack(seller)
        assert result == expected

    @pytest.mark.usefixtures("seller_1", "seller_2", "seller_4")
    @pytest.mark.parametrize(
            "seller, expected",
            [
                ("seller_1", 0.682089552238806/2),
                ("seller_2", 0),
                ("seller_4", 0.5)
            ])
    def test_get_percent_of_time_experience_with_primary_stack(self, seller, expected, request):
        seller = request.getfixturevalue(seller)
        Experience.set_experience(seller)
        Experience.title_validity(seller)
        Stacks.get_percent_of_time_experience_with_primary_stack(seller)
        result = seller._percent_primary_stacks_in_experiences
        assert result == expected

    @pytest.mark.usefixtures("seller_1", "seller_2")
    @pytest.mark.parametrize(
        "seller, expected",
        [
            ("seller_1", {'C#/.Net': 0, 'React': 1}),
            ("seller_2", {'C#/.Net': 0, 'React': 0})
        ])
    def test_get_primary_stack_in_profile_title(self, seller, expected, request):
        seller = request.getfixturevalue(seller)
        Stacks.get_stack_in_profile_title(seller)
        result = seller._primary_stacks_in_profile_title
        assert result == expected

    @pytest.mark.usefixtures("seller_1", "seller_2")
    @pytest.mark.parametrize(
        "seller, expected",
        [
            ("seller_1", {'C#/.Net': 0, 'React': 0}),
            ("seller_2", {'C#/.Net': 0, 'React': 0})
        ])
    def test_get_primary_stack_in_summary(self, seller, expected, request):
        seller = request.getfixturevalue(seller)
        Stacks.get_stack_in_summary(seller)
        result = seller._primary_stacks_in_summary
        assert result == expected
