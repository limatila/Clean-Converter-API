
#* Configurations for the project (mainly: names and paths)

from pathlib import Path

#Cookies for youtube client
COOKIES_FILE_PATH = "cookies.txt"
COOKIES_BACKUP_FILE_PATH = "backup-cookies.txt"

#Download and Compression configuration
DOWNLOADS_FOLDER_PATH_MP3 = Path("./temp-mp3-downloads")
DOWNLOADS_FOLDER_PATH_MP4 = Path("./temp-mp4-downloads")
COMPRESSION_FOLDER_PATH = Path("./temp-compressions") 

QUIET_EXECUTION_OPTION: bool = True #no logs from yt-dlp if True

YDL_OPTS: dict[ str, dict[str, any]] = {
    #a group of yt-dlp options to be used in downloads methods.
    #shall be used in 'YoutubeDL(YDL_OPTS['your-option'])'.
    'SINGLE_MP3': {
        'format': 'bestaudio/best',
        'outtmpl': str(DOWNLOADS_FOLDER_PATH_MP3 / '%(title)s.temp'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'cookiefile': COOKIES_FILE_PATH,
        'noplaylist': True,
        'age_limit': 20,
        'wait_for_video': (0, 86400), #For lives that didn't finish (but will), will wait for 24hours for it to finish.
        'quiet': QUIET_EXECUTION_OPTION
    },
    'SINGLE_MP4': {
        'format': 'best[ext=mp4]/best',
        'outtmpl': str(DOWNLOADS_FOLDER_PATH_MP4 / '%(title)s.%(ext)s'),
        'cookiefile': COOKIES_FILE_PATH,
        'noplaylist': True,
        'age_limit': 20,
        'merge_output_format': 'mp4',
        'wait_for_video': (0, 86400),
        'quiet': QUIET_EXECUTION_OPTION
    }
    # 'MULTIPLE_MP3': 
}

#File usage registry
USAGE_REG_PATH = "./src/logs/usage-reg.json"
USAGE_REG_INDENT = 2
USAGE_REG_EXECUTIONS_KEY = "executedTimes"
DEFAULT_FILE_EXTENSION = ".mp3"
DEFAULT_COMPRESSION_EXTENSION = '.7z'

#* Logger configuration (paths and formats)
BASE_LOGS_PATH: str = "./src/logs/"
defaultFormatter = '#API_LOG > %(asctime)s - %(levelname)s - %(message)s'

#DateTime configs
defaultTimezone = "-03:00"
defaultTimeFormat = "%d-%m(%y) %H:%M:%S"
