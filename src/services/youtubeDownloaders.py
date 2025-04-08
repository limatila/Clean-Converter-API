import subprocess
from pathlib import Path

from yt_dlp import YoutubeDL
from fastapi import HTTPException

def download_mp3(url: str) -> Path:
    downloadsFolderPath = Path("./temp-downloads")

    if not downloadsFolderPath.is_dir():
        downloadsFolderPath.mkdir()

    download_args: list = [
        "yt-dlp",                                 #downloader
        "-x",                                       #only audio
        "--audio-format=mp3",                       #audio format
        f"-P \"./{str(downloadsFolderPath)}/\"",       #path to download
        "-o %(title)s", #template for filename
        url                                         #url by client
    ]

    #if already existant download:
    with YoutubeDL() as ydl:
        videoInfo: dict = ydl.extract_info(url, download=False)
    # existantFilePath = downloadsFolderPath / (videoInfo['title'] + f" [{ videoInfo['id'] }]" + ".mp3")
    existantFilePath = downloadsFolderPath / (videoInfo['title'] + ".mp3")
    if existantFilePath.exists():
        print("INFO: video is already downloaded, proceeding... ")
        return existantFilePath
    else:
        subprocess.call(" ".join(download_args))

    #sucess 
    #BUG: some characters in video titles are bugged out when downloading, like ':', so it will return a RuntimeError
    return existantFilePath #returns full path in str #TODO: change to a local Path
    