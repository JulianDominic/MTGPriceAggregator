import uvicorn
from litestar import Litestar
from controller import CardListController, SearchController

app = Litestar(route_handlers=[CardListController, SearchController])

if __name__ == "__main__":
    uvicorn.run(app, port=10016, host="localhost")
