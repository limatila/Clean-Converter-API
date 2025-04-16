from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import RedirectResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from src.routers import *
from src.config import API_DETAILS
from src.services.validators.cookieValidation import validate_cookies
from src.middleware.requestLimiters import ipLimiter

app = FastAPI (
    version=API_DETAILS['version'],
    title=API_DETAILS['name'],
    summary=API_DETAILS['summary'],
    description=API_DETAILS['description_md']
)
app.state.limiter = ipLimiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

app.include_router(downloads_router)
app.include_router(compressions_router)

@app.get('/', description="redirects Root url to Documentation page", include_in_schema=False)
def root_redirect(request: Request):
    return RedirectResponse("/docs", headers={"result": "redirected to Documentation page (at \'/docs\')"})

# startup
if __name__ == "__main__":
    validate_cookies()