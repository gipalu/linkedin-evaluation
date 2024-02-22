from loguru import logger

from entities.seller import Seller
from entities.experience import Experience
from entities.scoring import Scoring
from entities.articles import Articles
from entities.connections import Connections
from entities.key_words import KeyWords
from entities.recommendations import Recommendations
from entities.description_experience import DescriptionExperience
from entities.stacks import Stacks
from entities.summary import Summary
from entities.career import Career
from entities.education import Education
from entities.skills import Skills
from entities.hard_skills import HardSkills
from entities.description_classification import DescriptionClassification


def linkedin_evaluation(seller_data: dict):
    seller = Seller()
    seller.build(seller_data)
    seller.get_recommendations_comments(seller_data)
    seller.get_certifications_title(seller_data)
    seller.get_experiences_fields(seller_data)

    hard_skills = HardSkills()
    hard_skills.build(seller)

    model = DescriptionClassification()
    model.load_career_classification_model()
    model.load_desc_validation_model()

    if seller.experiences:
        Experience.set_experience(seller)
        Experience.title_validity(seller)
        Experience.set_experiences_time(seller)
        Experience.latest_experience_time(seller)
        Experience.previous_experience_time(seller)
        Experience.percent_valid_experience_between_jobs(seller)

        Scoring.get_full_experience_score(seller)
        Scoring.get_recent_experiences_score(seller)
        Scoring.time_experience_between_jobs_score(seller)
    else:
        Scoring.set_scoring_for_empty_experiences(seller)
    logger.info(seller._time_experience_score)

    if seller.skills:
        Skills.set_formated_skills(seller)
        Skills.get_skills_filtered_by_primary_stack(seller)
        Skills.get_hard_skills_in_skills(seller, hard_skills)
        Scoring.set_scoring_for_primary_stacks_in_skills(seller)
        Scoring.set_scoring_for_linkedin_seal_for_stacks_in_skills(seller)
        Scoring.set_scoring_for_colleagues_rec_for_stacks_in_skills(seller)
        Scoring.set_scoring_for_hard_skills_in_skills(seller)
    else:
        Scoring.set_scoring_for_empty_skills(seller)
    logger.info(seller._linkedin_seal_for_stacks_in_skills_score)

    hard_skills.get_hard_skills_in_summary_and_profile_title(seller)
    hard_skills.get_hard_skills_in_experiences(seller)
    hard_skills.join_fields(seller)
    Scoring.set_scoring_for_hard_skills_in_fields(seller)
    logger.info(seller._hard_skills_in_skills_score)

    Articles.get_articles_number(seller)
    Scoring.get_articles_score(seller)
    logger.info(seller._articles_score)

    Summary.summary_size(seller)
    Scoring.set_scoring_for_summary_size(seller)

    Stacks.get_stack_in_profile_title(seller)
    Stacks.get_stack_in_summary(seller)
    Stacks.get_percent_of_time_experience_with_primary_stack(seller)
    Scoring.set_scoring_for_primary_stacks_in_profile_title_and_summary(seller)
    Scoring.set_scoring_for_primary_stacks_in_exp(seller)
    logger.info(seller._stacks_in_skills_score)

    Career.get_career_in_profile_title(seller)
    Career.get_career_in_summary(seller)
    Career.get_percent_of_time_experience_in_each_career(seller, model)
    Career.get_time_exp_with_career_recent_exps(seller, model)
    Scoring.set_scoring_for_career_in_profile_title_and_summary(seller)
    Scoring.set_scoring_for_career_in_exp(seller)
    Scoring.set_scoring_for_career_in_recent_exp(seller)
    logger.info(seller._career_in_recent_exps_score)

    KeyWords.set_sellers_key_words_count(seller)
    Scoring.get_senior_score(seller)
    Scoring.get_pleno_score(seller)
    Scoring.get_leadership_score(seller)
    Scoring.get_tech_coord_score(seller)
    logger.info(seller._tech_coord_score)


    Education.get_valid_education(seller)
    Scoring.set_scoring_for_education(seller)


    if seller.recommendations_received:
        Recommendations.set_recommendations_quantity(seller)
        Recommendations.set_recommendations_size(seller)
        Recommendations.compare_recommendations_received_and_sent(seller)
        Scoring.get_recommendations_quantity_score(seller)
        Scoring.get_recommendations_size_score(seller)
    else:
        Scoring.set_scoring_for_empty_recommendations(seller)

    if seller.experiences_description:
        DescriptionExperience.set_description_experience_size(seller)
        DescriptionExperience.set_last_experience_size(seller)
        Scoring.get_description_experience_size_score(seller)
        Scoring.get_last_description_experience_size_score(seller)
    else:
        Scoring.set_scoring_for_empty_descriptions(seller)

    seller.get_sum_scores()
    Scoring.set_status_evaluation(seller)

    return dict(
        userId=seller.user_id,
        final_score=seller._final_score,
        status=seller._evaluation,
        score = dict(
            time_experience = seller._time_experience_score,
            recent_time_experience = seller._recent_time_experience_score,
            time_experience_between_jobs = seller._time_experience_between_jobs_score,
            recommendations_quantity = seller._recommendations_quantity_score,
            recommendations_size = seller._recommendations_size_score,
            description_exp_size = seller._description_size_score,
            description_last_exp_size = seller._last_description_size_score,
            key_word_senior = seller._senior_score,
            key_word_pleno = seller._pleno_score,
            key_word_leadership = seller._leadership_score,
            key_word_teech_coordenation = seller._tech_coord_score,
            articles = seller._articles_score,
            stacks_in_experience = seller._primary_stacks_in_exp_score,
            stacks_in_profile_title_and_summary = seller._primary_stacks_in_profile_title_and_summary_score,
            summary = seller._summary_size_score,
            career_in_experience = seller._career_in_exp_score,
            career_in_recent_experiences = seller._career_in_recent_exps_score,
            career_in_profile_title_and_summary = seller._career_in_profile_title_and_summary_score,
            education = seller._education_score,
            stacks_in_skills = seller._stacks_in_skills_score,
            stacks_linkedin_seal_in_skills = seller._linkedin_seal_for_stacks_in_skills_score,
            stacks_endorsed_by_colleagues_in_skills = seller._colleagues_rec_for_stacks_in_skills_score,
            hard_skills_in_fields = seller._hard_skills_in_fields_score,
            hard_skills_in_skills = seller._hard_skills_in_skills_score
        )
    )
