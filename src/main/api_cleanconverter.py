from fastapi import FastAPI

from middleware.conversion import *
from services.youtubeDownloaders import *

app = FastAPI(version="0.1", title="Clean Converter API",
              description="Mp3 downloader only, for now.")

@app.get(f"/{app.version}" + "/download/mp3/{url_inserted}")
def get_video_in_mp3(url_inserted: str):
    downloadOutputPath = download_raw_audio(url_inserted)
    locationMp3 = convert_to_mp3(downloadOutputPath)
    
    # success
    print("Video has been successfully saved, in .mp3: " + str(locationMp3))
