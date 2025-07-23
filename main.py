import os
import urllib.request
import zipfile

def download_ffmpeg():
    ffmpeg_url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
    ffmpeg_zip = "ffmpeg.zip"
    ffmpeg_exe_path = "ffmpeg.exe"

    # Check if ffmpeg.exe already exists
    if os.path.isfile(ffmpeg_exe_path):
        print("ffmpeg.exe found.")
        return

    print("Downloading ffmpeg...")
    urllib.request.urlretrieve(ffmpeg_url, ffmpeg_zip)

    print("Extracting ffmpeg...")
    with zipfile.ZipFile(ffmpeg_zip, 'r') as zip_ref:
        for file in zip_ref.namelist():
            if file.endswith("ffmpeg.exe") and "bin/" in file:
                zip_ref.extract(file, ".")
                os.rename(file, ffmpeg_exe_path)
                break

    os.remove(ffmpeg_zip)
    print("ffmpeg.exe downloaded and ready.")

# Call it at the start of the script
download_ffmpeg()
