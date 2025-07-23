
import sys
import os
import threading
import time
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from yt_dlp import YoutubeDL
import pyperclip

# Default download folder
DOWNLOAD_FOLDER = os.path.join(os.path.expanduser("~"), "Downloads")

class DownloaderApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SH Download")
        self.geometry("500x400")
        self.resizable(False, False)
        self.create_widgets()
        self.check_clipboard()

    def create_widgets(self):
        # URL Input
        tk.Label(self, text="YouTube URL:").pack(pady=5)
        self.url_var = tk.StringVar()
        self.url_entry = tk.Entry(self, textvariable=self.url_var, width=60)
        self.url_entry.pack(pady=5)

        # Download Folder
        folder_frame = tk.Frame(self)
        folder_frame.pack(pady=5)
        tk.Label(folder_frame, text="Download Folder:").pack(side="left")
        self.folder_var = tk.StringVar(value=DOWNLOAD_FOLDER)
        self.folder_entry = tk.Entry(folder_frame, textvariable=self.folder_var, width=40)
        self.folder_entry.pack(side="left", padx=5)
        tk.Button(folder_frame, text="Browse", command=self.choose_folder).pack(side="left")

        # Format Selection
        self.audio_only = tk.BooleanVar()
        tk.Checkbutton(self, text="Audio Only", variable=self.audio_only).pack(pady=5)

        # Quality Selection
        tk.Label(self, text="Quality (e.g. 1080, 720, best):").pack()
        self.quality_var = tk.StringVar(value="best")
        tk.Entry(self, textvariable=self.quality_var).pack(pady=5)

        # Progress bar
        self.progress = ttk.Progressbar(self, mode="determinate")
        self.progress.pack(fill="x", padx=10, pady=10)

        # Download Button
        tk.Button(self, text="Download", command=self.start_download_thread).pack(pady=5)

        # Status Label
        self.status_label = tk.Label(self, text="Ready", fg="green")
        self.status_label.pack(pady=5)

    def choose_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_var.set(folder)

    def check_clipboard(self):
        try:
            clip = pyperclip.paste()
            if clip.startswith("http"):
                self.url_var.set(clip)
        except:
            pass

    def start_download_thread(self):
        threading.Thread(target=self.download_video).start()

    def download_video(self):
        url = self.url_var.get().strip()
        out_dir = self.folder_var.get().strip()
        quality = self.quality_var.get().strip()

        if not url:
            messagebox.showerror("Error", "URL cannot be empty")
            return

        self.status_label.config(text="Downloading...", fg="blue")
        self.progress.start()

        ydl_opts = {
            'outtmpl': os.path.join(out_dir, '%(title)s.%(ext)s'),
            'progress_hooks': [self.hook],
        }

        if self.audio_only.get():
            ydl_opts['format'] = 'bestaudio/best'
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        else:
            ydl_opts['format'] = f'bestvideo[height<={quality}]+bestaudio/best'

        try:
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            self.status_label.config(text="Download Complete", fg="green")
        except Exception as e:
            self.status_label.config(text=f"Error: {e}", fg="red")
        finally:
            self.progress.stop()

    def hook(self, d):
        if d['status'] == 'downloading':
            p = d.get('_percent_str', '0.0%').strip()
            self.status_label.config(text=f"Downloading: {p}", fg="blue")
        elif d['status'] == 'finished':
            self.status_label.config(text="Merging...", fg="orange")

if __name__ == "__main__":
    app = DownloaderApp()
    app.mainloop()
