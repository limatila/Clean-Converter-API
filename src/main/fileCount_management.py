# For FastAPI BackgroundTasks: 'from fastapi import BackgroundTasks'
from json import load, dump
from pathlib import Path

#Constants
USAGE_REG_FILENAME = "usage-reg.json"
USAGE_REG_INDENT = 2
USAGE_REG_EXECUTIONS_KEY = "executedTimes"


#on start, gen usage_reg
try:
    with open(USAGE_REG_FILENAME, 'r') as usage_json:
        usage_reg: dict[str, int] = load(usage_json)
except FileNotFoundError:
    with open(USAGE_REG_FILENAME, 'w') as usage_json:
        usage_reg: dict[str, int] = {}
        dump(usage_reg, usage_json, indent=USAGE_REG_INDENT)

#also, gen count of total executions on registry...
try:
    totalExecutionCount: int = usage_reg[ USAGE_REG_EXECUTIONS_KEY ]
except KeyError:
    with open(USAGE_REG_FILENAME, 'w') as usage_json: #also update it
        usage_reg.update({USAGE_REG_EXECUTIONS_KEY: 0})
        dump(usage_reg, usage_json, indent=USAGE_REG_INDENT)
    totalExecutionCount: int = 0


#* Management functions
def delete_stored_files(filename: str, fileExtension: str, converted: bool = True):
    toDelete: list[Path] = []
    defaultFileExtension_downloads = ".m4a"

    #getting and checking files
    #TODO: log assertion errors
    file_downloaded: Path = Path("./temp-downloads") / (filename + defaultFileExtension_downloads)
    toDelete.append(file_downloaded)

    if converted: #False if you don't want to delete the .mp3 converted file
        file_converted: Path = Path("./temp-converted") / (filename + fileExtension)
        toDelete.append(file_converted)

    #deleting them
    for file in toDelete:
        file.unlink(missing_ok=True)   #TODO: log FileNotFound error
    #resetting count on file
    update_usage_registry({filename: 0})

def update_usage_registry(entry: dict[str, int]):
    """Function to update var 'usage_reg' & file on path 'USAGE_REG_FILENAME' 

    Args:
        entry (dict[str, int]): a dict with 'filename' or 'USAGE_REG_EXECUTIONS_KEY' as key, and a number on its value
    """
    usage_reg.update(entry)
    with open(USAGE_REG_FILENAME, 'w') as usage_json: #also update it
        dump(usage_reg, usage_json, indent=USAGE_REG_INDENT)
        
def account_for_usage(files_paths: list[Path]):
    global totalExecutionCount, usage_reg

    file_downloaded, file_converted = files_paths
    filename = str(file_converted.stem)
    fileExtension = str(file_converted.suffix)

    # add count to entry #? should do this on if/else ?
    try:
        countFileUsage: int = usage_reg[ filename ]
    except KeyError:
        usage_reg.update({str(filename): 0}) #starts at 0 usage
        countFileUsage: int = usage_reg[ filename ]
    
    countFileUsage += 1     #TODO: this cant be permanent. Must account for days since last usage

    # add entry update to usage_reg
    update_usage_registry({filename: countFileUsage})

    # add +1 executedTimes to registry
    totalExecutionCount += 1
    update_usage_registry({USAGE_REG_EXECUTIONS_KEY: totalExecutionCount})
    
    # call delete_stored_files() if file is not so much used, every 20th request (max 20x +-10MB music)
    if ( (totalExecutionCount % 20) == 0 and totalExecutionCount != 0 ):
        for name in usage_reg:
            if (usage_reg[name] <= 4 and name != filename and name != USAGE_REG_EXECUTIONS_KEY):
                delete_stored_files(name, fileExtension)
