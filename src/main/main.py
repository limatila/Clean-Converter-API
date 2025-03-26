from os import getlogin, rename as renameFile

from middleware.conversion import *
from middleware.youtube import *

if __name__ == "__main__":
    downloadOutputPath = download_raw_audio
    locationMp3 = convert_to_mp3(downloadOutputPath)
    
    # success
    print("Video has been successfully saved, in .mp3: " + str(locationMp3))
