from pydantic import BaseModel

class QueryFilter(BaseModel):
    start: str = None
    end: str = None