from entities.seller import Seller
from entities.utils import get_words


class Education:

    @staticmethod
    def get_valid_education(seller: Seller):
        """
        :param seller: seller sent by request
        :return: if seller has a valid experience
        """
        universities = get_words('universities', 'brasil_public_universities')
        initials = get_words('universities', 'initials')
        degree = get_words('universities', 'degree')
        validity = 0
        if seller.education:
            for edu in seller.education:
                if edu.get('schoolName'):
                    university_validity = 1 if edu.get('schoolName') in universities or edu.get('schoolName') in initials else 0
                else:
                    university_validity = 0
                if edu.get('degreeName'):
                    degree_validity = 1 if edu.get('degreeName').lower() in [name.lower() for name in degree] else 0
                else:
                    degree_validity = 0
                if university_validity == 1 and degree_validity == 1:
                    validity += 1
        seller.set_education_validity(validity)



