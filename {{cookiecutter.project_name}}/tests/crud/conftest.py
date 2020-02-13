import pytest

from services.dependencies import get_db


@pytest.fixture()
def session():
    yield from get_db()
