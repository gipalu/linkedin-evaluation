import pytest
from entities.connections import Connections
from entities.loader import loader

class TestConnections:

    @pytest.mark.parametrize(
        "text, expected",
        [
            ('50 conexões', 50),
            ('+ de 500 conexões', 500)
        ])
    def test_connection_number(self, text, expected):
        result = Connections.connection_number(text)
        assert result == expected

