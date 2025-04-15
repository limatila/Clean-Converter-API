# For FastAPI BackgroundTasks: 'from fastapi import BackgroundTasks'
from json import load, dump, JSONDecodeError
from pathlib import Path

from src.config import (
    USAGE_REG_PATH_MP3, 
    USAGE_REG_PATH_MP4,
    USAGE_REG_INDENT,
    USAGE_REG_EXECUTIONS_KEY, 
    DEFAULT_FILE_EXTENSION,
    DEFAULT_COMPRESSION_EXTENSION,
    DOWNLOADS_FOLDER_PATH_MP3,
    DOWNLOADS_FOLDER_PATH_MP4,
    COMPRESSION_FOLDER_PATH,
)
from src.middleware.loggers import fileUsageLogger
from src.exceptions import FileUsageManagementError


#* On init, generate usage registrys
#mp3 reg
try:
    with open(USAGE_REG_PATH_MP3, 'r') as usage_json:
        usage_reg_mp3: dict[str, int] = load(usage_json)
except (FileNotFoundError, JSONDecodeError):
    usageJsonPath = Path(USAGE_REG_PATH_MP3)
    usageJsonPath.parent.mkdir(exist_ok=True, parents=True)
    usageJsonPath.write_text("")

    usage_reg_mp3: dict[str, int] = {}
    with open(usageJsonPath, 'w') as usage_json:
        dump(usage_reg_mp3, usage_json, indent=USAGE_REG_INDENT)

#mp4 reg
try:
    with open(USAGE_REG_PATH_MP4, 'r') as usage_json:
        usage_reg_mp4: dict[str, int] = load(usage_json)
except (FileNotFoundError, JSONDecodeError):
    usageJsonPath = Path(USAGE_REG_PATH_MP4)
    usageJsonPath.parent.mkdir(exist_ok=True, parents=True)
    usageJsonPath.write_text("")

    usage_reg_mp4: dict[str, int] = {}
    with open(usageJsonPath, 'w') as usage_json:
        dump(usage_reg_mp4, usage_json, indent=USAGE_REG_INDENT)

#also, gen count of total executions (var and file)
#mp3 reg
try:
    totalExecutionCount: int = usage_reg_mp3[ USAGE_REG_EXECUTIONS_KEY ]
except KeyError:
    totalExecutionCount: int = 0
    with open(USAGE_REG_PATH_MP3, 'w') as usage_json: #also update it
        usage_reg_mp3.update({USAGE_REG_EXECUTIONS_KEY: totalExecutionCount})
        dump(usage_reg_mp3, usage_json, indent=USAGE_REG_INDENT)

#mp4 reg
try:
    totalExecutionCount: int = usage_reg_mp4[ USAGE_REG_EXECUTIONS_KEY ]
except KeyError:
    totalExecutionCount: int = 0
    with open(USAGE_REG_PATH_MP4, 'w') as usage_json: #also update it
        usage_reg_mp4.update({USAGE_REG_EXECUTIONS_KEY: totalExecutionCount})
        dump(usage_reg_mp4, usage_json, indent=USAGE_REG_INDENT)


#* Management functions
def delete_stored_files(filename: str, fileExtension: str = DEFAULT_FILE_EXTENSION, compressedExtension: str = DEFAULT_COMPRESSION_EXTENSION):
    toDelete: list[Path] = []
    
    #getting and checking files
    match(fileExtension):
        case ".mp3":
            file_downloaded: Path = DOWNLOADS_FOLDER_PATH_MP3 / (filename + fileExtension)
            if file_downloaded.exists(): toDelete.append(file_downloaded)
        case ".mp4":
            file_downloaded: Path = DOWNLOADS_FOLDER_PATH_MP4 / (filename + fileExtension)
            if file_downloaded.exists(): toDelete.append(file_downloaded)
        case _:
            message = "File Deletion Service > file extension is not compatible, please verify execution (video/audio was not deleted.)"
            fileUsageLogger.error(message)
    
    file_compressed: Path = COMPRESSION_FOLDER_PATH / (filename + compressedExtension)
    if file_compressed.exists(): toDelete.append(file_compressed)

    #deleting mp3
    for file in toDelete:
        try:
            file.unlink()
        except FileNotFoundError:
            fileUsageLogger.warning(f"File Deletion Service > file was not found at deletion point: {file}") 
        finally: continue

    #resetting count on file
    match(fileExtension):
        case ".mp3":
            update_usage_registry(usage_reg_mp4, {filename: 0})
            fileUsageLogger.info(f"File Deletion Service > audio files was deleted for: {filename}")
        case ".mp4":
            update_usage_registry(usage_reg_mp4, {filename: 0})
            fileUsageLogger.info(f"File Deletion Service > video files was deleted for: {filename}")

