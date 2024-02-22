import sys
from loguru import logger
import pytest

from entities.loader import loader
from entities.seller import Seller
from entities.experience import Experience
from entities.scoring import Scoring
from entities.key_words import KeyWords
from entities.articles import Articles
from entities.recommendations import Recommendations
from entities.description_experience import DescriptionExperience
from entities.stacks import Stacks
from entities.summary import Summary
from entities.career import Career
from entities.education import Education
from entities.skills import Skills
from entities.hard_skills import HardSkills
from entities.description_classification import DescriptionClassification


sys.path.append('../')

class TestScores:
    @pytest.fixture
    def seller(self):
        seller = Seller()
        seller.build(loader("seller_1"))
        seller.get_recommendations_comments(loader("seller_1"))
        seller.get_certifications_title(loader("seller_1"))
        seller.get_experiences_fields(loader("seller_1"))

        model = DescriptionClassification()
        model.load_career_classification_model()
        model.load_desc_validation_model()

        hard_skills = HardSkills()
        hard_skills.build(seller)
        Experience.set_experience(seller)
        Experience.title_validity(seller)
        Experience.set_experiences_time(seller)
        Experience.latest_experience_time(seller)
        Experience.previous_experience_time(seller)
        Experience.percent_valid_experience_between_jobs(seller)
        Articles.get_articles_number(seller)
        Recommendations.compare_recommendations_received_and_sent(seller)
        Recommendations.set_recommendations_quantity(seller)
        Recommendations.set_recommendations_size(seller)
        DescriptionExperience.set_description_experience_size(seller)
        DescriptionExperience.set_last_experience_size(seller)
        Stacks.get_percent_of_time_experience_with_primary_stack(seller)
        Stacks.get_stack_in_profile_title(seller)
        Stacks.get_stack_in_summary(seller)
        Summary.summary_size(seller)
        Career.get_percent_of_time_experience_in_each_career(seller, model)
        Career.get_career_in_profile_title(seller)
        Career.get_career_in_summary(seller)
        Career.get_time_exp_with_career_recent_exps(seller, model)
        Education.get_valid_education(seller)
        Skills.set_formated_skills(seller)
        Skills.get_skills_filtered_by_primary_stack(seller)
        Skills.get_hard_skills_in_skills(seller, hard_skills)
        hard_skills.get_hard_skills_in_summary_and_profile_title(seller)
        hard_skills.get_hard_skills_in_experiences(seller)
        hard_skills.join_fields(seller)
        return seller

    @pytest.fixture
    def seller_key_word(self):
        seller = Seller()
        seller.build(loader("seller_1"))
        seller.get_recommendations_comments(loader("seller_1"))
        seller.get_experiences_fields(loader("seller_1"))
        seller.get_certifications_title(loader("seller_1"))
        KeyWords.set_sellers_key_words_count(seller)
        return seller

    def test_get_full_experience_score(self, seller):
        Scoring.get_full_experience_score(seller)
        result = seller._time_experience_score
        valid_result = 0
        assert result == valid_result


    def test_get_recent_experiences_score(self, seller):
        Scoring.get_recent_experiences_score(seller)
        result = seller._recent_time_experience_score
        valid_result = 0.5 * 0.8
        assert result == valid_result


    def test_time_experience_between_jobs_score(self, seller):
        Scoring.time_experience_between_jobs_score(seller)
        result = seller._time_experience_between_jobs_score
        valid_result = 0.25
        assert result == valid_result

    def test_get_connections(self, seller):
        Scoring.get_connections_score(seller)
        result = seller._connections_score
        valid_result = 1 * 0.25
        assert result == valid_result

    def test_get_senior_score(self, seller_key_word):
        Scoring.get_senior_score(seller_key_word)
        result = seller_key_word._senior_score
        valid_result = 0.75
        assert result == valid_result

    def test_get_pleno_score(self, seller_key_word):
        Scoring.get_pleno_score(seller_key_word)
        result = seller_key_word._pleno_score
        valid_result = 0
        assert result == valid_result

    def test_get_leadership_score(self, seller_key_word):
        Scoring.get_leadership_score(seller_key_word)
        result = seller_key_word._leadership_score
        valid_result = 1 * 0.6
        assert result == valid_result

    def test_get_tech_coord_score(self, seller_key_word):
        Scoring.get_tech_coord_score(seller_key_word)
        result = seller_key_word._tech_coord_score
        valid_result = 0 * 0.8
        assert result == valid_result

    def test_get_articles_score(self, seller):
        Scoring.get_articles_score(seller)
        result = seller._articles_score
        valid_result = 0.5 * 0.25
        assert result == valid_result

    def test_get_recommendations_quantity_score(self, seller):
        Scoring.get_recommendations_quantity_score(seller)
        result = seller._recommendations_quantity_score
        valid_result = 0.5 * 0.5 * 1
        assert result == valid_result

    def test_get_recommendations_size_score(self, seller):
        Scoring.get_recommendations_size_score(seller)
        result = seller._recommendations_size_score
        valid_result = 0.75 * 0.5 * 1
        assert result == valid_result

    def test_get_description_experience_size_score(self, seller):
        Scoring.get_description_experience_size_score(seller)
        result = seller._description_size_score
        valid_result = 1 * 1.5
        assert result == valid_result

    def test_get_last_description_experience_size_score(self, seller):
        Scoring.get_last_description_experience_size_score(seller)
        result = seller._last_description_size_score
        valid_result = 1
        assert result == valid_result

    def test_set_scoring_for_primary_stacks_in_exp(self, seller):
        Scoring.set_scoring_for_primary_stacks_in_exp(seller)
        result = seller._primary_stacks_in_exp_score
        valid_result = 0.25 * 1.5
        assert result == valid_result

    def test_set_scoring_for_primary_stacks_in_profile_title_and_summary(self, seller):
        Scoring.set_scoring_for_primary_stacks_in_profile_title_and_summary(seller)
        result = seller._primary_stacks_in_profile_title_and_summary_score
        valid_result = 0.125 / 2
        assert result == valid_result

    def test_set_scoring_for_summary_size(self, seller):
        Scoring.set_scoring_for_summary_size(seller)
        result = seller._summary_size_score
        valid_result = 0.25 * 0.25
        assert result == valid_result

    def test_set_scoring_for_career_in_exp(self, seller):
        Scoring.set_scoring_for_career_in_exp(seller)
        result = seller._career_in_exp_score
        valid_result = 0.75
        assert result == valid_result

    def test_set_scoring_for_career_in_recent_exp(self, seller):
        Scoring.set_scoring_for_career_in_recent_exp(seller)
        result = seller._career_in_recent_exps_score
        valid_result = 0.75
        assert result == valid_result

    def test_set_scoring_for_career_in_profile_title_and_summary(self, seller):
        Scoring.set_scoring_for_career_in_profile_title_and_summary(seller)
        result = seller._career_in_profile_title_and_summary_score
        valid_result = 0.5 * 0.25
        assert result == valid_result

    def test_get_valid_education(self, seller):
        Scoring.set_scoring_for_education(seller)
        result = seller._education_score
        valid_relsut = 0.5 * 0.25
        assert result == valid_relsut

    def test_set_scoring_for_primary_stacks_in_skills(self, seller):
        Scoring.set_scoring_for_primary_stacks_in_skills(seller)
        result = seller._stacks_in_skills_score
        valid_result = 0.125 / 2
        assert result == valid_result

    def test_set_scoring_for_linkedin_seal_for_stacks_in_skills(self, seller):
        Scoring.set_scoring_for_linkedin_seal_for_stacks_in_skills(seller)
        result = seller._linkedin_seal_for_stacks_in_skills_score
        valid_result = 0.25 / 2
        assert result == valid_result

    def test_set_scoring_for_colleagues_rec_for_stacks_in_skills(self, seller):
        Scoring.set_scoring_for_colleagues_rec_for_stacks_in_skills(seller)
        result = seller._colleagues_rec_for_stacks_in_skills_score
        valid_result = 0.25 / 2
        assert result == valid_result

    def test_set_scoring_for_hard_skills_in_skills(self, seller):
        Scoring.set_scoring_for_hard_skills_in_skills(seller)
        result = seller._hard_skills_in_skills_score
        valid_result = 0.1
        assert  result == valid_result

    def test_set_scoring_for_hard_skills_in_fields(self, seller):
        Scoring.set_scoring_for_hard_skills_in_fields(seller)
        result = seller._hard_skills_in_fields_score
        valid_result = 0.15
        assert  result == valid_result

    def test_set_status_evaluation(self, seller):
        KeyWords.set_sellers_key_words_count(seller)

        Scoring.get_full_experience_score(seller)
        Scoring.get_recent_experiences_score(seller)
        Scoring.time_experience_between_jobs_score(seller)
        Scoring.get_senior_score(seller)
        Scoring.get_pleno_score(seller)
        Scoring.get_leadership_score(seller)
        Scoring.get_tech_coord_score(seller)
        Scoring.get_articles_score(seller)
        Scoring.get_recommendations_quantity_score(seller)
        Scoring.get_recommendations_size_score(seller)
        Scoring.get_description_experience_size_score(seller)
        Scoring.get_last_description_experience_size_score(seller)
        Scoring.set_scoring_for_primary_stacks_in_exp(seller)
        Scoring.set_scoring_for_primary_stacks_in_profile_title_and_summary(seller)
        Scoring.set_scoring_for_summary_size(seller)
        Scoring.set_scoring_for_career_in_exp(seller)
        Scoring.set_scoring_for_career_in_recent_exp(seller)
        Scoring.set_scoring_for_career_in_profile_title_and_summary(seller)
        Scoring.set_scoring_for_education(seller)
        Scoring.set_scoring_for_primary_stacks_in_skills(seller)
        Scoring.set_scoring_for_linkedin_seal_for_stacks_in_skills(seller)
        Scoring.set_scoring_for_colleagues_rec_for_stacks_in_skills(seller)
        Scoring.set_scoring_for_hard_skills_in_skills(seller)
        Scoring.set_scoring_for_hard_skills_in_fields(seller)
        seller.get_sum_scores()
        Scoring.set_status_evaluation(seller)
        result = seller._evaluation
        valid_result = 1
        assert result == valid_result

