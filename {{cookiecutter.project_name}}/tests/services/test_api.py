# Example tests, for basic stuff from this project

from services.api import responses


def test_responses():
    assert len(responses) == 1
    assert 400 in responses  # default error response


def test_extra_responses():
    extra = responses.extra(['permissions', 'not_found'])
    assert len(extra) == 3
    assert 400 in extra
    assert 403 in extra
    assert 404 in extra
