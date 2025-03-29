from pathlib import Path

from pytubefix import YouTube
from pytubefix.cli import on_progress

def download_raw_audio(url: str) -> Path:
    yt_Client = YouTube(url, on_progress_callback=on_progress)
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
    