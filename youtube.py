# pytube is not working anymore
# use pytubefix instead
from pytubefix import YouTube
from pytubefix.request import stream
import tkinter as tk
from tkinter import filedialog

def download_video(url, save_path):
    try:
        yt = YouTube(url)
        streams = yt.streams.filter(progressive=True, file_extension="mp4")
        highest_res_stream = streams.get_highest_resolution()
        highest_res_stream.download(output_path=save_path)
        print("Video downloaded successfully!!")

    except Exception as e:
            print(e)


def open_file_dialogue():
    folder = filedialog.askdirectory()
    if folder:
        print(f"Selected folder: {folder}")
    return folder

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()

    video_url = input("Please enter a YouTube url: ")
    save_dir = open_file_dialogue()

    if save_dir:
        print("Download started")
        download_video(video_url, save_dir)
    else:
        print("Invalid save direction.")