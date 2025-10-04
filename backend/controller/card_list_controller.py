from litestar import Controller, get
from litestar.exceptions import HTTPException
from models import CardListResponse
from service import CardListService

class CardListController(Controller):
    path = "/cards"
    card_list_service = CardListService()
    
    @get(path="/all")
    async def get_all_cards(self, force: bool) -> CardListResponse:
        try:
            card_names = await self.card_list_service.get_card_list(force)
            return CardListResponse(card_names=card_names)
        
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=e.__str__(),
            )
        