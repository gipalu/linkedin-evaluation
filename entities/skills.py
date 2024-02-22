from entities.seller import Seller
from entities.utils import get_number_in_string
from entities.utils import get_words
from entities.utils import convert_dict_values_in_one_string
from entities.hard_skills import HardSkills

class Skills:
    @staticmethod
    def set_formated_skills(seller):
        """
        :param seller: seller sent by request
        :return: dict with skills formatted with skill name and binary fields
        """
        result = []
        for skill in seller.skills:
            output = dict (
                stack = skill.get('title').lower(),
                endorsed_quantity = get_number_in_string(skill.get('endorsements').get('endorsed_quantitys')),
                endorsed_by_others = 1 if skill.get('endorsements').get('endorsed_by_others') else 0,
                endorsed_by_colleagues = 1 if skill.get('endorsements').get('endorsed_by_colleagues') else 0,
                endorsed_by_linkedin = 1 if skill.get('endorsements').get('endorsed_by_linkedin') else 0
            )
            result.append(output)
        seller.skills = result

    @staticmethod
    def get_skills_filtered_by_primary_stack(seller):
        """
        :param seller: seller sent by request
        :return: brings the skill field for each seller stack
        """
        skills_filtered = {}
        for skill in seller.skills:
            for stack in seller.stack:
                if stack.lower() in skill.get('stack'):
                    output = {
                        f'{stack.lower()}': skill
                    }
                    skills_filtered.update(output)
        seller.set_stacks_in_skills(skills_filtered)

    @staticmethod
    def get_hard_skills_in_skills(seller: Seller, hard_skills: HardSkills):
        """
        :param seller: seller sent by request
        :param hard_skills:  bring the quantity of hard skills in skills field
        :return:
        """
        hard_skills_quantity = 0
        hard_skills = hard_skills.hard_skills
        for skill in seller.skills:
            if skill.get('stack') in [hs.lower() for hs in hard_skills]:
                hard_skills_quantity += 1
        seller.set_hard_skills_quantity_in_skills(hard_skills_quantity)

