import spacy

from entities.utils import get_words
from entities.seller import Seller
from entities.utils import convert_dict_values_in_one_string, finalpreprocess
from entities.experience import Experience
from entities.utils import key_words_count
from entities.description_classification import DescriptionClassification

class Career:
    nlp = spacy.load('pt_core_news_sm')

    CAREER_MAPPING = dict(
        backend = ['back-end', 'back end', 'back', 'backend'],
        frontend = ['front-end', 'front end', 'front', 'frontend'],
        fullstack = ['full stack', 'fullstack', 'full-stack'],
        mobile_fullstack = ['full stack mobile', 'fullstack mobile', 'full-stack mobile','mobile full stack', 'mobile fullstack', 'mobile full-stack'],
        mobile = ['mobile']
    )

    CAREER_EQUIVALENCE = dict(
        backend = dict(
            backend = 1,
            frontend = 0,
            fullstack = 0,
            mobile_fullstack = 0,
            mobile = 0,
            indefinido=0
        ),
        frontend = dict(
            backend=0,
            frontend=1,
            fullstack=0,
            mobile_fullstack=0,
            mobile=0,
            indefinido=0
        ),
        fullstack = dict(
            backend=1,
            frontend=1,
            fullstack=1,
            mobile_fullstack=0,
            mobile=0,
            indefinido=0
        ),
        mobile_fullstack = dict(
            backend=1,
            frontend=1,
            fullstack=1,
            mobile_fullstack=1,
            mobile=1,
            indefinido=0
        ),
        mobile = dict(
            backend=0,
            frontend=0,
            fullstack=0,
            mobile_fullstack=0,
            mobile=1,
            indefinido=0
        ),
        indefinido = dict(
            backend=0,
            frontend=0,
            fullstack=0,
            mobile_fullstack=0,
            mobile=0,
            indefinido=1
        )
    )

    CAREER_SELLER_NAMES = {
        "Back-end": 'backend',
        "Front-end": "frontend",
        "Full-stack": "fullstack",
        "Full-stack mobile": "mobile_fullstack",
        "Mobile": "mobile",
        "indefinido": "Indefinido"
    }

    @classmethod
    def careers_equivalence(cls, item:dict):
        result = dict(
            backend = 0,
            frontend = 0,
            fullstack = 0,
            mobile_fullstack = 0,
            mobile = 0,
            indefinido = 0
        )
        for key, value in item.items():
            if value == 1:
                for key2, value2 in cls.CAREER_EQUIVALENCE.get(key).items():
                    result[key2] = value2
        return result

    @staticmethod
    def delete_career_duplicates(item:dict):
        if item.get('mobile_fullstack') == 1:
            item['backend'] = 0
            item['frontend'] = 0
            item['fullstack'] = 0
            item['mobile'] = 0
        elif item.get('mobile') == 1:
            if item.get('fullstack') == 1:
                item['backend'] = 0
                item['frontend'] = 0
                item['fullstack'] = 0
                item['mobile_fullstack'] = 1
                item['mobile'] = 0
            else:
                item['backend'] = 0
                item['frontend'] = 0
                item['fullstack'] = 0
                item['mobile_fullstack'] = 0
                item['mobile'] = 1
        elif item.get('fullstack'):
            item['backend'] = 0
            item['frontend'] = 0
            item['fullstack'] = 1
            item['mobile_fullstack'] = 0
            item['mobile'] = 0
        elif item.get('backend') == 1:
            if item.get('frontend') == 1:
                item['backend'] = 0
                item['frontend'] = 0
                item['fullstack'] = 1
                item['mobile_fullstack'] = 0
                item['mobile'] = 0
        return item

    @classmethod
    def verify_exist_career_in_title(cls, exp:dict):
        careers = {}
        for key, value in cls.CAREER_MAPPING.items():
            exist_item = 0
            for item in value:
                exist_item += 1 if item in exp.get('title').lower() else 0
            valid = 1 if exist_item else 0
            output = {
                    f'{key}': valid
                }
            careers.update(output)
        return cls.delete_career_duplicates(careers)

    @staticmethod
    def get_career_from_exp_desc(exp:dict,  model: DescriptionClassification):
        career_in_desc = dict(
            backend = 0,
            frontend = 0,
            fullstack = 0,
            mobile_fullstack = 0,
            mobile = 0,
            indefinido = 0
        )
        model.transform_desc_in_array_tokenized(model.df_valid, finalpreprocess(exp.get('description')))
        validation = model.predict_text_in_desc_is_valid()
        if validation == 'valid':
            model.transform_desc_in_array_tokenized(model.df_career, finalpreprocess(exp.get('description')))
            career = model.predict_career_in_desc()
            career_in_desc[career] = 1
        else:
            career_in_desc['indefinido'] = 1
        return career_in_desc

    @classmethod
    def get_careers_for_one_exp(cls, exp, model: DescriptionClassification):
        time_exp_with_career = dict(
            backend = 0,
            frontend = 0,
            fullstack = 0,
            mobile_fullstack = 0,
            mobile = 0,
            indefinido = 0
        )
        time_exp = Experience.delta_experience_time(exp)
        exist_career_int_title = sum(cls.verify_exist_career_in_title(exp).values())
        if exist_career_int_title:
            equivalence = cls.careers_equivalence(cls.verify_exist_career_in_title(exp))
        else:
            output = cls.get_career_from_exp_desc(exp, model)
            equivalence = cls.careers_equivalence(output)
        for key, value in equivalence.items():
            time_exp_with_career[key] += time_exp if value else 0
        return time_exp_with_career

    @classmethod
    def get_time_exp_for_each_career(cls, seller: Seller, model: DescriptionClassification):
        time_exp_with_career = dict(
            backend = 0,
            frontend = 0,
            fullstack = 0,
            mobile_fullstack = 0,
            mobile = 0,
            indefinido = 0
        )
        for exp in seller.experiences:
            output = cls.get_careers_for_one_exp(exp, model)
            for key, value in output.items():
                time_exp_with_career[key] += value
        return time_exp_with_career

    @classmethod
    def get_percent_of_time_experience_in_each_career(cls, seller, model: DescriptionClassification):
        result = dict(
            backend = 0,
            frontend = 0,
            fullstack = 0,
            mobile_fullstack = 0,
            mobile = 0,
            indefinido = 0
        )
        total_exp = Experience.get_total_experience_time_with_overlap(seller)
        if total_exp:
            for key, value in cls.get_time_exp_for_each_career(seller, model).items():
                result[key] = value/total_exp
        seller.set_percent_career_in_experiences(result)

    @staticmethod
    def get_career_in_profile_title(seller):
        """
        :param seller: seller sent by request
        :return: list with 0 if career isn't in profile title or 1 if in profile title
        """
        score = 0
        exist_career = []
        words = get_words('career', seller.career)
        for word in words:
            if word.lower().replace('-', '') in seller.profile_title.lower().replace('-', ''):
                exist_career.append(1)
        if len(exist_career) >= 1:
            score += 1
        seller.set_career_in_profile_title(score)

    @staticmethod
    def get_career_in_summary(seller):
        """
        :param seller: seller sent by request
        :return: list with 0 if career isn't in summary or 1 if in summary
        """
        score = 0
        exist_career = []
        words = get_words('career', seller.career)
        for word in words:
            if word.lower().replace('-', '') in seller.summary.lower().replace('-', ''):
                exist_career.append(1)
        if len(exist_career) >= 1:
            score += 1
        seller.set_career_in_summary(score)

    @classmethod
    def get_careers_in_latest_exp(cls, seller: Seller, model: DescriptionClassification):
        if len(seller.experiences) >= 1:
            careers_latest_exp = cls.get_careers_for_one_exp(seller.experiences[0], model)
        else:
            careers_latest_exp = dict(
            backend = 0,
            frontend = 0,
            fullstack = 0,
            mobile_fullstack = 0,
            mobile = 0,
            indefinido = 0
        )
        return careers_latest_exp

    @classmethod
    def get_careers_in_previous_exp(cls, seller: Seller, model: DescriptionClassification):
        if len(seller.experiences) > 1:
            careers_previous_exp = cls.get_careers_for_one_exp(seller.experiences[1], model)
        else:
            careers_previous_exp = dict(
            backend = 0,
            frontend = 0,
            fullstack = 0,
            mobile_fullstack = 0,
            mobile = 0,
            indefinido = 0
        )
        return careers_previous_exp

    @classmethod
    def get_time_exp_with_career_recent_exps(cls, seller, model:DescriptionClassification):
        result = 0
        latest_exp = seller._latest_experience_time
        previous_exp = seller._previous_experience_time

        careers_latest_exp = cls.get_careers_in_latest_exp(seller, model)
        careers_previous_exp = cls.get_careers_in_previous_exp(seller, model)
        seller_career = cls.CAREER_SELLER_NAMES.get(seller.career)

        if latest_exp >= 245:
            if careers_latest_exp.get(seller_career) >= 1:
                if latest_exp >= 915:
                    result = 1.25
                else:
                    result = 1
            else:
                if previous_exp >= 245:
                    if careers_previous_exp.get(seller_career) >= 1:
                        if previous_exp >= 915:
                            result = 0.75
                        else:
                            result = 0.5
                    else:
                        if careers_previous_exp.get('indefinido') >= 1:
                            result = -0.5
                        else:
                            result = -0.75
        else:
            if previous_exp >= 245:
                if careers_previous_exp.get(seller_career) >= 1:
                    if previous_exp >= 915:
                        result = 0.75
                    else:
                        result = 0.5
                else:
                    if careers_previous_exp.get('indefinido') >= 1:
                        result = -0.5
                    else:
                        result = -0.75
            else:
                if careers_latest_exp.get(seller_career) >= 1 and careers_previous_exp.get(seller_career) >= 1:
                    if latest_exp + previous_exp >= 365:
                        result = 0.5
                    else:
                        result = -0.5
                else:
                    if careers_latest_exp.get('indefinido') >= 1 and careers_previous_exp.get('indefinido') >= 1:
                        result = -0.5
                    else:
                        result = -0.75
        seller.set_career_in_recent_experiences(result)

