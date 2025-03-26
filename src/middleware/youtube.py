from pytubefix import YouTube
from pytubefix.cli import on_progress

def download_raw_audio():
    urlToDownload = str(input("Enter the video Url\t->")) 

    yt_Client = YouTube(url=urlToDownload, on_progress_callback=on_progress)
    if yt_Client: 
        print("INFO: Video found: " + yt_Client.title)

    yt_AudioStream = yt_Client.streams.get_audio_only()
    downloadedFilePath = yt_AudioStream.download("./temp-downloads/")
    if downloadedFilePath: 
        print("INFO: m4a downloaded.")

    return downloadedFilePath