
# functions for request validation, returns HTTPException with details of validation error

from fastapi import HTTPExcepetion

def verify_youtube_url(url: str): -> HTTPException | None:
    if url.contains("youtube.com/watch?v="):
        return HTTPException(status_code=400, detail="youtube video could not be resolved, please insert a valid youtube video url.")
