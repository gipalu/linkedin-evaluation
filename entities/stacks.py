import spacy

from entities.seller import Seller
from entities.experience import Experience
from entities.utils import convert_dict_values_in_one_string
from entities.utils import key_words_count


class Stacks:
    nlp = spacy.load('pt_core_news_sm')

    STACKS_MAPPING = {
        'Angular': ['angular'],
        'C#/.Net': ['.net', 'dot net', 'c#/.net'],
        'Node': ['node', 'nodejs', 'node.js'],
        'React': ['react', 'reactjs', 'react.js'],
        'React Native': ['react native'],
        'Vue': ['vue'],
    }

    @classmethod
    def check_stacks_in_field(cls, field):
        result = {}
        for key, value in cls.STACKS_MAPPING.items():
            output = {
                f'{key}': key_words_count(cls.nlp, field.lower(), value)
            }
            result.update(output)
        return result

    @classmethod
    def check_if_stack_exists_in_experience(cls, seller: Seller):
        stack_in_fields = []
        result = {}
        for exp in seller.experiences:
            time_experience = Experience.delta_experience_time(exp)
            stacks_in_field = cls.check_stacks_in_field(convert_dict_values_in_one_string(exp))
            for stack in seller.stack:
                if stack == 'React':
                    if stacks_in_field.get(stack) != stacks_in_field.get('React Native'):
                        output = dict(
                            time_experience=time_experience,
                            stack=stack
                        )
                        stack_in_fields.append(output)
                else:
                    if stacks_in_field.get(stack):
                        output = dict(
                            time_experience = time_experience,
                            stack = stack
                        )
                        stack_in_fields.append(output)
        for item in stack_in_fields:
            result.setdefault(item['stack'], []).append(item)
        return result


    @classmethod
    def get_percent_of_time_experience_with_each_stack(cls, seller):
        """
        :param seller: seller sent by request
        :return: of the total experiences how many has the stack in title and description
        """
        items = cls.check_if_stack_exists_in_experience(seller)
        percent_time_experience_with_stack = []
        for stack in seller.stack:
            if stack in items.keys():
                total_time_experience = Experience.get_total_experience_time_with_overlap(seller)
                experience = [i.get('time_experience') for i in items.get(stack)]
                output = dict(
                    stack = stack,
                    time_experience_with_stack = sum(experience) / total_time_experience
                )
                percent_time_experience_with_stack.append(output)
            else:
                output = dict(
                    stack=stack,
                    time_experience_with_stack=0
                )
                percent_time_experience_with_stack.append(output)
        return percent_time_experience_with_stack

    @classmethod
    def get_percent_of_time_experience_with_primary_stack(cls, seller):
        items = cls.get_percent_of_time_experience_with_each_stack(seller)
        experiences = []
        for item in items:
            experiences.append(item.get('time_experience_with_stack'))
        seller.set_percent_primary_stacks_in_experiences(sum(experiences)/len(experiences))

    @staticmethod
    def get_stack_in_profile_title(seller):
        """
        :param seller: seller sent by request
        :return: list with 0 if stack isn't in profile title or 1 if in profile title
        """
        result = {}
        for stack in seller.stack:
            if stack.lower() in seller.profile_title.lower():
                exist_stack = 1
            else:
                exist_stack = 0
            output = {
                f'{stack}': exist_stack
            }
            result.update(output)
            seller.set_primary_stacks_in_profile_title(result)

    @staticmethod
    def get_stack_in_summary(seller):
        """
        :param seller: seller sent by request
        :return: list with 0 if stack isn't in summary or 1 if in summary
        """
        result = {}
        for stack in seller.stack:
            if stack.lower() in seller.summary.lower():
                exist_stack = 1
            else:
                exist_stack = 0
            output = {
                f'{stack}': exist_stack
            }
            result.update(output)
            seller.set_primary_stacks_in_summary(result)

