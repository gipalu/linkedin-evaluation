import pytest
from loguru import logger
import spacy

from entities.key_words import KeyWords
from entities.utils import key_words_count


class TestUtils:
    @pytest.mark.parametrize(
            "key_words, expected",
            [
                ('Pleno pleno', 2),
                ('Pleno pleno PLENO plleno', 3),
                ('pleno dois', 1),
                ('pleno pleno', 2),
                ('pleno pleno PLENO', 3)
            ])
    def test_key_words_count(self, key_words, expected):
        nlp = spacy.load('pt_core_news_sm')
        words = ['Pleno', 'PLENO', 'pleno']
        result = key_words_count(nlp, key_words, words)
        logger.info(result)
        assert result == expected