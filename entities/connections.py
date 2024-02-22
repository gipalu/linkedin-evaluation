import re
from entities.utils import get_number_in_string


class Connections:

    @staticmethod
    def connection_number(text: str):
        """
        :param text: text that brings the connections
        :return: int number of connections
        """
        return get_number_in_string(text)