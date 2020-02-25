from functools import partial
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

from fastapi import APIRouter, FastAPI
from starlette.responses import UJSONResponse

from conf import DEBUG
from services.schemas import ErrorResponse


def make_app(*args: Any, **kwargs: Any) -> FastAPI:
    kwargs.setdefault('docs_url', '/api')
    kwargs.setdefault('debug', DEBUG)
    kwargs.setdefault('openapi_url', '/api/openapi.json')
    return FastAPI(*args, **kwargs)


class APIResponse(UJSONResponse):
    def render(self, content: Any) -> bytes:
        # Customize response here
	return super().render(content)


class Api(APIRouter):
    def api_route(self, *args: Any, **kwargs: Any) -> Callable[..., Any]:  # pylint: disable=W0221
        kwargs.setdefault('response_class', APIResponse)
        return super().api_route(*args, **kwargs)


def Error(error: Union[str, Dict, List, Tuple], code: int = 400) -> UJSONResponse:  # noqa
    return UJSONResponse(status_code=code, content=ErrorResponse(ok=False, error=error).dict())


PermissionsError = partial(Error, code=403)
NotFoundError = partial(Error, code=404)


class ResponsesContainer(dict):
    default_responses = {400: {'model': ErrorResponse, 'description': 'General error'}}
    permissions_error = (
        403,
        {
            'model': ErrorResponse,
            'description': 'User does not have permissions to perform this action',
        },
    )
    not_found_error = (
        404,
        {'model': ErrorResponse, 'description': 'Requested resource was not found'},
    )
    errors_dict = {'permissions': permissions_error, 'not_found': not_found_error}

    def __init__(self) -> None:
        dict.__init__(self, self.default_responses)

    def extra(self, extra: Optional[List[str]] = None) -> Dict[int, Dict]:
        result_responses = self.default_responses.copy()
        if extra:
            for key in extra:
                response = self.errors_dict.get(key)
                if not response:
                    continue
                result_responses[response[0]] = response[1]
        return result_responses


# basic usage: `@api.post(..., responses=responses)`. Error response 400 with ErrorResponse model is added by default
# `@api.post(..., responses=responses.extra('not_found')` - will add 404 code to default reponses
# You can add new responses to the ResponsesContainer above
responses = ResponsesContainer()
