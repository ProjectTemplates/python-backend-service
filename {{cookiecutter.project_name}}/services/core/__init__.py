from typing import Any, Callable

from fastapi.exceptions import RequestValidationError
from starlette.requests import Request
from starlette.responses import Response, StreamingResponse, UJSONResponse

from conf import DEBUG
from services.api import make_app

app = make_app()


@app.exception_handler(RequestValidationError)
def type_error_handler(request: Request, exc: RequestValidationError) -> UJSONResponse:
    return UJSONResponse(status_code=422, content={'ok': False, 'error': exc.args})


@app.middleware('http')
async def log_and_trace(request: Request, call_next: Callable[[Request], Any]) -> Response:
    response: StreamingResponse = await call_next(request)
    # Here you can place logging, tracing headers
    return response


from .routes import *  # pylint: disable=C0413  # isort:skip

app.include_router(api, tags=['api'], prefix='/api')

if DEBUG:
    from starlette.middleware.cors import CORSMiddleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
        expose_headers=['*']
    )
