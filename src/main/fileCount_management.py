# For FastAPI BackgroundTasks: 'from fastapi import BackgroundTasks'
from json import load, dump, JSONDecodeError
from pathlib import Path

from src.config import (
    USAGE_REG_PATH, 
    USAGE_REG_INDENT,
    USAGE_REG_EXECUTIONS_KEY, 
    DEFAULT_FILE_EXTENSION
)

#On Start, generate usage_reg
try:
    with open(USAGE_REG_PATH, 'r') as usage_json:
        usage_reg: dict[str, int] = load(usage_json)
except (FileNotFoundError, JSONDecodeError):
    with open(USAGE_REG_PATH, 'w') as usage_json:
        usage_reg: dict[str, int] = {}
        dump(usage_reg, usage_json, indent=USAGE_REG_INDENT)

#also, gen count of total executions (var and file)
try:
    totalExecutionCount: int = usage_reg[ USAGE_REG_EXECUTIONS_KEY ]
except KeyError:
    with open(USAGE_REG_PATH, 'w') as usage_json: #also update it
        usage_reg.update({USAGE_REG_EXECUTIONS_KEY: 0})
        dump(usage_reg, usage_json, indent=USAGE_REG_INDENT)
    totalExecutionCount: int = 0


#* Management functions
def delete_stored_files(filename: str, fileExtension: str = DEFAULT_FILE_EXTENSION):
    #getting and checking files
    #TODO: log assertion errors
    file_downloaded: Path = Path("./temp-downloads") / (filename + fileExtension)

    #deleting mp3
    file_downloaded.unlink(missing_ok=True)   #TODO: log FileNotFound error

    #resetting count on file
    update_usage_registry({filename: 0})

def update_usage_registry(entry: dict[str, int]):
    """Function to update var 'usage_reg' & file on path 'USAGE_REG_FILENAME' 

    Args:
        entry (dict[str, int]): a dict with 'filename' or 'USAGE_REG_EXECUTIONS_KEY' as key, and a number on its value
    """
    usage_reg.update(entry)
    with open(USAGE_REG_PATH, 'w') as usage_json: #also update it
        dump(usage_reg, usage_json, indent=USAGE_REG_INDENT)

#* Usage behavior logic
def account_for_usage(file_path: Path):
    global totalExecutionCount, usage_reg

    file_downloaded = file_path
    filename = str(file_downloaded.stem)
    fileExtension = str(file_downloaded.suffix)

    # add count to entry #? should do this on if/else ?
    try:
        countFileUsage: int = usage_reg[ filename ]
    except KeyError:
        usage_reg.update({str(filename): 0}) #starts at 0 usage
        countFileUsage: int = usage_reg[ filename ]
    
    countFileUsage += 1    #! This cant be permanent. Must account for days since last usage

    # add entry update to usage_reg
    update_usage_registry({filename: countFileUsage})

    # add +1 executedTimes to registry
    totalExecutionCount += 1
    update_usage_registry({USAGE_REG_EXECUTIONS_KEY: totalExecutionCount})
    
    #? should i refactor this?
    # call delete_stored_files() if file is not so much used, every 20th request (max 20x +-10MB music)
    if ( (totalExecutionCount % 20) == 0 and totalExecutionCount != 0 ):
        for name in usage_reg:
            if (usage_reg[name] <= 4 and name != filename and name != USAGE_REG_EXECUTIONS_KEY):
                delete_stored_files(name, fileExtension)
