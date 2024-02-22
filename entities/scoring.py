#TODO create tests for breakpoints

import bisect

from entities.seller import Seller
from entities.connections import Connections
from entities.recommendations import Recommendations


class Scoring:
    @staticmethod
    def get_full_experience_score(seller: Seller):
        """
        :param seller: seller sent by request
        :return: score from the seller full experience
        """
        total_experience_time = seller._total_valid_experience_time
        break_points = [2.5, 5, 8]
        if seller.level in (3,4):
            score = 0
        elif seller.level in (5,6):
            scores = [0, 1, 1.5, 2]
            index = bisect.bisect_left(break_points, total_experience_time)
            score = scores[index]
        else:
            scores = [0, 0.5, 1, 1.25]
            index = bisect.bisect_left(break_points, total_experience_time)
            score = scores[index]
        seller._time_experience_score = score

    @staticmethod
    def get_recent_experiences_score(seller: Seller):
        """
        :param seller: seller sent by request
        :return: score from the seller recent experiences
        """
        latest_exp = seller._latest_experience_time
        previous_exp = seller._previous_experience_time
        if latest_exp >= 365:
            score = 0.5
        else:
            if previous_exp >= 365:
                score = 0.25
            else:
                score = 0
        seller._recent_time_experience_score = score * 0.8

    @staticmethod
    def time_experience_between_jobs_score(seller: Seller):
        """
        :param seller: seller sent by request
        :return: score from the seller experience between jobs
        """
        percent = seller._percent_experiences_between_jobs
        break_points = [0.25, 0.6, 0.8, 0.99]
        scores = [0, 0.25, 0.5, 0.75, 1]
        index = bisect.bisect_left(break_points, percent)
        score = scores[index]
        seller._time_experience_between_jobs_score = score

    @staticmethod
    def set_scoring_for_empty_experiences(seller: Seller):
        """
        :param seller: seller sent by request with empty experience field
        :return: score 0 for experiences scores
        """
        seller._time_experience_score = 0
        seller._recent_time_experience_score = 0
        seller._time_experience_between_jobs_score = 0

    @staticmethod
    def get_connections_score(seller: Seller):
        """
        :param seller: seller sent by request
        :return: score from the connections number
        """
        connections_number = Connections.connection_number(seller.connections)
        break_points = [150, 499]
        scores = [0, 0.5, 1]
        index = bisect.bisect_left(break_points, connections_number)
        score = scores[index]
        seller._connections_score = score * 0.25

    @staticmethod
    def get_senior_score(seller: Seller):
        """
        :param seller: seller sent by request
        :return: score from the key word senior
        """
        senior_key_words = seller._key_words_count.get('senior')
        break_points = [0.99, 3]
        scores = [0, 0.75, 1]
        index = bisect.bisect_left(break_points, senior_key_words)
        score = scores[index]
        seller._senior_score = score

    @staticmethod
    def get_pleno_score(seller: Seller):
        """
        :param seller: seller sent by request
        :return: score from the key word pleno
        """
        pleno_key_words = seller._key_words_count.get('pleno')
        break_points = [0.99, 3]
        scores = [0, 0.75, 1]
        index = bisect.bisect_left(break_points, pleno_key_words)
        score = scores[index]
        seller._pleno_score = score

    @staticmethod
    def get_leadership_score(seller: Seller):
        """
        :param seller: seller sent by request
        :return: score from the key word leadership
        """
        leadership_key_words = seller._key_words_count.get('leadership')
        if leadership_key_words == 0:
            score = 0
        else:
            score = 1
        seller._leadership_score = score * 0.6

    @staticmethod
    def get_tech_coord_score(seller: Seller):
        """
        :param seller: seller sent by request
        :return: score from the key word technical coordination
        """
        tech_coord_key_words = seller._key_words_count.get('technical_coordination')
        if tech_coord_key_words == 0:
            score = 0
        else:
            score = 1
        seller._tech_coord_score = score * 0.8

    @staticmethod
    def get_articles_score(seller: Seller):
        """
        :param seller: seller sent by request
        :return: score from the articles number
        """
        articles_quantity = seller._articles_quantity
        break_points = [0.99, 1.99]
        scores = [0, 0.25, 0.5]
        index = bisect.bisect_left(break_points, articles_quantity)
        score = scores[index]
        seller._articles_score = score * 0.25

    @staticmethod
    def get_recommendations_quantity_score(seller: Seller):
        """
        :param seller: seller sent by request
        :return: score from the quantity recommendations
        """
        multiplier = seller._recommendations_multiplier
        recommendation_quantity = seller._recommendations_quantity
        break_points = [0.99, 2.99]
        scores = [0, 0.25, 0.5]
        index = bisect.bisect_left(break_points, recommendation_quantity)
        score = scores[index] * 0.5
        seller._recommendations_quantity_score = score * multiplier

    @staticmethod
    def get_recommendations_size_score(seller: Seller):
        """
        :param seller: seller sent by request
        :return: score from the percent of recommendations with right size
        """
        multiplier = seller._recommendations_multiplier
        percent = seller._percent_recommendations_right_size
        break_points = [0.25, 0.6, 0.8, 0.99]
        scores = [0, 0.25, 0.5, 0.75, 1]
        index = bisect.bisect_left(break_points, percent)
        score = scores[index] * 0.5
        seller._recommendations_size_score = score * multiplier

    @staticmethod
    def set_scoring_for_empty_recommendations(seller: Seller):
        """
        :param seller: seller sent by request
        :return: score 0 to seller with recommendation field empty
        """
        seller._recommendations_quantity_score = 0
        seller._recommendations_size_score = 0

    @staticmethod
    def get_description_experience_size_score(seller: Seller):
        """
        :param seller: seller sent by request
        :return: score from the percent of description experiences with right size
        """
        percent = seller._percent_description_experience_size
        break_points = [0.25, 0.6, 0.8, 0.99]
        scores = [0, 0.25, 0.5, 0.75, 1]
        index = bisect.bisect_left(break_points, percent)
        score = scores[index]
        seller._description_size_score = score * 1.5

    @staticmethod
    def get_last_description_experience_size_score(seller: Seller):
        """
        :param seller: seller sent by request
        :return: score from the last description experience size
        """
        size_last_exp = seller._last_description_experience_size
        break_points = [0, 49, 89, 150]
        scores = [-0.25, 0, 0.25, 0.75, 1]
        index = bisect.bisect_left(break_points, size_last_exp)
        score = scores[index]
        seller._last_description_size_score = score

    @staticmethod
    def set_scoring_for_empty_descriptions(seller: Seller):
        """
        :param seller: seller sent by request
        :return: score 0 to seller with experience field empty
        """
        seller._description_size_score = 0
        seller._last_description_size_score = -0.25

    @staticmethod
    def set_scoring_for_primary_stacks_in_exp(seller: Seller):
        """
        :param seller: seller sent by request
        :return: score for stack in experience
        """
        percent = seller._percent_primary_stacks_in_experiences
        break_points = [0.25, 0.6, 0.8, 0.99]
        scores = [0, 0.25, 0.5, 0.75, 1]
        index = bisect.bisect_left(break_points, percent)
        stack_in_exp_score = scores[index]
        seller._primary_stacks_in_exp_score = stack_in_exp_score * 1.5

    @staticmethod
    def set_scoring_for_primary_stacks_in_profile_title_and_summary(seller: Seller):
        """
        :param seller: seller sent by request
        :return: score for stack in profile_title and summary
        """
        scores = []
        profile_title = seller._primary_stacks_in_profile_title
        summary = seller._primary_stacks_in_summary
        for stack in seller.stack:
            if profile_title.get(stack):
                score = 0.5 if summary.get(stack) else 0.25
            elif profile_title.get(stack) == 0.5:
                score = 0.5 if summary.get(stack) else 0.25
            else:
                score = 0.25 if summary.get(stack) else 0
            scores.append(score * 0.5)
        seller._primary_stacks_in_profile_title_and_summary_score = sum(scores) / len(scores)

    @staticmethod
    def set_scoring_for_summary_size(seller):
        """
        :param seller: seller sent by request
        :return: score for summary size
        """
        summary = seller._summary_size
        break_points = [650, 900]
        scores = [0, 0.25, 0.5]
        index = bisect.bisect_left(break_points, summary)
        score = scores[index]
        seller._summary_size_score = score * 0.25

    @staticmethod
    def set_scoring_for_career_in_exp(seller):
        """
        :param seller: seller sent by request
        :return: score for career in experience
        """
        career_names = {
                "Back-end": 'backend',
                "Front-end": "frontend",
                "Full-stack": "fullstack",
                "Full-stack mobile": "mobile_fullstack",
                "Mobile": "mobile",
                "indefinido": "Indefinido"
            }
        career = career_names.get(seller.career)
        percent_in_career = seller._percent_career_in_experiences.get(career)
        break_points = [0.25, 0.5, 0.6, 0.75, 0.9]
        scores = [-0.5, -0.25, 0, 0.5, 0.75, 1]
        index = bisect.bisect_left(break_points, percent_in_career)
        career_in_exp_score = scores[index]
        seller._career_in_exp_score = career_in_exp_score * 0.75

    @staticmethod
    def set_scoring_for_career_in_profile_title_and_summary(seller: Seller):
        """
        :param seller: seller sent by request
        :return: score for career in profile_title and summary
        """
        profile_title = seller._career_in_profile_title
        summary = seller._career_in_summary
        if profile_title:
            score = 0.5 if summary else 0.25
        else:
            score = 0.25 if summary else 0
        seller._career_in_profile_title_and_summary_score = score * 0.25

    @staticmethod
    def set_scoring_for_career_in_recent_exp(seller: Seller):
        """
        :param seller: seller sent by request
        :return: score for career in recent experiences

        """
        score = seller._career_in_recent_experiences * 0.75
        seller._career_in_recent_exps_score = score

    @staticmethod
    def set_scoring_for_education(seller: Seller):
        """
        :param seller: seller sent by request
        :return: score for education field
        """
        education = seller._education_validity
        score = 0.5 if education == 1 else 0
        seller._education_score = score * 0.25

    @staticmethod
    def set_scoring_for_primary_stacks_in_skills(seller: Seller):
        """
        :param seller: seller sent by request
        :return: score for primary stacks in skills
        """
        valid_stacks = seller._stacks_in_skills
        final_score = []
        for stack in seller.stack:
            stack = stack.lower()
            if valid_stacks.get(stack):
                break_points = [1, 8, 15]
                scores = [0.25, 0.5, 0.75, 0.25]
                index = bisect.bisect_left(break_points, valid_stacks.get(stack).get('endorsed_quantity'))
                score = scores[index]
            else:
                score = 0
            final_score.append(score * 0.25)
        seller._stacks_in_skills_score  = sum(final_score) / len(final_score)

    @staticmethod
    def set_scoring_for_linkedin_seal_for_stacks_in_skills(seller):
        """
        :param seller: seller sent by request
        :return: score for stacks in skills that has linkedin seal
        """
        valid_stacks = seller._stacks_in_skills
        final_score = []
        for stack in seller.stack:
            stack = stack.lower()
            if valid_stacks.get(stack):
                score = 0.5 if valid_stacks.get(stack).get('endorsed_by_linkedin') else 0
            else:
                score = 0
            final_score.append(score * 0.5)
        seller._linkedin_seal_for_stacks_in_skills_score = sum(final_score) / len(final_score)

    @staticmethod
    def set_scoring_for_colleagues_rec_for_stacks_in_skills(seller):
        """
        :param seller: seller sent by request
        :return: score for stacks in skills that has colleagues recommendation
        """
        valid_stacks = seller._stacks_in_skills
        final_score = []
        for stack in seller.stack:
            stack = stack.lower()
            if valid_stacks.get(stack):
                score = 0.5 if valid_stacks.get(stack).get('endorsed_by_colleagues') else 0
            else:
                score = 0
            final_score.append(score * 0.5)
        seller._colleagues_rec_for_stacks_in_skills_score = sum(final_score) / len(final_score)

    @staticmethod
    def set_scoring_for_empty_skills(seller: Seller):
        """
        :param seller: seller sent by request
        :return: score 0 to seller with skills field empty
        """
        seller._stacks_in_skills_score = 0
        seller._linkedin_seal_for_stacks_in_skills_score = 0
        seller._colleagues_rec_for_stacks_in_skills_score = 0
        seller._hard_skills_in_skills_score = 0

    @staticmethod
    def set_scoring_for_hard_skills_in_skills(seller: Seller):
        """
        :param seller: seller sent by request
        :return: score for hard skills in skills field
        """
        hd_quantity = seller._hard_skills_quantity_in_skills
        break_points = [1, 2, 5]
        scores = [0, 0.5, 0.75, 1]
        index = bisect.bisect_left(break_points, hd_quantity)
        score = scores[index]
        seller._hard_skills_in_skills_score = score * 0.2

    @staticmethod
    def set_scoring_for_hard_skills_in_fields(seller: Seller):
        """
        :param seller: seller sent by request
        :return: score for hard skills in profile title, summary and description experience
        """
        {'profile_title': 1, 'summary': 0, 'experiences_description': 0}
        hd_quantity = 0
        for value in seller._hard_skills_quantity_in_fields.values():
            hd_quantity += value
        break_points = [0, 2, 5]
        scores = [0, 0.5, 0.75, 1]
        index = bisect.bisect_left(break_points, hd_quantity)
        score = scores[index]
        seller._hard_skills_in_fields_score = score * 0.3

    @staticmethod
    def set_status_evaluation(seller: Seller):
        """
        :param seller: seller sent by request
        :return: evaluation id from the seller
        """
        final_score = seller._final_score
        evaluation = 1 if final_score >= 5.6 else 2
        seller.set_evaluation(evaluation)

