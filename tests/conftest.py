import pytest
from unittest.mock import patch

@pytest.fixture(autouse=True)
def mock_kafka_publicar():
    with patch("app.routers.routers.publicar_evento") as mock_pub:
        mock_pub.return_value = True
        yield mock_pub