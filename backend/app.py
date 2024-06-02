from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
from lgs import GamesHaven, OneMTG, AgoraHobby, FlagshipGames, CardsCitadel, GreyOgreGames, Hideout, ScrapeMTG

class CardRequest(BaseModel):
    cardName: str
    stores: List[str]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost"],
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

    response = {}
    for site_instance in instances:
        site_instance:ScrapeMTG
        results:dict = site_instance.get_card_info(site_instance.status_code)
        if results is not None:
            query_url = results["url"]
            cards = results["cards"]
            if cards:
                response[site_instance.__name__] = {
                    "url": query_url,
                    "cards": cards,
                }

    if not response:
        raise HTTPException(status_code=404, detail="No cards found")

    return response

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
