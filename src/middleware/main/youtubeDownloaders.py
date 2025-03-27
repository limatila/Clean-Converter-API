from pytubefix import YouTube
from pytubefix.cli import on_progress

def download_raw_audio(url: str):
    yt_Client = YouTube(url, on_progress_callback=on_progress)
    tempDownloadsFolder = "./temp-downloads/" #path to temp files

    if yt_Client: 
        print("INFO: Video found: " + yt_Client.title)

    yt_AudioStream = yt_Client.streams.get_audio_only()
    downloadedFilePath = yt_AudioStream.download(tempDownloadsFolder)
    if downloadedFilePath: 
        print("INFO: m4a downloaded.")

    return downloadedFilePath