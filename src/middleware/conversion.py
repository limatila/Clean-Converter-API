from pathlib import Path

from subprocess import run, PIPE

def convert_to_mp3(input_path) -> Path: #Reliable.
    print("INFO: converting to MP3...")

    downloadsFolderPath = Path.home() / "Downloads"
    output_file = downloadsFolderPath / (Path(input_path).stem + ".mp3")

    command = [
        "ffmpeg", "-y",  # Overwrite without asking
        "-i", str(input_path),  # Input file
        "-vn",  # Remove video streams if present
        "-acodec", "libmp3lame",  # Use LAME MP3 encoder
        "-q:a", "2",  # High-quality variable bitrate (lower is better, range: 0-9)
        str(output_file)  # Output file
    ]
    run(command, stdout=PIPE, stderr=PIPE)

    return output_file