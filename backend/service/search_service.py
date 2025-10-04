import aiohttp
import asyncio
from typing import List
from lgs import GamesHaven, OneMTG, AgoraHobby, FlagshipGames, CardsCitadel, GreyOgreGames, Hideout, MTGAsia, ScrapeMTG

STORE_MAPPING = {
    "GamesHaven": GamesHaven,
    "OneMTG": OneMTG,
    "AgoraHobby": AgoraHobby,
    "FlagshipGames": FlagshipGames,
    "CardsCitadel": CardsCitadel,
    "GreyOgreGames": GreyOgreGames,
    "Hideout": Hideout,
    "MTGAsia": MTGAsia
}

class SearchService():
    def validate_input(self, card_name: str, selected_stores: List[str]):
        if (card_name is None or not card_name):
            raise Exception("Card name is empty. Card name must be provided.")
        
        if (selected_stores is None or not selected_stores):
            raise Exception("No store was selected. At least one store must be selected.")
            
        
    async def get_cards(self, client, site_instance:ScrapeMTG):
        print("Fetching for", site_instance.__class__.__name__)
        success = await site_instance.fetch(client)
        print("Finished fetching for", site_instance.__class__.__name__)
        if not(success):
            return None
        return await site_instance.get_card_info()

    async def get_prices(self, card_name: str, stores: List[str]):
        instances = [STORE_MAPPING[store](card_name) for store in stores]
        
        results = None
        async with aiohttp.ClientSession() as client:
            all_store_cards = [self.get_cards(client, site_instance) for site_instance in instances]
            results = await asyncio.gather(*all_store_cards)
        
        if (results is None):
            raise Exception("Internal Server Error")
        
        all_cards = []
        for result in results:
            if result is not None:
                all_cards.extend(result)

        return all_cards     
