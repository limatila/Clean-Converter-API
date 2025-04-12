from yt_dlp import YoutubeDL
from pathlib import Path

from src.services.validators.cookieValidation import validate_cookies

from src.config import YDL_OPTS
from src.config import DOWNLOADS_FOLDER_PATH
from src.middleware.loggers import fileUsageLogger

DOWNLOADS_FOLDER_PATH.mkdir(exist_ok=True)

#*- to mp3
def download_mp3(url: str, _retry_flag: bool = False) -> Path:
    try:
        with YoutubeDL(YDL_OPTS['SINGLE_MP3']) as ydl:
            video = ydl.extract_info(url, download=True)
            file_path = Path(ydl.prepare_filename(video)).with_suffix('.mp3')
        fileUsageLogger.debug(f"File Download Service > new file was compressed: {file_path}")
    except Exception as err:
        if not _retry_flag:
            validate_cookies()  # check if cookies was corrupted
            return download_mp3(url=url, _retry_flag=True)
        else:
            fileUsageLogger.error(f"File Download Service > error during file download process: {err.__class__.__name__}. Check uvicorn logs!")
            raise err
        
    #sucess 
    #BUG: some characters in video titles are bugged out when downloading, like ':', so it will return a RuntimeError
    validate_cookies() #? later add this as a decorator
    return file_path #returns full path in str
    
#*- in mp4