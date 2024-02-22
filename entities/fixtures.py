import pytest
from entities.loader import loader
from entities.seller import Seller
from entities.experience import Experience


@pytest.fixture
def seller_1():
    seller = Seller()
    seller.build(loader("seller_1"))
    seller.get_experiences_fields(loader("seller_1"))
    seller.get_recommendations_comments(loader("seller_1"))
    seller.get_certifications_title(loader("seller_1"))
    return seller

@pytest.fixture
def seller_2():
    """
    :return: seller with all fields empty
    """
    seller = Seller()
    seller.build(loader("seller_2"))
    seller.get_experiences_fields(loader("seller_2"))
    seller.get_recommendations_comments(loader("seller_2"))
    seller.get_certifications_title(loader("seller_2"))
    return seller

@pytest.fixture
def seller_3():
    """
    :return: seller with all fields empty
    """
    seller = Seller()
    seller.build(loader("seller_1"))
    seller.get_experiences_fields(loader("seller_1"))
    Experience.set_experience(seller)
    Experience.title_validity(seller)
    additional_experience = {'userId': '6250bfa19c17cf7ae989c41d',
                             'level': 8,
                             'startDate': '2020-06-02',
                             'endDate': '2020-06-10',
                             'title': 'Specialist Developer',
                             'description': 'Promote technical improvements and restructuring the Educational Technology team, and supporting/developing front-end with Vue and Back with Node and PHP, react'
                             }
    seller.experiences.append(additional_experience)
    return seller

@pytest.fixture
def seller_4():
    """
    :return: seller with only the first item in seller_1 fields
    """
    seller = Seller()
    seller.build(loader("seller_4"))
    seller.get_experiences_fields(loader("seller_4"))
    seller.get_recommendations_comments(loader("seller_4"))
    seller.get_certifications_title(loader("seller_4"))
    return seller

@pytest.fixture
def seller_5():
    """
    :return: seller with only the first item in seller_1 fields
    """
    seller = Seller()
    seller.build(loader("seller_5"))
    seller.get_experiences_fields(loader("seller_5"))
    seller.get_recommendations_comments(loader("seller_5"))
    seller.get_certifications_title(loader("seller_5"))
    return seller

@pytest.fixture
def seller_6():
    """
    :return: seller with only the first item in seller_1 fields
    """
    seller = Seller()
    seller.build(loader("seller_6"))
    seller.get_experiences_fields(loader("seller_6"))
    seller.get_recommendations_comments(loader("seller_6"))
    seller.get_certifications_title(loader("seller_6"))
    return seller
