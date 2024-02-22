# TODO pegar variação das palavras

import spacy
import io

from entities.seller import Seller
from entities.utils import get_words
from entities.utils import key_words_count


class KeyWords:
    nlp = spacy.load('pt_core_news_sm')

    @classmethod
    def set_sellers_key_words_count(cls, seller: Seller):
        """
        :param seller: seller sent by request
        :return: dict with how many key words have from each filename
        """
        result = {}
        fields = ['recommendations_comments', 'summary', 'experiences_title', 'experiences_description', 'certifications_title']
        filenames = ['leadership', 'pleno', 'senior', 'technical_coordination']
        for filename in filenames:
            counter = 0
            words = get_words('key_words', filename)
            for field in fields:
                seller_attr = getattr(seller, field)
                if seller_attr:
                    if type(seller_attr) == list:
                        for text in seller_attr:
                            counter += key_words_count(cls.nlp, text, words)
                    else:
                        counter += key_words_count(cls.nlp, seller_attr, words)
            result[filename] = counter
        seller.set_key_words_count(result)




