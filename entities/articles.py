from entities.seller import Seller

class Articles:
    @staticmethod
    def get_articles_number(seller: Seller):
        """
        :param seller: seller sent by request
        :return: quantity of articles from the seller
        """
        quantity = len(seller.articles)
        seller.set_articles_quantity(quantity)