import aiohttp
import asyncio
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
from lgs import GamesHaven, OneMTG, AgoraHobby, FlagshipGames, CardsCitadel, GreyOgreGames, Hideout, ScrapeMTG, MTGAsia

class CardRequest(BaseModel):
    cardName: str
    stores: List[str]

class APIResponse(BaseModel):
    success: bool
    errorMessage: str
    cards: List[Dict[str, str]]

app = FastAPI()

origins = [
    "localhost", "http://localhost", "http://localhost:10015"
]

origins_regex = "http://192.168.*.*"

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
    "Hideout": Hideout,
    "MTGAsia": MTGAsia
}

async def get_cards(client, site_instance:ScrapeMTG):
    print("Fetching for", site_instance.__class__.__name__)
    success = await site_instance.fetch(client)
    print("Finished fetching for", site_instance.__class__.__name__)
    if not(success):
        return None
    return await site_instance.get_card_info()

def validate_input(card_name: str, selected_stores: List[str]):
    errorMessage = ""
    if (card_name is None or not card_name):
        errorMessage = "Card name is empty. Card name must be provided."
    elif (selected_stores is None or not selected_stores):
        errorMessage = "No store was selected. At least one store must be selected."
    
    if (errorMessage):
        raise HTTPException(status_code=400, detail=errorMessage)


@app.post("/search", response_model=APIResponse)
async def search_card(card_request: CardRequest):
    card_name = card_request.cardName
    selected_stores = card_request.stores

    response = {
        "success": True,
        "errorMessage": "",
        "cards": []
    }

    # Check for valid input
    try:
        validate_input(card_name, selected_stores)
    except HTTPException as e:
        response["success"] = False
        response["errorMessage"] = e.detail
        return response

    instances = [store_mapping[store](card_name) for store in selected_stores]

    results = None
    async with aiohttp.ClientSession() as client:
        all_store_cards = [get_cards(client, site_instance) for site_instance in instances]
        results = await asyncio.gather(*all_store_cards)
    
    # Check if there was some kind of server error
    if (results is None):
        response["success"] = False
        response["errorMessage"] = "Some internal server error occured"
        return response

    all_cards = []
    for result in results:
        if result is not None:
            all_cards.extend(result)

    # Check if there was any card found at all
    if (not all_cards):
        response["success"] = False
        response["errorMessage"] = f"\"{card_name}\" is not available in any of the stores selected."
    else:
        response["cards"] = all_cards

    return response

if __name__ == '__main__':
    import uvicorn
    # This line only matters if you are doing `python app.py`
    uvicorn.run(app, host="0.0.0.0", port=10016)
