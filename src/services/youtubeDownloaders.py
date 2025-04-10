from yt_dlp import YoutubeDL
from pathlib import Path

from src.services.cookieValidation import validate_cookies

def download_mp3(url: str) -> Path:
    downloads_folder_path = Path("./temp-downloads")
    downloads_folder_path.mkdir(exist_ok=True)

    ydl_opts = {
        'format': 'mp3/bestaudio/best',
        'outtmpl': str(downloads_folder_path / '%(title)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'cookiefile': 'cookies.txt',  # Path to your cookies file
        'no_write_cookies': True,
        'noplaylist': True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        video = ydl.extract_info(url, download=True)
        file_path = Path(ydl.prepare_filename(video)).with_suffix('.mp3')

    validate_cookies() #Check at least once, will be checked later also.

    #sucess 
    #BUG: some characters in video titles are bugged out when downloading, like ':', so it will return a RuntimeError
    return file_path #returns full path in str #TODO: change to a local Path
    
