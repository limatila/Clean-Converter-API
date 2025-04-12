# File compression scripts, to provide less data usage
from pathlib import Path

# from archivefile import ArchiveFile
from py7zr import SevenZipFile as SZip

from src.config import COMPRESSION_FOLDER_PATH, DEFAULT_COMPRESSION_EXTENSION
from src.middleware.loggers import fileUsageLogger

COMPRESSION_FOLDER_PATH.mkdir(exist_ok=True)

def compress_single_file(file_path: Path, compressionExtension: str = DEFAULT_COMPRESSION_EXTENSION) -> Path:
    try:
        assert file_path.exists()
    except AssertionError:
        fileUsageLogger.error(f"File Compression Service > file to compress could not be found at: {file_path}")
        raise AssertionError

    #get folder of path
    outputZipPath = COMPRESSION_FOLDER_PATH / (file_path.stem + compressionExtension)

    try:
        with SZip(outputZipPath, 'w') as zipfile:
            zipfile.write(file_path)
        
        assert outputZipPath.exists()
        fileUsageLogger.debug(f"File Compression Service > new file was compressed: {outputZipPath}")
    except Exception as err:
        fileUsageLogger.error(f"File Compression Service > error during file compression process: {err.__class__.__name__}. Check uvicorn logs!")
        raise err

    return outputZipPath

#? def compressPlaylistFiles