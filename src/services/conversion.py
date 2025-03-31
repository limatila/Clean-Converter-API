from pathlib import Path

import ffmpeg #bindings libr, needs ffmpeg installed and in PATH

def convert_to_mp3(input_path: Path) -> Path: #Reliable.
    conversionFolderPath = Path("./temp-converted")
    if not conversionFolderPath.is_dir():
        conversionFolderPath.mkdir()

    newConvertedFilePath = str(input_path.stem + ".mp3")
    output_path = conversionFolderPath / newConvertedFilePath

    #if already existant conversion:
    if output_path.exists():
        print("INFO: conversion already exists, proceeding... ")
        return output_path

    print("INFO: converting to MP3...")
    conversionProcess = (
        ffmpeg.input(
                input_path, 
                format="m4a"
            ).output(
                str(output_path),
                format="mp3",
                vn= None, # -vn option, remove video frames
                acodec="libmp3lame", # -acodec option, conversion to .mp3
                aq= "2", # -q:a option with alias, lower number, better quality 
            ).overwrite_output() # -y option
            .run_async(pipe_stdout=True, pipe_stderr=True)
    )
    out, err = conversionProcess.communicate() 

    if conversionProcess.returncode == 0:
        return output_path # returns 
    else:
        print("-------Last Logs:\n", out.decode())
        raise Exception(f"Audio conversion failed on subprocess: {err.decode()}")