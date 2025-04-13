from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse

from src.services.validators import inputValidation
from src.services.validators.cookieValidation import validate_cookies
from src.services.youtubeDownloaders import download_mp3
from src.services.fileCompression import compress_single_file
from src.middleware.fileCount_management import account_for_usage

app = FastAPI(version="1.1", title="Youtube Clean Converter",
              description=(
                    "## An API for automatic download and conversion of Youtube videos.\n Mp3 downloader only, for now.\n" +
                    "## NOTE:\n you should note that this API doesn't have a HTTPS certificate, but use it in mind that IT SHOULD ONLY download MP3 files."), 
             )

@app.get(f"/v{app.version}" + "/download/mp3/", description="Downloads given URL's audio, in browser. Just put a video url in the input to download it (ETA: 20s)")
def get_in_mp3(url: str, background: BackgroundTasks):
    #for youtube urls: #? other may be added for other sources
    inputValidation.verify_youtube_url(url) 

    #Download
    downloadOutputPath = download_mp3(url)

    #Compression
    compressedOutputPath = compress_single_file(downloadOutputPath)

    # success
    if downloadOutputPath:
        filename = compressedOutputPath.name
        #file usage management
        background.add_task(account_for_usage, downloadOutputPath)
        background.add_task(validate_cookies)

        return FileResponse(
            filename=filename,
            path=compressedOutputPath,
            media_type="application/x-7z-compressed",
            headers={
                "result": "Video has been successfully delivered with .mp3, and compressed for delivery.",
                "hint": "Please extract the .mp3 audio to access your audio"
            }
        )
    else:
        raise HTTPException(status_code=500, detail="Could not resolve video conversion.")


# startup
if __name__ == "__main__":
    validate_cookies()