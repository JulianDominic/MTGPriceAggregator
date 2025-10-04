from pydantic import BaseModel
from typing import List, Dict

class SearchResponse(BaseModel):
    cards: List[Dict[str, str]]
