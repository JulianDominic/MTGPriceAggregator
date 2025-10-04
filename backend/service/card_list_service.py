import json, os, requests
from datetime import datetime, timedelta
from models import CardListItem
from typing import List

MASTER_CARD_LIST_PATH = "scryfall_card_names.json"
CACHE_DURATION = timedelta(hours=24)

class CardListService():
    def is_valid_cache(self) -> bool:
        if not os.path.exists(MASTER_CARD_LIST_PATH):
            return False
        modified_time = datetime.fromtimestamp(os.path.getmtime(MASTER_CARD_LIST_PATH))
        return datetime.now() - modified_time < CACHE_DURATION
    
    async def get_card_list(self, force:bool) -> List[CardListItem]:
        if (not force and self.is_valid_cache()):
            print("Local file found.")
            with open(MASTER_CARD_LIST_PATH, "r", encoding="utf-8") as file:
                card_names = json.load(file)
                return card_names
        
        print("Pulling cards from Scryfall API")
        try:
            response = requests.get("https://api.scryfall.com/catalog/card-names", timeout=10)
            response.raise_for_status()
            scryfall_data:dict = response.json()
            temp_card_names = scryfall_data.get("data", [])
            card_names = []
            for idx, card_name in enumerate(temp_card_names):
                card_list_item = CardListItem(
                    id=idx,
                    name=card_name
                )
                card_names.append(card_list_item)
            # Save only the card names (not full metadata)
            if (os.path.exists(MASTER_CARD_LIST_PATH)):
                os.remove(MASTER_CARD_LIST_PATH)
            with open(MASTER_CARD_LIST_PATH, "w", encoding="utf-8") as f:
                json.dump(card_names, f)
            return card_names

        except requests.RequestException:
            raise Exception("Failed to fetch from Scryfall")
