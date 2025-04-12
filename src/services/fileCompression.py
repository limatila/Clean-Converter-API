# File compression scripts, to provide less data usage
from pathlib import Path

# from archivefile import ArchiveFile
from py7zr import SevenZipFile as SZip
from src.config import COMPRESSION_FOLDER_PATH, DEFAULT_COMPRESSION_EXTENSION

def compress_single_file(file_path: Path, compressionExtension: str = DEFAULT_COMPRESSION_EXTENSION) -> Path:
    assert file_path.exists() #TODO: Log assertion error

    #get folder of path
    outputZipPath = COMPRESSION_FOLDER_PATH / (file_path.stem + compressionExtension)

    with SZip(outputZipPath, 'w') as zipfile:
        zipfile.write(file_path)

    assert outputZipPath.exists() #! need testing
    return outputZipPath

#? def compressPlaylistFiles