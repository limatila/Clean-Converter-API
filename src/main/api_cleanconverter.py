from fastapi import FastAPI, HTTPException

from src.middleware.conversion import *
from src.services.youtubeDownloaders import *

app = FastAPI(version="0.1", title="Clean Converter API",
              description="Mp3 downloader only, for now.")

@app.get(f"/v{app.version}" + "/download/mp3/")
def get_video_in_mp3(url: str):
    downloadOutputPath = download_raw_audio(url)
    locationMp3 = convert_to_mp3(downloadOutputPath)

    if not locationMp3:
        return HTTPException(status_code=500, detail="Could not resolve video conversion.")
    
    # success
    return {
        "result": "Video has been successfully saved, in .mp3",
        "location": locationMp3
    }