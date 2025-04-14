from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse

from src.config import API_DETAILS
from src.services.validators import inputValidation
from src.services.validators.cookieValidation import validate_cookies
from src.services.youtubeDownloaders import download_mp3, download_mp4
from src.services.fileCompression import compress_single_file
from src.middleware.fileCount_management import account_for_usage
from src.middleware.loggers import requestsLogger

app = FastAPI (
    version=API_DETAILS['version'],
    title=API_DETAILS['name'],
    summary=API_DETAILS['summary'],
    description=API_DETAILS['description_md']
)

#! mp4 are downloading at 360 30fps maximum!
mp4_lowQualityMessage_md = """
<br>
**NOTE:** video downloads are available only at 360p, 30fps quality.
"""

@app.get("/download/mp3/", description="Downloads a URL's audio in mp3, in browser. Just put a video url in the input to download it (ETA: 20s)")
def get_in_mp3_audio(url: str, background: BackgroundTasks):
    requestsLogger.info(f"New GET request of /download/mp3 for: {url}")
    #for youtube urls: #? other may be added for other sources
    inputValidation.verify_youtube_url(url) 

    #Download
    downloadOutputPath = download_mp3(url)

    # success
    if downloadOutputPath:
        filename = downloadOutputPath.name
        #file usage management
        background.add_task(account_for_usage, downloadOutputPath)
        background.add_task(validate_cookies)

        return FileResponse(
            filename=filename,
            path=downloadOutputPath,
            media_type="audio/mpeg",
            headers={
                "result": "Video has been successfully delivered with .mp3.",
                "hint": "Just open the video with a compatible video player."
            }
        )
    else:
        raise HTTPException(status_code=500, detail="Could not resolve video conversion.")
    
@app.get("/download/mp4/", description="Downloads a URL's video, in browser. Just put a video url in the input to download it (ETA: 8s)" + mp4_lowQualityMessage_md)
def get_in_mp4_video(url: str, background: BackgroundTasks):
    requestsLogger.info(f"New GET request of /download/mp4 for: {url}")
    #for youtube urls: #? other may be added for other sources
    inputValidation.verify_youtube_url(url) 

    #Download
    downloadOutputPath = download_mp4(url)

    # success
    if downloadOutputPath:
        filename = downloadOutputPath.name
        #file usage management
        background.add_task(account_for_usage, downloadOutputPath)
        background.add_task(validate_cookies)

        return FileResponse(
            filename=filename,
            path=downloadOutputPath,
            media_type="video/mp4",
            headers={
                "result": "Video has been successfully delivered with .mp4.",
                "hint": "Just open the video with a compatible video player."
            }
        )
    else:
        raise HTTPException(status_code=500, detail="Could not resolve video conversion.")

@app.get("/compressed/mp3/", description="Downloads a URL's audio in a compressed file, in browser. Just put a video url in the input to download it (ETA: 20s)")
def get_compressed_in_mp3(url: str, background: BackgroundTasks):
    requestsLogger.info(f"New GET request of /compressed/mp3 for: {url}")
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

@app.get("/compressed/mp4/", description="Downloads a URL's video in a compressed file, in browser. Just put a video url in the input to download it (ETA: 20s)" + mp4_lowQualityMessage_md)
def get_compressed_in_mp4(url: str, background: BackgroundTasks):
    requestsLogger.info(f"New GET request of /compressed/mp4 for: {url}")
    #for youtube urls: #? other may be added for other sources
    inputValidation.verify_youtube_url(url) 

    #Download
    downloadOutputPath = download_mp4(url)

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
                "hint": "Please extract the .mp4 video to access your video"
            }
        )
    else:
        raise HTTPException(status_code=500, detail="Could not resolve video conversion.")


# startup
if __name__ == "__main__":
    validate_cookies()