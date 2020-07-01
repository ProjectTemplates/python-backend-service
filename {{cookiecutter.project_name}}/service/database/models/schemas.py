from pydantic import BaseModel


class ORMSchema(BaseModel):
    class Config:
        orm_mode = True
