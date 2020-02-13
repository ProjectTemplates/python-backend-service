from typing import Dict, List, Union

from pydantic import BaseModel


class ErrorResponse(BaseModel):
    ok: bool = False
    error: Union[str, Dict, List] = 'Unknown error'


class ORMModel(BaseModel):  # inherit all models from this one
    class Config:
        orm_mode = True
