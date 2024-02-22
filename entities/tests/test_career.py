import pytest

from entities.career import Career
from entities.experience import Experience
from entities.fixtures import seller_1, seller_2, seller_4, seller_5, seller_6
from entities.description_classification import DescriptionClassification

class TestCareer:
    @pytest.fixture
    def model_career(self):
        """
        :return: model for predict career
        """
        model = DescriptionClassification()
        model.load_career_classification_model()
        model.load_desc_validation_model()
        return model

    @pytest.mark.parametrize(
        "text, expected",
        [
            ({
                "backend": 0,
                "frontend": 0,
                "fullstack": 1,
                "mobile_fullstack": 0,
                "mobile": 0,
                "indefinido": 0
            },{
                "backend": 1,
                "frontend": 1,
                "fullstack": 1,
                "mobile_fullstack": 0,
                "mobile": 0,
                "indefinido": 0
            }),
            ({
                "backend": 0,
                "frontend": 1,
                "fullstack": 0,
                "mobile_fullstack": 0,
                "mobile": 0,
                "indefinido": 0
            },
             {
                 "backend": 0,
                 "frontend": 1,
                 "fullstack": 0,
                 "mobile_fullstack": 0,
                 "mobile": 0,
                 "indefinido": 0
             }),
        ])
    def test_career_equivalence(self, text, expected):
        result = Career.careers_equivalence(text)
        assert result == expected

    @pytest.mark.parametrize(
        "text, expected",
        [
            ({
                "backend": 0,
                "frontend": 0,
                "fullstack": 1,
                "mobile_fullstack": 1,
                "mobile": 1,
            },{
                "backend": 0,
                "frontend": 0,
                "fullstack": 0,
                "mobile_fullstack": 1,
                "mobile": 0,
            }),
            ({
                "backend": 1,
                "frontend": 1,
                "fullstack": 0,
                "mobile_fullstack": 0,
                "mobile": 0,
            },
             {
                 "backend": 0,
                 "frontend": 0,
                 "fullstack": 1,
                 "mobile_fullstack": 0,
                 "mobile": 0,
             }),
        ])
    def test_delete_career_duplicates(self, text, expected):
        result = Career.delete_career_duplicates(text)
        assert result == expected

    @pytest.mark.usefixtures("seller_1", "seller_4", "seller_5")
    @pytest.mark.parametrize(
            "seller, expected",
            [
                ("seller_1", {
                    'frontend': 0,
                    'backend': 0,
                    'fullstack': 0,
                    'mobile_fullstack': 0,
                    'mobile': 0
                }),
                ("seller_4", {
                    'frontend': 0,
                    'backend': 0,
                    'fullstack': 0,
                    'mobile_fullstack': 0,
                    'mobile': 0
                }),
                ("seller_5", {
                    'frontend': 0,
                    'backend': 1,
                    'fullstack': 0,
                    'mobile_fullstack': 0,
                    'mobile': 0
                })
            ])
    def test_verify_exist_career_in_title(self, seller, expected, request):
        seller = request.getfixturevalue(seller)
        Experience.set_experience(seller)
        Experience.title_validity(seller)
        exp = seller.experiences[0]
        result = Career.verify_exist_career_in_title(exp)
        assert result == expected

    @pytest.mark.usefixtures("seller_1", "seller_4", "seller_5")
    @pytest.mark.parametrize(
            "seller, expected",
            [
                ("seller_1", {
                    "backend": 0,
                    "frontend": 0,
                    "fullstack": 1,
                    "mobile_fullstack": 0,
                    "mobile": 0,
                    "indefinido": 0
                }
                ),
                ("seller_4", {
                    "backend": 0,
                    "frontend": 0,
                    "fullstack": 1,
                    "mobile_fullstack": 0,
                    "mobile": 0,
                    "indefinido": 0
                }),
                ("seller_5", {
                    "backend": 0,
                    "frontend": 0,
                    "fullstack": 0,
                    "mobile_fullstack": 0,
                    "mobile": 0,
                    "indefinido": 1
                })
            ])
    def test_get_career_from_exp_desc(self, seller, expected, request, model_career):
        seller = request.getfixturevalue(seller)
        Experience.set_experience(seller)
        Experience.title_validity(seller)
        exp = seller.experiences[0]
        result = Career.get_career_from_exp_desc(exp, model_career)
        assert result == expected

    @pytest.mark.usefixtures("seller_1", "seller_4", "seller_5")
    @pytest.mark.parametrize(
            "seller, expected",
            [
                ("seller_1", {
                    "backend": 457,
                    "frontend": 457,
                    "fullstack": 457,
                    "mobile_fullstack": 0,
                    "mobile": 0,
                    "indefinido": 0
                }
                ),
                ("seller_4", {
                    "backend": 457,
                    "frontend": 457,
                    "fullstack": 457,
                    "mobile_fullstack": 0,
                    "mobile": 0,
                    "indefinido": 0
                }),
                ("seller_5", {
                    "backend": 823,
                    "frontend": 0,
                    "fullstack": 0,
                    "mobile_fullstack": 0,
                    "mobile": 0,
                    "indefinido": 0
                })
            ])
    def test_get_careers_for_one_exp(self, seller, expected, request, model_career):
        seller = request.getfixturevalue(seller)
        Experience.set_experience(seller)
        Experience.title_validity(seller)
        exp = seller.experiences[0]
        result = Career.get_careers_for_one_exp(exp, model_career)
        assert result == expected

    @pytest.mark.usefixtures("seller_1", "seller_2", "seller_4", "seller_5")
    @pytest.mark.parametrize(
            "seller, expected",
            [
                ("seller_1", {
                    "backend": 670,
                    "frontend": 670,
                    "fullstack": 670,
                    "mobile_fullstack": 0,
                    "mobile": 0,
                    "indefinido": 0
                }
                ),
                ("seller_2", {
                    "backend": 0,
                    "frontend": 0,
                    "fullstack": 0,
                    "mobile_fullstack": 0,
                    "mobile": 0,
                    "indefinido":0
                }),
                ("seller_4", {
                    "backend": 457,
                    "frontend": 457,
                    "fullstack": 457,
                    "mobile_fullstack": 0,
                    "mobile": 0,
                    "indefinido": 0
                }),
                ("seller_5", {
                    "backend": 1249,
                    "frontend": 213,
                    "fullstack": 213,
                    "mobile_fullstack": 0,
                    "mobile": 0,
                    "indefinido": 0
                })
            ])
    def test_get_time_exp_for_each_career(self, seller, expected, request, model_career):
        seller = request.getfixturevalue(seller)
        Experience.set_experience(seller)
        Experience.title_validity(seller)
        result = Career.get_time_exp_for_each_career(seller, model_career)
        assert result == expected

    @pytest.mark.usefixtures("seller_1", "seller_2", "seller_4", "seller_5")
    @pytest.mark.parametrize(
        "seller, expected",
        [
            ("seller_1", {
                "backend": 670/670,
                "frontend": 670/670,
                "fullstack": 670/670,
                "mobile_fullstack": 0,
                "mobile": 0,
                "indefinido": 0
            }
             ),
            ("seller_2", {
                "backend": 0,
                "frontend": 0,
                "fullstack": 0,
                "mobile_fullstack": 0,
                "mobile": 0,
                "indefinido": 0
            }),
            ("seller_4", {
                "backend": 457/457,
                "frontend": 457/457,
                "fullstack": 457/457,
                "mobile_fullstack": 0,
                "mobile": 0,
                "indefinido": 0
            }),
            ("seller_5", {
                "backend": 1249/1249,
                "frontend": 213/1249,
                "fullstack": 213/1249,
                "mobile_fullstack": 0,
                "mobile": 0,
                "indefinido": 0
            })
        ])
    def test_get_percent_of_time_experience_in_each_career(self, seller, expected, request, model_career):
        seller = request.getfixturevalue(seller)
        Experience.set_experience(seller)
        Experience.title_validity(seller)
        Career.get_percent_of_time_experience_in_each_career(seller, model_career)
        result = seller._percent_career_in_experiences
        assert result == expected

    @pytest.mark.usefixtures("seller_1", "seller_2")
    @pytest.mark.parametrize(
        "seller, expected",
        [
            ("seller_1", 1),
            ("seller_2", 0)
        ])
    def test_get_career_in_profile_title(self, seller, expected, request):
        seller = request.getfixturevalue(seller)
        Career.get_career_in_profile_title(seller)
        result = seller._career_in_profile_title
        assert result == expected

    @pytest.mark.usefixtures("seller_1", "seller_2")
    @pytest.mark.parametrize(
        "seller, expected",
        [
            ("seller_1", 1),
            ("seller_2", 0)
        ])
    def test_get_career_in_summary(self, seller, expected, request):
        seller = request.getfixturevalue(seller)
        Career.get_career_in_summary(seller)
        result = seller._career_in_summary
        assert result == expected

    @pytest.mark.usefixtures("seller_1", "seller_2")
    @pytest.mark.parametrize(
        "seller, expected",
        [
            ("seller_1", {
                "backend": 457,
                "frontend": 457,
                "fullstack": 457,
                "mobile_fullstack": 0,
                "mobile": 0,
                "indefinido": 0
            }),
            ("seller_2", {
                "backend": 0,
                "frontend": 0,
                "fullstack": 0,
                "mobile_fullstack": 0,
                "mobile": 0,
                "indefinido": 0
            })
        ])
    def test_get_careers_in_latest_exp(self, seller, expected, request, model_career):
        seller = request.getfixturevalue(seller)
        Experience.set_experience(seller)
        Experience.title_validity(seller)
        result = Career.get_careers_in_latest_exp(seller, model_career)
        assert result == expected

    @pytest.mark.usefixtures("seller_1", "seller_2")
    @pytest.mark.parametrize(
        "seller, expected",
        [
            ("seller_1", {
                "backend": 213,
                "frontend": 213,
                "fullstack": 213,
                "mobile_fullstack": 0,
                "mobile": 0,
                "indefinido": 0
            }),
            ("seller_2", {
                "backend": 0,
                "frontend": 0,
                "fullstack": 0,
                "mobile_fullstack": 0,
                "mobile": 0,
                "indefinido": 0
            })
        ])
    def test_get_careers_in_previous_exp(self, seller, expected, request, model_career):
        seller = request.getfixturevalue(seller)
        Experience.set_experience(seller)
        Experience.title_validity(seller)
        result = Career.get_careers_in_previous_exp(seller, model_career)
        assert result == expected

    @pytest.mark.usefixtures("seller_1", "seller_2", "seller_4", "seller_6")
    @pytest.mark.parametrize(
        "seller, expected",
        [
            ("seller_1", 1),
            ("seller_4", 1),
            ("seller_2", -0.75),
            ("seller_6", 0.75)
        ])
    def test_get_time_exp_with_career_recent_exps(self, seller, expected, request, model_career):
        seller = request.getfixturevalue(seller)
        Experience.set_experience(seller)
        Experience.title_validity(seller)
        Experience.latest_experience_time(seller)
        Experience.previous_experience_time(seller)
        Career.get_time_exp_with_career_recent_exps(seller, model_career)
        result = seller._career_in_recent_experiences
        assert result == expected
