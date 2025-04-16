from src.routers.downloads import downloads_router
from src.routers.compressions import compressions_router
from src.routers.customSwagger import swagger_router

__all__: list[str] = [
    'downloads_router',
    'compressions_router',
    'swagger_router'
    #other more routers here
]