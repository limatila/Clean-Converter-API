
# functions for request validation, returns HTTPException with details of validation error

from fastapi import HTTPException

def verify_youtube_url(url: str) -> HTTPException | None:
    if not ("youtube.com/watch?v=" in url
            or "youtu.be/" in url):
        raise HTTPException(status_code=400, detail={
                "error": "youtube video could not be resolved, please insert a valid youtube video url.",
                "example": "https://youtube.com/watch?v=\'random string here\'"
            })
