from pathlib import Path

import ffmpeg #bindings libr, needs ffmpeg installed and in PATH

def convert_to_mp3(input_path: str) -> Path: #Reliable.
    conversionFolderPath = Path("./temp-converted")
    if not conversionFolderPath.is_dir():
        conversionFolderPath.mkdir()

    newConvertedFilePath = (Path(input_path).stem + ".mp3")
    output_path = conversionFolderPath / newConvertedFilePath

    #TODO: add condition if file exists

    print("INFO: converting to MP3...")
    conversionProcess = (
        ffmpeg.input(
                input_path, 
                format="m4a"
            ).output(
                str(output_path),
                vn= None, # -vn option, remove video frames
                acodec="libmp3lame", 
                aq= "2", # -q:a option with alias, lower number, better quality 
            ).overwrite_output() # -y option
            .run_async(pipe_stdout=True, pipe_stderr=True)
    )
    out, err = conversionProcess.communicate() 

    if conversionProcess.returncode == 0:
        return output_path
    else:
        print("-------Last Logs:\n", out.decode())
        raise Exception(f"Audio conversion failed on subprocess: {err.decode()}")