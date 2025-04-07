import subprocess
from pathlib import Path

from fastapi import HTTPException

def download_raw_audio(url: str) -> Path:
    download_args = [
        "yt-dlp",                               #downloader
        "-x",                                   #only audio
        "--audio-format mp3",                   #audio format
        "o \"./\""
        url                                     #url by client
    ]

    #if already existant download:
    existantFilePath = 
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
    