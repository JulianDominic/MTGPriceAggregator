from litestar import Controller, get, post, put, patch, delete
from litestar.dto import DTOData
from litestar.exceptions import HTTPException
from models import SearchRequest, SearchResponse
from service import SearchService
from typing import List

class SearchController(Controller):
    path = "/search"
    
    def __init__(self):
        self.search_service = SearchService()
    
    @get(path="/")
    async def search(self, card_name:str, stores:List[str]) -> SearchResponse:
        try:
            self.search_service.validate_input(card_name, stores)
            
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=e.__str__(),
            )
            
        all_cards = []
        try:
            all_cards = self.search_service.get_prices(card_name, stores)
            return SearchResponse(
                cards=all_cards
            )
            
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=e.__str__(),
            )
