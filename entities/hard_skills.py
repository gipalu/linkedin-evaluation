from entities.seller import Seller
from entities.utils import get_words


class HardSkills:
    def __init__(self):
        self.hard_skills: list = []

    def build(self, seller: Seller):
        hard_skills = []
        for stack in seller.stack:
            if stack != 'C#/.Net':
                hs = get_words('hard_skills', stack)
            else:
                hs = get_words('hard_skills', 'CSharpDotNet')
            hard_skills.extend(hs)
        self.hard_skills = list(set(hard_skills))

    def get_hard_skills_in_summary_and_profile_title(self, seller: Seller):
        """
        :param seller: seller sent by request
        :return: quantity of hard skills in summary and profile title fields
        """
        fields = ['summary', 'profile_title']
        result = {}
        for field in fields:
            hard_skills_quantity = 0
            seller_attr = getattr(seller, field)
            for hard_skill in self.hard_skills:
                if hard_skill.lower() in seller_attr.lower():
                    hard_skills_quantity += 1
            output = {
                f'{field}': hard_skills_quantity
            }
            result.update(output)
        return result


    def get_hard_skills_in_experiences(self, seller: Seller):
        """
        :param seller: seller sent by request
        :return: quantity of hard skills in experience description
        """
        hard_skills_quantity = 0
        for hard_skill in self.hard_skills:
            for desc in seller.experiences_description:
                if hard_skill.lower() in desc.lower():
                    hard_skills_quantity += 1
        output = dict(
            experiences_description = hard_skills_quantity
        )
        return output

    def join_fields(self, seller: Seller):
        """
        :param seller: seller sent by request
        :return: join all dicts with hard skills quantity
        """
        fields = self.get_hard_skills_in_summary_and_profile_title(seller)
        exp_field = self.get_hard_skills_in_experiences(seller)
        fields.update(exp_field)
        seller.set_hard_skills_quantity_in_fields(fields)