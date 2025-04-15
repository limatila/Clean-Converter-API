
# functions for request validation, returns HTTPException with details of validation error

from fastapi import HTTPException

URL_PATTERNS = [
    "youtube.com/watch?v=", 
    "youtu.be/",
    "youtube.com/shorts/",
    "m.youtube.com/shorts/"
]

def verify_youtube_url(url: str) -> HTTPException | None:
    for pattern in URL_PATTERNS:
        if pattern in url:
            return None
    
    raise HTTPException(status_code=400, detail={
            "error": "youtube video could not be resolved, please insert a valid youtube video url.",
            "example": "https://youtube.com/watch?v=\'random string here\'"
        })
