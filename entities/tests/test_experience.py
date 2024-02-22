import copy
import pytest

from entities.fixtures import seller_3
from entities.fixtures import seller_2
from entities.fixtures import seller_1
from entities.fixtures import seller_4
from entities.experience import Experience
from entities.loader import loader
from entities.seller import Seller

class TestExperience:
    def test_date_name_to_int_return_mapping(self):
        valid_date_list = ['fev', 'de', '2022']
        expected_date_list = [2, 'de', '2022']

        result = Experience.date_name_to_int(valid_date_list)

        assert result == expected_date_list

    def test_transform_date_len_three(self):
        valid_date_list = "nov de 2008 "
        expected_date_dict = {
            'day': 1,
            'month': 11,
            'year': 2008
        }

        result = Experience.transform_date(valid_date_list)

        assert result == expected_date_dict

    def test_transform_date_len_two(self):
        valid_date_list = " o momento "
        expected_result = None

        result = Experience.transform_date(valid_date_list)

        assert result == expected_result

    def test_transform_date_len_one(self):
        valid_date_list = "2018"
        expected_date_dict = {
            'day': 1,
            'month': 1,
            'year': 2018
        }

        result = Experience.transform_date(valid_date_list)

        assert result == expected_date_dict

    @pytest.mark.usefixtures("seller_1", "seller_2", "seller_4")
    @pytest.mark.parametrize(
            "seller, expected",
            [
                ("seller_1", [{
                    'userId': '6250bfa19c17cf7ae989c41d',
                    'level': 8,
                    'startDate': '2020-06-01',
                    'endDate': '2021-09-01',
                    'title': 'Tech Lead',
                    'description': 'Promote technical improvements and restructuring the Educational Technology team, and supporting/developing front-end with Vue and Back with Node and PHP, react'},
                    {'userId': '6250bfa19c17cf7ae989c41d',
                    'level': 8,
                    'startDate': '2019-11-01',
                    'endDate': '2020-06-01',
                    'title': 'Specialist Developer',
                    'description': '-development of internal platforms for fleet control, tracking and registration of vehicles and drivers with vue, typescript, sass and node- singluar and recurring billing system for subscriptions with vue, nuxt and node- control of sensitive information and data from datalake- structuring services and endpoints with graphql, express and node'}]),
                ("seller_2", [{
                    'userId': '6250bfa19c17cf7ae989c41d',
                    'level': 8,
                    'startDate': 0,
                    'endDate': 0,
                    'title': 0,
                    'description': ''}]),
                ("seller_4", [{
                    'userId': '6250bfa19c17cf7ae989c41d',
                    'level': 8,
                    'startDate': '2020-06-01',
                    'endDate': '2021-09-01',
                    'title': 'Tech Lead',
                    'description': 'Promote technical improvements and restructuring the Educational Technology team, and supporting/developing front-end with Vue and Back with Node and PHP, react'}])
            ])
    def test_set_experience(self, seller, expected, request):
        seller = request.getfixturevalue(seller)
        Experience.set_experience(seller)
        assert expected == seller.experiences

    @pytest.mark.usefixtures("seller_1", "seller_2", "seller_4")
    @pytest.mark.parametrize(
            "seller, expected",
            [
                ("seller_1", [{
                    'userId': '6250bfa19c17cf7ae989c41d',
                    'level': 8,
                    'startDate': '2020-06-01',
                    'endDate': '2021-09-01',
                    'title': 'Tech Lead',
                    'description': 'Promote technical improvements and restructuring the Educational Technology team, and supporting/developing front-end with Vue and Back with Node and PHP, react'
                },
                {
                    'userId': '6250bfa19c17cf7ae989c41d',
                    'level': 8,
                    'startDate': '2019-11-01',
                    'endDate': '2020-06-01',
                    'title': 'Specialist Developer',
                    'description': '-development of internal platforms for fleet control, tracking and registration of vehicles and drivers with vue, typescript, sass and node- singluar and recurring billing system for subscriptions with vue, nuxt and node- control of sensitive information and data from datalake- structuring services and endpoints with graphql, express and node'
                }]),
                ("seller_2", []),
                ("seller_4", [{
                    'userId': '6250bfa19c17cf7ae989c41d',
                    'level': 8,
                    'startDate': '2020-06-01',
                    'endDate': '2021-09-01',
                    'title': 'Tech Lead',
                    'description': 'Promote technical improvements and restructuring the Educational Technology team, and supporting/developing front-end with Vue and Back with Node and PHP, react'
                }])
            ])
    def test_invalid_titles(self, seller, expected, request):
        seller = request.getfixturevalue(seller)
        Experience.set_experience(seller)
        Experience.title_validity(seller)
        assert expected == seller.experiences


    def test_overlap_two_intervals_with_overlap(self):
        exp = {'userId': '6250bfa19c17cf7ae989c41d',
               'level': 8,
               'startDate': '2021-11-01',
               'endDate': '2021-11-30',
               'title': 'Tech Lead',
               'description': 'Promote technical improvements and restructuring the Educational Technology team, and supporting/developing front-end with Vue and Back with Node and PHP, react'
        }
        exp_ref = {'userId': '6250bfa19c17cf7ae989c41d',
                   'level': 8,
                   'startDate': '2021-11-20',
                   'endDate': '2021-12-10',
                   'title': 'Specialist Developer',
                   'description': 'Promote technical improvements and restructuring the Educational Technology team, and supporting/developing front-end with Vue and Back with Node and PHP, react'
        }
        result = Experience.overlap_two_intervals(exp, exp_ref)
        valid_result = 11
        assert result == valid_result

    def test_overlap_two_intervals_without_overlap(self):
        exp = {'userId': '6250bfa19c17cf7ae989c41d',
               'level': 8,
               'startDate': '2021-11-01',
               'endDate': '2021-11-30',
               'title': 'Tech Lead',
               'description': 'Promote technical improvements and restructuring the Educational Technology team, and supporting/developing front-end with Vue and Back with Node and PHP, react'
        }
        exp_ref = {'userId': '6250bfa19c17cf7ae989c41d',
                   'level': 8,
                   'startDate': '2021-12-01',
                   'endDate': '2021-12-10',
                   'title': 'Specialist Developer',
                   'description': 'Promote technical improvements and restructuring the Educational Technology team, and supporting/developing front-end with Vue and Back with Node and PHP, react'
                   }
        result = Experience.overlap_two_intervals(exp, exp_ref)
        valid_result = 0
        assert result == valid_result

    @pytest.mark.usefixtures("seller_3", "seller_2", "seller_4")
    @pytest.mark.parametrize(
        "seller, expected",
        [
            ("seller_3", 10),
            ("seller_2", 0),
            ("seller_4", 0)
        ])
    def test_get_total_intersection_with_overlap(self, seller, expected, request):
        seller = request.getfixturevalue(seller)
        seller.buffer = copy.deepcopy(seller.experiences)
        result = Experience.get_total_intersection(seller)
        assert result == expected

    @pytest.mark.usefixtures("seller_1")
    @pytest.mark.parametrize(
        "seller, expected",
        [
            ("seller_1", 457)
        ])
    def test_delta_experience_time(self, seller, expected, request):
        seller = request.getfixturevalue(seller)
        Experience.set_experience(seller)
        Experience.title_validity(seller)
        experience = seller.experiences[0]
        result = Experience.delta_experience_time(experience)
        assert result == expected

    @pytest.mark.usefixtures("seller_3", "seller_2")
    @pytest.mark.parametrize(
        "seller, expected",
        [
            ("seller_3", 668/365),
            ("seller_2", 0)
        ])
    def test_set_experiences_time(self, seller, expected, request):
        seller = request.getfixturevalue(seller)
        Experience.set_experiences_time(seller)
        result = seller._total_valid_experience_time
        assert result == expected

    @pytest.mark.usefixtures("seller_1", "seller_2", "seller_4")
    @pytest.mark.parametrize(
        "seller, expected",
        [
            ("seller_1", 457),
            ("seller_2", 0),
            ("seller_4", 457)
        ])
    def test_get_latest_experience_time(self, seller, expected, request):
        seller = request.getfixturevalue(seller)
        Experience.set_experience(seller)
        Experience.title_validity(seller)
        Experience.latest_experience_time(seller)
        result = seller._latest_experience_time
        assert result == expected

    @pytest.mark.usefixtures("seller_1", "seller_2", "seller_4")
    @pytest.mark.parametrize(
        "seller, expected",
        [
            ("seller_1", 213),
            ("seller_2", 0),
            ("seller_4", 0)
        ])
    def test_get_previous_experience_time(self, seller, expected, request):
        seller = request.getfixturevalue(seller)
        Experience.set_experience(seller)
        Experience.title_validity(seller)
        Experience.previous_experience_time(seller)
        result = seller._previous_experience_time
        assert result == expected

    @pytest.mark.usefixtures("seller_1", "seller_2", "seller_4")
    @pytest.mark.parametrize(
        "seller, expected",
        [
            ("seller_1", 0.5),
            ("seller_2", 0),
            ("seller_4", 1)
        ])
    def test_percent_valid_experience_between_jobs(self, seller, expected, request):
        seller = request.getfixturevalue(seller)
        Experience.set_experience(seller)
        Experience.title_validity(seller)
        Experience.percent_valid_experience_between_jobs(seller)
        result = seller._percent_experiences_between_jobs
        assert result == expected

    @pytest.mark.usefixtures("seller_1", "seller_2", "seller_4")
    @pytest.mark.parametrize(
        "seller, expected",
        [
            ("seller_1", 670),
            ("seller_2", 0),
            ("seller_4", 457),
        ])
    def test_get_total_experience_time_with_overlap(self, seller, expected, request):
        seller = request.getfixturevalue(seller)
        Experience.set_experience(seller)
        Experience.title_validity(seller)
        Experience.percent_valid_experience_between_jobs(seller)
        result = Experience.get_total_experience_time_with_overlap(seller)
        assert result == expected

