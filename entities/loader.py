import json
import glob
import os

from entities.seller import Seller

def loader(seller):
    """
    :param seller: specific seller in payloads field
    :return: seller payload
    """
    with open(f'entities/data/payloads/{seller}.json', encoding="utf8") as json_data:
        payload = json.load(json_data)
    return payload

def load_seller(seller_1):
    """
    :param seller_1: specific seller payload
    :return: seller 1 builded
    """
    seller = Seller()
    seller.build(loader(seller_1))
    seller.get_recommendations_comments(loader(seller_1))
    seller.get_certifications_title(loader(seller_1))
    seller.get_experiences_fields(loader(seller_1))
    return seller