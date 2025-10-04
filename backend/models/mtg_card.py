from pydantic import BaseModel

class MTGCard(BaseModel):
    name: str
    set_name: str
    price: float
    store: str
    url: str