#TODO: this def is forces too much boilerplate, it should be refactored ASAP
def update_usage_registry(reg_to_update: dict, entry: dict[str, int]):
    reg_to_update.update(entry)

    if reg_to_update is usage_reg_mp3:
        with open(USAGE_REG_PATH_MP3, 'w') as usage_json: #also update it
            dump(reg_to_update, usage_json, indent=USAGE_REG_INDENT)
    elif reg_to_update is usage_reg_mp4: 
        with open(USAGE_REG_PATH_MP4, 'w') as usage_json: #also update it
            dump(reg_to_update, usage_json, indent=USAGE_REG_INDENT)
    else: 
        message = "usage_reg to update is falty, please verify execution."
        fileUsageLogger.warning(message)

def check_file_usage(filename: str, fileExtension: str):
    # call delete_stored_files() if file is not so much used (less than 4 times), every 20th request (max 20x +-10MB music)
    match(fileExtension):
        case ".mp3":
            if ( (totalExecutionCount % 20) == 0 and totalExecutionCount != 0 ):
                for name in usage_reg_mp3:
                    if (usage_reg_mp3[name] <= 4 and name != filename and name != USAGE_REG_EXECUTIONS_KEY):
                        delete_stored_files(name, fileExtension)
        case ".mp4":
            if ( (totalExecutionCount % 20) == 0 and totalExecutionCount != 0 ):
                for name in usage_reg_mp4:
                    if (usage_reg_mp4[name] <= 4 and name != filename and name != USAGE_REG_EXECUTIONS_KEY):
                        delete_stored_files(name, fileExtension)
        case _: 
            message = f"File Usage Management > file extension found for file {filename + fileExtension} is not compatible, please verify execution."
            fileUsageLogger.error(message)
            raise FileUsageManagementError(message)

#* Usage behavior logic
#TODO: too much boilerplate, shall be refactored after its dependencies!
def account_for_usage(file_path: Path):
    global totalExecutionCount, usage_reg_mp3, usage_reg_mp4

    file_downloaded = file_path
    filename = str(file_downloaded.stem)
    fileExtension = str(file_downloaded.suffix)

    # add count to entry
    match(fileExtension):
        case ".mp3": 
            try:
                countFileUsage: int = usage_reg_mp3[ filename ]
            except KeyError:
                usage_reg_mp3.update({str(filename): 0}) #starts at 0 usage
                countFileUsage: int = usage_reg_mp3[ filename ]
        case ".mp4":
            try:
                countFileUsage: int = usage_reg_mp4[ filename ]
            except KeyError:
                usage_reg_mp4.update({str(filename): 0}) #starts at 0 usage
                countFileUsage: int = usage_reg_mp4[ filename ]
        case _:
            message = f"File Usage Management > file extension found for file {file_downloaded.name} is not compatible, please verify execution."
            fileUsageLogger.error(message)
            raise FileUsageManagementError(message)


    countFileUsage += 1    #! This cant be permanent. Must account for days since last usage

    match(fileExtension):
        case ".mp3":
            # add entry update to usage_reg
            update_usage_registry(usage_reg_mp3, {filename: countFileUsage})

            # add +1 executedTimes to registry
            totalExecutionCount += 1
            update_usage_registry(usage_reg_mp3, {USAGE_REG_EXECUTIONS_KEY: totalExecutionCount})

        case ".mp4":
            update_usage_registry(usage_reg_mp4, {filename: countFileUsage})

            totalExecutionCount += 1
            update_usage_registry(usage_reg_mp4, {USAGE_REG_EXECUTIONS_KEY: totalExecutionCount})
        # case _ is already with.

    check_file_usage(filename, fileExtension)
