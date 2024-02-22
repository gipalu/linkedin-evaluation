from entities.seller import Seller

class Summary:

    @staticmethod
    def summary_size(seller: Seller):
        """
        :param seller: seller sent by request
        :return: number of characters in summary
        """
        summary_size = len(seller.summary)
        seller.set_summary_size(summary_size)

