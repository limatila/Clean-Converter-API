
# functions that check cookie usage, as requests are added

#Constants
COOKIES_FILE_PATH = "cookies.txt"
COOKIES_BACKUP_FILE_PATH = "backup-cookies.txt"

#should run one per request, to be correctly used
def update_cookies():
    with open(COOKIES_BACKUP_FILE_PATH, 'r') as backup:
        with open(COOKIES_FILE_PATH, 'w') as cookies:
            backupLines = backup.read()
            cookies.write(backupLines)
            #TODO: log updates
            

def validate_cookies():
    with open(COOKIES_FILE_PATH, 'r') as cookies:
        with open(COOKIES_BACKUP_FILE_PATH, 'r') as backup:
            currentLines = cookies.read()
            backupLines = backup.read()
            if currentLines != backupLines: update_cookies()