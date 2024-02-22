from entities.seller import Seller

class DescriptionExperience:

    @staticmethod
    def set_description_experience_size(seller: Seller):
        """
        :param seller: seller sent by request
        :return: of the total descriptions experience how many has the valid size
        """
        final_descriptions = []
        for description in seller.experiences_description:
            description_size = len(description)
            if description_size >= 90:
                final_descriptions.append(description)
        if final_descriptions:
            seller.set_percent_description_experience_size(len(final_descriptions) / len(seller.experiences_description))
        else:
            seller.set_percent_description_experience_size(0)

    @staticmethod
    def set_last_experience_size(seller: Seller):
        """
        :param seller: seller sent by request
        :return: size of the last description text
        """
        if seller.experiences_description:
            last_exp = seller.experiences_description[0]
            seller.set_last_description_experience_size(len(last_exp))
        else:
            seller.set_last_description_experience_size(0)