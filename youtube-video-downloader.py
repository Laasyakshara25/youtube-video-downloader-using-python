from pytubefix import YouTube
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk


def update_progress(stream, chunk, bytes_remaining):
    # progress bar
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    progress = (bytes_downloaded / total_size) * 100
    progress_bar['value'] = progress
    progress_label.config(text=f"Progress: {progress:.2f}%")
    app.update_idletasks()


def download_video():
    # Handles the video download process
    url = url_entry.get()
    save_path = folder_path.get()

    # Reset progress bar and status message
    progress_bar['value'] = 0
    progress_label.config(text="Progress: 0%")
    status_label.config(text="", foreground="black")
    status_message.set("")  # Clear the scrolling message

    if not url:
        status_label.config(text="Error: Please enter a YouTube URL.", foreground="red")
        return

    if not save_path:
        status_label.config(text="Error: Please select a save folder.", foreground="red")
        return

    try:
        # Indicate download start
        status_label.config(text="Downloading started...", foreground="blue")
        status_message.set("Fetching video details...")
        app.update_idletasks()

        yt = YouTube(url, on_progress_callback=update_progress)
        streams = yt.streams.filter(progressive=True, file_extension="mp4")
        highest_res_stream = streams.get_highest_resolution()

        # Update status
        status_message.set(f"Downloading: '{yt.title}'...")
        app.update_idletasks()

        # Download the video
        highest_res_stream.download(output_path=save_path)

        # Indicate download completion
        status_label.config(text="Download completed!", foreground="green")
        status_message.set(f"'{yt.title}' downloaded successfully.")
        progress_label.config(text="Progress: 100%")
    except Exception as e:
        status_label.config(text="Error occurred during download.", foreground="red")
        status_message.set(f"Error: {e}")


def browse_folder():
    """Opens a dialog to select the folder."""
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        folder_path.set(folder_selected)


# Create the main application window
app = tk.Tk()
app.title("YouTube Video Downloader")
app.geometry("700x450")  # Larger window size
app.resizable(False, False)

# String variables for inputs
folder_path = tk.StringVar()
status_message = tk.StringVar()

# Title label
title_label = tk.Label(app, text="YouTube Video Downloader", font=("Helvetica", 20, "bold"))
title_label.pack(pady=15)

# URL input section
url_label = tk.Label(app, text="Enter YouTube URL:", font=("Helvetica", 14))
url_label.pack(pady=5)
url_entry = ttk.Entry(app, width=70, font=("Helvetica", 12))
url_entry.pack(pady=5)

# Folder selection section
folder_label = tk.Label(app, text="Select Save Folder:", font=("Helvetica", 14))
folder_label.pack(pady=5)
folder_frame = tk.Frame(app)
folder_frame.pack(pady=5)

folder_entry = ttk.Entry(folder_frame, textvariable=folder_path, width=55, font=("Helvetica", 12))
folder_entry.pack(side=tk.LEFT, padx=5)
browse_button = ttk.Button(folder_frame, text="Browse", command=browse_folder)
browse_button.pack(side=tk.LEFT)

# Download button (subtle color)
download_button = ttk.Button(app, text="Download", command=download_video, style="Subtle.TButton")
download_button.pack(pady=20)

# Progress bar
progress_bar = ttk.Progressbar(app, orient="horizontal", length=600, mode="determinate")
progress_bar.pack(pady=10)

# Progress percentage
progress_label = tk.Label(app, text="Progress: 0%", font=("Helvetica", 12))
progress_label.pack(pady=5)

# Status message
status_label = tk.Label(app, text="", font=("Helvetica", 14))
status_label.pack(pady=10)

# Scrolling status messages
scroll_frame = tk.Frame(app)
scroll_frame.pack(fill=tk.BOTH, expand=True, pady=10)

scroll_message = tk.Label(scroll_frame, textvariable=status_message, font=("Helvetica", 12), wraplength=650, justify="left")
scroll_message.pack(anchor="w", padx=10)

# Apply custom style for the download button (subtle color)
style = ttk.Style(app)
style.configure("Subtle.TButton",
                font=("Helvetica", 16),
                padding=10,
                background="#a8d0e6",  # Light blue color
                foreground="black",
                relief="flat")
style.map("Subtle.TButton", background=[("active", "#6c9bd9"), ("pressed", "#6c9bd9")])

# Start the Tkinter main loop
app.mainloop()
