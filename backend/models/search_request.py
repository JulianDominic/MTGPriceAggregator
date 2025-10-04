from pydantic import BaseModel
from typing import List

class SearchRequest(BaseModel):
    cardName: str
    stores: List[str]
