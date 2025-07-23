import os
import tkinter as tk
from tkinter import filedialog, messagebox
from pytube import YouTube
import subprocess

def download_video():
    url = url_entry.get()
    only_audio = audio_var.get()
    if not url:
        messagebox.showerror("Error", "Please enter a YouTube URL")
        return

    try:
        yt = YouTube(url)
        if only_audio:
            stream = yt.streams.filter(only_audio=True).first()
        else:
            stream = yt.streams.get_highest_resolution()

        output_path = filedialog.askdirectory(title="Select Download Folder")
        if not output_path:
            return

        downloaded_file = stream.download(output_path=output_path)

        if only_audio:
            base, ext = os.path.splitext(downloaded_file)
            mp3_file = base + ".mp3"
            ffmpeg_path = os.path.join(os.getcwd(), "ffmpeg.exe")

            command = [ffmpeg_path, "-i", downloaded_file, mp3_file]
            subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            os.remove(downloaded_file)

        messagebox.showinfo("Success", "Download completed!")
    except Exception as e:
        messagebox.showerror("Error", str(e))

app = tk.Tk()
app.title("SH Downloader")
app.geometry("400x200")

tk.Label(app, text="YouTube URL:").pack(pady=10)
url_entry = tk.Entry(app, width=50)
url_entry.pack()

audio_var = tk.BooleanVar()
tk.Checkbutton(app, text="Audio Only (MP3)", variable=audio_var).pack()

tk.Button(app, text="Download", command=download_video).pack(pady=20)

app.mainloop()
