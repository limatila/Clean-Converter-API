#Configurations for the project (mainly: names and paths)

from pathlib import Path
from dotenv import load_dotenv as load_envfile  #TODO

#Downloaders
DOWNLOADS_FOLDER_PATH = Path("./temp-downloads")
YDL_OPTS: dict[str, any] = {
        'format': 'bestaudio/best',
        'outtmpl': str(DOWNLOADS_FOLDER_PATH / '%(title)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'cookiefile': 'cookies.txt',  # Path to your cookies file
        'overwrites': False,
        'noplaylist': True,
        'age_limit': 20,
        'wait_for_video': (0, 86400) #For lives that didn't finish (but will), will wait for 24hours for it to finish.
}

#Cookies for youtube client
COOKIES_FILE_PATH = "cookies.txt"
COOKIES_BACKUP_FILE_PATH = "backup-cookies.txt"

#File usage registry
USAGE_REG_PATH = "./src/logs/usage-reg.json"
USAGE_REG_INDENT = 2
USAGE_REG_EXECUTIONS_KEY = "executedTimes"
DEFAULT_FILE_EXTENSION = ".mp3"