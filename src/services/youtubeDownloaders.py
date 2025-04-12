from yt_dlp import YoutubeDL
from pathlib import Path

from src.services.validators.cookieValidation import validate_cookies

from src.config import YDL_OPTS
from src.config import DOWNLOADS_FOLDER_PATH

DOWNLOADS_FOLDER_PATH.mkdir(exist_ok=True)


#*- to mp3
def download_mp3(url: str) -> Path:
    with YoutubeDL(YDL_OPTS['SINGLE_MP3']) as ydl:
        video = ydl.extract_info(url, download=True)
        file_path = Path(ydl.prepare_filename(video)).with_suffix('.mp3')

    validate_cookies() #? later add this as a decorator

    #sucess 
    #BUG: some characters in video titles are bugged out when downloading, like ':', so it will return a RuntimeError
    assert file_path.exists() #! need testing
    return file_path #returns full path in str
    
#*- in mp4