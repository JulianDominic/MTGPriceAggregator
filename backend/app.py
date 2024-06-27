import aiohttp
import asyncio
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
from lgs import GamesHaven, OneMTG, AgoraHobby, FlagshipGames, CardsCitadel, GreyOgreGames, Hideout, ScrapeMTG

class CardRequest(BaseModel):
    cardName: str
    stores: List[str]

app = FastAPI()

origins = [
    "localhost", "http://localhost", "http://localhost:10015"
]

origins_regex = "http://192\.168\.*\.*"

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex=origins_regex,
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)

store_mapping = {
    "GamesHaven": GamesHaven,
    "OneMTG": OneMTG,
    "AgoraHobby": AgoraHobby,
    "FlagshipGames": FlagshipGames,
    "CardsCitadel": CardsCitadel,
    "GreyOgreGames": GreyOgreGames,
    "Hideout": Hideout
}

@app.post("/search", response_model=List[Dict[str, str]])
async def search_card(card_request: CardRequest):
    card_name = card_request.cardName
    selected_stores = card_request.stores
    
    if not card_name:
        raise HTTPException(status_code=400, detail="Card name must be provided")
    
    if not selected_stores:
        raise HTTPException(status_code=400, detail="At least one store must be selected")

    instances = [store_mapping[store](card_name) for store in selected_stores]

    async def get_cards(client, site_instance:ScrapeMTG):
        print("Fetching for", site_instance.__class__.__name__)
        success = await site_instance.fetch(client)
        print("Finished fetching for", site_instance.__class__.__name__)
        if not(success):
            return None
        return await site_instance.get_card_info()
    
    async with aiohttp.ClientSession() as client:
        all_store_cards = [get_cards(client, site_instance) for site_instance in instances]
        results = await asyncio.gather(*all_store_cards)
    
    all_cards = []
    for result in results:
        if result is not None:
            all_cards.extend(result)

    if not all_cards:
        raise HTTPException(status_code=404, detail="No cards found")

    return all_cards

if __name__ == '__main__':
    import uvicorn
    # This line only matters if you are doing `python app.py`
    uvicorn.run(app, host="0.0.0.0", port=10016)
