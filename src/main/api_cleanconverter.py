from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse

from src.services import inputValidation
from src.services.conversion import convert_to_mp3
from src.services.youtubeDownloaders import download_raw_audio
from src.main.fileCount_management import account_for_usage

app = FastAPI(version="0.1", title="Clean Converter API",
              description="An API for automatic download and conversion of Youtube videos. Mp3 downloader only, for now.")

@app.get(f"/v{app.version}" + "/download/mp3/")
def get_in_mp3(url: str, background: BackgroundTasks):
    #for youtube urls: #? other may be added for other sources
    inputValidation.verify_youtube_url(url) 

    #Download
    downloadOutputPath = download_raw_audio(url)

    #Convert
    locationMp3 = convert_to_mp3(downloadOutputPath)

    #get Filename from conversion
    filenameMp3 = str(locationMp3.name)

    # success
    if locationMp3:
        #file usage management
        background.add_task(account_for_usage, [downloadOutputPath, locationMp3])

        return FileResponse(
            filename=filenameMp3,
            path=locationMp3,
            media_type="audio/mpeg",
            headers={
                "result": "Video has been successfully delivered with .mp3"
            }
        )
    else:
        raise HTTPException(status_code=500, detail="Could not resolve video conversion.")
