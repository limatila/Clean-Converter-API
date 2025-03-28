from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse

from src.middleware.conversion import *
from src.services.youtubeDownloaders import *

app = FastAPI(version="0.1", title="Clean Converter API",
              description="Mp3 downloader only, for now.")

@app.get(f"/v{app.version}" + "/download/mp3/")
async def get_video_in_mp3(url: str):

    #TODO: apply condition for "mp3 or mp4 already exists" and imeddiatly returns. #! should result in a race condition, so need to account for that also!
    downloadOutputPath = download_raw_audio(url)
    locationMp3 = convert_to_mp3(downloadOutputPath)
    filenameMp3 = str(locationMp3.stem) + ".mp3"

    # success
    if locationMp3:
        return FileResponse(
            filename=filenameMp3,
            path=locationMp3,
            media_type="audio/mpeg",
            headers={
                "result": "Video has been successfully converted to .mp3"
            }
        )
        # return {
        #     "result": "Video has been successfully saved, in .mp3",
        #     "location": locationMp3
        # }
    else:
        return HTTPException(status_code=500, detail="Could not resolve video conversion.")