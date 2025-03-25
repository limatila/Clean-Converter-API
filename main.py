from os import getlogin, rename as renameFile
from pathlib import Path

#Downloading
import pytubefix as pytube
from pytubefix.cli import on_progress

#mp3 Conversion
import subprocess

def convert_to_mp3(input_path) -> Path: #Reliable.
    print("INFO: converting to MP3...")
    downloads_folder = Path.home() / "Downloads"
    output_file = downloads_folder / (Path(input_path).stem + ".mp3")

    command = [
        "ffmpeg", "-y",  # Overwrite without asking
        "-i", str(input_path),  # Input file
        "-vn",  # Remove video streams if present
        "-acodec", "libmp3lame",  # Use LAME MP3 encoder
        "-q:a", "2",  # High-quality variable bitrate (lower is better, range: 0-9)
        str(output_file)  # Output file
    ]
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    return output_file

#* Execution
url_download = str(input("Enter the video Url\t->")) 
yt_client = pytube.YouTube(url=url_download, on_progress_callback=on_progress)
if yt_client: print("INFO: Video found: " + yt_client.title)

yt_stream = yt_client.streams.get_audio_only()
downloaded_file = yt_stream.download("./temp-downloads/")
if downloaded_file: print("INFO: m4a downloaded.")

base_tempPath = downloaded_file

locationMp3 = convert_to_mp3(base_tempPath)

# result of success
print("Video has been successfully downloaded, in mp3: " + str(locationMp3))