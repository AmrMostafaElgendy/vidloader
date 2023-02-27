import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from pytube import YouTube
from tkinter import ttk


def download_video():
    try:
        video = YouTube(url_entry.get())
        streams = video.streams.filter(progressive=True)
        stream_info = [(s.resolution, s.fps, s.filesize//(1024*1024)) for s in streams]
        stream_listbox.delete(0, tk.END)
        for info in stream_info:
            stream_listbox.insert(tk.END, f"{info[0]} {info[1]}fps {info[2]}MB")
        stream_listbox.selection_clear(0, tk.END)
        stream_listbox.select_set(0)
        stream_listbox.activate(0)
        root.video = video
    except:
        messagebox.showerror("Error", "Invalid video URL or no video streams available")


def select_directory():
    directory = filedialog.askdirectory()
    if directory:
        directory_entry.delete(0, tk.END)
        directory_entry.insert(0, directory)


def start_download():
    try:
        stream_index = stream_listbox.curselection()[0]
        stream = root.video.streams.filter(progressive=True)[stream_index]
        directory = directory_entry.get()
        filename = f"{stream.default_filename}"
        filepath = os.path.join(directory, filename)
        if os.path.exists(filepath):
            overwrite = messagebox.askyesno("Overwrite?", f"{filename} already exists in the selected directory. Do you want to overwrite it?")
            if not overwrite:
                return
        if stream.includes_audio_track and not stream.includes_video_track:
            messagebox.showerror("Error", f"Download failed. {filename} is an audio-only track and cannot be downloaded.")
            return
        messagebox.showinfo("Download Started", f"{filename} is being downloaded to {directory}. You will be notified when the download completes.")
        stream.download(output_path=directory, filename=filename)
        messagebox.showinfo("Download Complete", f"{filename} has been downloaded to {directory}")
    except IndexError:
        messagebox.showerror("Error", "Please select a video stream to download.")
    except Exception as e:
        messagebox.showerror("Error", f"Download failed: {str(e)}")


root = tk.Tk()
root.title("Vidloader")

url_label = tk.Label(root, text="Enter video URL:")
url_label.pack()

url_entry = tk.Entry(root, width=50)
url_entry.pack()

download_button = tk.Button(root, text="Choose quality", command=download_video)
download_button.pack()

stream_label = tk.Label(root, text="Select video stream:")
stream_label.pack()

stream_listbox = tk.Listbox(root, width=50)
stream_listbox.pack()

directory_label = tk.Label(root, text="Select download directory:")
directory_label.pack()

directory_entry = tk.Entry(root, width=50)
directory_entry.pack()

directory_button = tk.Button(root, text="Browse", command=select_directory)
directory_button.pack()

start_button = tk.Button(root, text="Start Download", command=start_download)
start_button.pack()

progress_bar = tk.ttk.Progressbar(root, orient=tk.HORIZONTAL, length=200, mode='determinate')
progress_bar.pack()

root.mainloop()
