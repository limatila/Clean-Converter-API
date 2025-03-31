from pathlib import Path

from pytubefix import YouTube
from pytubefix.cli import on_progress
from pytubefix.exceptions import RegexMatchError, VideoUnavailable
from fastapi import HTTPException

def download_raw_audio(url: str) -> Path:
    try:
        yt_Client = YouTube(url, on_progress_callback=on_progress)
    except RegexMatchError:
        raise HTTPException(status_code=400, detail={
            "error": "the video url is invalid, please copy a proper video url from youtube client",
            "inserted_link": url
        })
    except VideoUnavailable:
        raise HTTPException(status_code=404, detail={
            "error": "Youtube video was not found with the inserted link.",
            "inserted_link": url,
            "hint": "try using another link, you can copy it from any youtube video"
        })
    except:
        raise HTTPException(status_code=500, detail="Your video could not be resolved by the download service. Please try another video url!")

    downloadsFolderPath = Path("./temp-downloads/") #path to temp files
    if not downloadsFolderPath.is_dir():
        downloadsFolderPath.mkdir()

    if yt_Client: 
        print("INFO: Video found: " + yt_Client.title)

    yt_AudioStream = yt_Client.streams.get_audio_only()

    #if already existant conversion:
    existantFilePath = downloadsFolderPath / (yt_Client.title + ".m4a")
    if existantFilePath.exists():
        print("INFO: video already is downloaded, proceeding... ")
        return existantFilePath
    else:
        downloadedFilePath = yt_AudioStream.download(downloadsFolderPath)

    #sucess
    if downloadedFilePath: 
        print("INFO: m4a downloaded.")
        assert existantFilePath.exists() #TODO: log the assertion error
        return existantFilePath #returns full path in str #TODO: change to a local Path
    