from pydantic import BaseModel
from typing import List

class CardListItem(BaseModel):
    id: int
    name: str

class CardListResponse(BaseModel):
    card_names: List[CardListItem]
