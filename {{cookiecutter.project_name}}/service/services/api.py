from functools import partial
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

from fastapi import APIRouter, FastAPI, HTTPException
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
        if isinstance(content, dict) and 'ok' in content:
            return super().render(content)
        return super().render({'ok': True, 'data': content})


class Api(APIRouter):
    def api_route(self, *args: Any, **kwargs: Any) -> Callable[..., Any]:  # pylint: disable=W0221
        kwargs.setdefault('response_class', APIResponse)
        return super().api_route(*args, **kwargs)


class Error(HTTPException):
    error: Optional[Union[str, Dict, List]] = None
    status_code: int = 400
    error_code: str = 'Error'

    def __init__(self, *args, **kwargs):
        if self.error is None:
            if len(args) == 1 and not kwargs:
                self.error = args[1]
            else:
                raise ValueError(
                    'Provide only error message or set default error template in error class to use arguments'
                )
        else:
            self.error = self.error.format(*args, **kwargs)

    def render(self):
        return UJSONResponse(
            status_code=self.status_code,
            content=ErrorResponse(ok=False, error=self.error, error_code=self.error_code).dict(),
        )


class PermissionsError(Error):
    status_code = 403
    error_code = 'INVALID_PERMISSIONS'


class NotFoundError(Error):
    status_code = 404
    error_code = 'NOT_FOUND'


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

    def __call__(self, extra: Optional[List[str]] = None) -> Dict[int, Dict]:
        result_responses = self.default_responses.copy()
        if extra:
            for key in extra:
                response = self.errors_dict.get(key)
                if not response:
                    continue
                result_responses[response[0]] = response[1]
        return result_responses


# basic usage: `@api.post(..., responses=responses)`. Error response 400 with ErrorResponse model is added by default
# `@api.post(..., responses=responses('not_found'))` - will add 404 code to default reponses
# You can add new responses to the ResponsesContainer above
responses = ResponsesContainer()
