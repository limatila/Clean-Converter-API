
# functions that check cookie usage, as requests are added

from src.config import (
    COOKIES_FILE_PATH, 
    COOKIES_BACKUP_FILE_PATH
)
from src.middleware.loggers import cookiesLogger

#should run one per request, to be correctly used
def update_cookies():
    with open(COOKIES_BACKUP_FILE_PATH, 'r') as backup:
        with open(COOKIES_FILE_PATH, 'w') as cookies:
            backupLines = backup.read()
            cookies.write(backupLines)
            cookiesLogger.info(f"Changes in {COOKIES_FILE_PATH} detected; Cookiefile was updated with backup.")
            

def validate_cookies():
    with open(COOKIES_FILE_PATH, 'r') as cookies:
        with open(COOKIES_BACKUP_FILE_PATH, 'r') as backup:
            currentLines = cookies.read()
            backupLines = backup.read()
            if currentLines != backupLines: update_cookies()