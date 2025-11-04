import uvicorn
from litestar import Litestar
from controller import CardListController, SearchController
from config import MTGCORSConfig

app = Litestar(
    route_handlers=[CardListController, SearchController],
    cors_config=MTGCORSConfig(),
    path="/api/v1"
    )

if __name__ == "__main__":
    uvicorn.run(app, port=10016, host="0.0.0.0")
