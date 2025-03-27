from pathlib import Path
from subprocess import run, PIPE

def convert_to_mp3(input_path: str) -> Path: #Reliable.
    print("INFO: converting to MP3...")

    conversionFolderPath = Path("./temp-converted")
    if not conversionFolderPath.is_dir():
        conversionFolderPath.mkdir()

    newConvertedFilePath = (Path(input_path).stem + ".mp3")
    output_file = conversionFolderPath / newConvertedFilePath

    #TODO: implement ffmpeg-python binding libr
    command = [
        "ffmpeg", "-y",           # Overwrite without asking
        "-i", str(input_path),    # Input file
        "-vn",                    # Remove video streams if present
        "-acodec", "libmp3lame",  # Use LAME MP3 encoder
        "-q:a", "2",              # High-quality variable bitrate (lower is better, range: 0-9)
        str(output_file)          # Output file
    ]
    processConversion = run(command, stdout=PIPE, stderr=PIPE)

    if processConversion.returncode == 0:
        return output_file
    else:
        raise Exception(f"Audio conversion failed on subprocess: {processConversion.stderr.decode()}")