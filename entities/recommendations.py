from entities.seller import Seller

class Recommendations:
    @staticmethod
    def set_recommendations_quantity(seller: Seller):
        """
        :param seller: seller sent by request
        :return: quantity of recommendations
        """
        quantity = len(seller.recommendations_received)
        seller.set_recommendations_quantity(quantity)

    @staticmethod
    def set_recommendations_size(seller: Seller):
        """
        :param seller: seller sent by request
        :return: of the total of recommendations how many has valid size
        """
        final_recs = []
        for rec in seller.recommendations_comments:
            rec_size = len(rec)
            if rec_size >= 100:
                final_recs.append(rec)
        if final_recs:
            seller.set_percent_recommendations_right_size(len(final_recs) / len(seller.recommendations_comments))
        else:
            seller.set_percent_recommendations_right_size(0)

    @staticmethod
    def compare_recommendations_received_and_sent(seller):
        """
        :return: recommendation multiplier for comparation between send and received recommendations
        """
        received = len(seller.recommendations_received)
        sent = len(seller.recommendations_sent)
        if sent:
            multiplier = 0.75 if received / sent < 1 else 1
        else:
            multiplier = 1
        seller.set_recommendations_multiplier(multiplier)