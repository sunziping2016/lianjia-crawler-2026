from pydantic import BaseModel


class District(BaseModel):
    name: str
    url: str


class State(BaseModel):
    districts: list[District] | None = None
