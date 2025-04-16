from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse, RedirectResponse 
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi

from src.middleware.requestLimiters import ipLimiter

swagger_router = APIRouter(include_in_schema=False)


@swagger_router.get('/', description="redirects Root url to Documentation page")
@ipLimiter.limit('1/second')
def root_redirect(request: Request):
    return RedirectResponse("/docs", headers={"result": "redirected to Documentation page (at \'/docs\')"})

@swagger_router.get("/docs")
@ipLimiter.limit('1/second')
def docs(request: Request):
    return get_swagger_ui_html(openapi_url="/openapi.json", title="YCC Docs")

@swagger_router.get("/openapi.json")
@ipLimiter.limit('1/second')
def openapi(request: Request):
    return JSONResponse(get_openapi(title=swagger_router.title, version=swagger_router.version, routes=swagger_router.routes))
