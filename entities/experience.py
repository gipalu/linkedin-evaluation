import pendulum
import copy
from datetime import datetime
from collections import namedtuple

from entities.seller import Seller
from entities.utils import predict_title


class Experience:
    _MONTHS_MAPPING = dict(
        jan = 1,
        fev = 2,
        mar = 3,
        abr = 4,
        mai = 5,
        jun = 6,
        jul = 7,
        ago = 8,
        set = 9,
        out = 10,
        nov = 11,
        dez = 12
    )
    @classmethod
    def date_name_to_int(cls, lista):
        """
        :param lista: list with day, month and year of experience
        :return: list with month replaced by your reference integer
        """
        for index in range(len(lista)):
            month = cls._MONTHS_MAPPING.get(lista[index])
            if month:
                lista[index] = month
        return lista

    @classmethod
    def transform_date(cls, text):
        """
        :param text: list with day, month and year of experience
        :return: dict with exp values formatted
        """
        data_split = text.split()
        is_len_three = len(data_split) == 3
        is_len_one = len(data_split) == 1
        if is_len_one or is_len_three:
            cls.date_name_to_int(data_split)
            output = {
                'day': 1,
                'month': data_split[0] if is_len_three else 1,
                'year': int(data_split[2]) if is_len_three else int(data_split[0])
            }
        else:
            output = None
        return output

    @classmethod
    def set_experience(cls, seller: Seller):
        """
        :param seller: seller sent by request
        :return: list with all seller experiences formatted
        """
        time_experiences = []
        experiences = []
        if seller.experiences:
            print(seller.experiences)
            for experience in seller.experiences:
                print(experience)
                startDate = cls.transform_date(experience.get('startDate'))
                endDate = cls.transform_date(experience.get('endDate'))
                title = experience.get('title')
                description = experience.get('description')
                output = {
                    'userId': seller.user_id,
                    'level': seller.level,
                    'startDate': startDate,
                    'endDate': endDate,
                    'title': title,
                    'description': description
                }
                experiences.append(output)
            for exp in experiences:
                userId = exp.get('userId')
                level = exp.get('level')
                title = exp.get('title')
                description = exp.get('description')
                if not exp.get('startDate'):
                    startDate = 0
                    endDate = 0
                else:
                    startDate = pendulum.datetime(exp.get('startDate').get('year'), exp.get('startDate').get('month'), exp.get('startDate').get('day')).to_date_string()
                    if exp.get('endDate') == None:
                        endDate = pendulum.today().to_date_string()
                    else:
                        endDate = pendulum.datetime(exp.get('endDate').get('year'), exp.get('endDate').get('month'), exp.get('endDate').get('day')).to_date_string()
                output_final = {
                    'userId': userId,
                    'level': level,
                    'startDate': startDate,
                    'endDate': endDate,
                    'title': title,
                    'description': description
                }
                time_experiences.append(output_final)
        else:
            output = {
                'userId': seller.user_id,
                'level': seller.level,
                'startDate': 0,
                'endDate': 0,
                'title': 0,
                'description': ''
            }
            time_experiences.append(output)
        seller.experiences = time_experiences

    time_experience_filtered = []

    @classmethod
    def title_validity(cls, seller):
        """
        :param seller: seller sent by request
        :return: list of dicts with all seller valid experience
        """
        time_experience_filtered = []
        for exp in seller.experiences:
            title = exp.get('title')
            if title:
                validity = predict_title(title)
                if validity:
                    time_experience_filtered.append(exp)
        seller.experiences = time_experience_filtered

    @staticmethod
    def overlap_two_intervals(exp_ref, exp):
        """
        :param exp_ref: dict with one seller experience
        :param exp: dict with other seller experience
        :return: overlap between two intervals passed
        """
        Range = namedtuple('Range', ['start', 'end'])
        range1 = Range(start=datetime.strptime(exp_ref["startDate"], '%Y-%m-%d'),
                   end=datetime.strptime(exp_ref["endDate"], '%Y-%m-%d'))
        range2 = Range(start=datetime.strptime(exp["startDate"], '%Y-%m-%d'),
                   end=datetime.strptime(exp["endDate"], '%Y-%m-%d'))
        latest_start = max(range1.start, range2.start)
        earliest_end = min(range1.end, range2.end)
        delta = (earliest_end - latest_start).days + 1
        overlap = max(0, delta)
        return overlap

    @classmethod
    def get_total_intersection(cls, seller):
        """
        :param seller: seller sent by request
        :return: all overlaps in seller experience
        """
        overlap = int()
        if len(seller.buffer) < 2:
            return 0
        else:
            exp_ref = seller.buffer.pop(0)
            for exp in seller.buffer:
                overlap_two = cls.overlap_two_intervals(exp_ref, exp)
                overlap += overlap_two
            return overlap + cls.get_total_intersection(seller)

    @staticmethod
    def delta_experience_time(experience):
        """
        :param experience: experience field from seller
        :return: time experience in days to one experience
        """
        start_date = pendulum.parse(experience.get('startDate')).date()
        end_date = pendulum.parse(experience.get('endDate')).date()
        delta = end_date - start_date
        return delta.days

    @classmethod
    def get_total_experience_time_with_overlap(cls, seller):
        """
        :return: full time experience for valid titles without taking off overlaps
        """
        delta_experiences = []
        for exp in seller.experiences:
            delta = cls.delta_experience_time(exp)
            delta_experiences.append(delta)
        return sum(delta_experiences)

    @classmethod
    def set_experiences_time(cls, seller):
        """
        :param seller: seller sent by request
        :return: all the time experience from seller
        """
        delta_experiences = []
        for exp in seller.experiences:
            delta = cls.delta_experience_time(exp)
            delta_experiences.append(delta)
        time_experience_sum = sum(delta_experiences)
        seller.set_total_experience_time(time_experience_sum)
        seller.buffer = copy.deepcopy(seller.experiences)
        total_intersection = cls.get_total_intersection(seller)
        seller.set_total_valid_experience_time((time_experience_sum - total_intersection) / 365)

    @classmethod
    def latest_experience_time(cls, seller):
        """
        :param seller: seller sent by request
        :return: time experience from the latest job
        """
        if len(seller.experiences) >= 1:
            latest_experience_time = cls.delta_experience_time(seller.experiences[0])
            seller.set_latest_experience_time(latest_experience_time)
        else:
            seller.set_latest_experience_time(0)

    @classmethod
    def previous_experience_time(cls, seller):
        """
        :param seller: seller sent by request
        :return: time experience from the penultimate job
        """
        if len(seller.experiences) > 1:
            previous_experience_time = cls.delta_experience_time(seller.experiences[1])
            seller.set_previous_experience_time(previous_experience_time)
        else:
            seller.set_previous_experience_time(0)

    @classmethod
    def percent_valid_experience_between_jobs(cls, seller):
        """
        :param seller: seller sent by request
        :return: of the total of experiences how many percent are valid
        """
        deltas = []
        if len(seller.experiences) >= 1:
            for exp in seller.experiences:
                delta = cls.delta_experience_time(exp)
                if delta >= 365:
                    deltas.append(delta)
            seller.set_percent_experiences_between_jobs(len(deltas) / len(seller.experiences))
        else:
            seller.set_percent_experiences_between_jobs(0)





