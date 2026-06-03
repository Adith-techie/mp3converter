import yt_dlp
from moviepy.editor import AudioFileClip
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, TIT2
import requests
from io import BytesIO
import os

# Always resolve paths relative to this script's directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
def sfx(name):
    return os.path.join(BASE_DIR, "soundfx", name)
from playsound3 import playsound
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import filedialog, messagebox, Toplevel

def download_youtube_video(url, output_path): # format and collecting data
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            title = info_dict.get('title', None)
            thumbnail_url = info_dict.get('thumbnail', None)
            downloaded_file = os.path.join(output_path, f"{title}.mp3")
        
        return downloaded_file, title, thumbnail_url
    except Exception as e:
        print(f"Error downloading audio: {e}")
        return None, None, None

def add_cover_photo(mp3_file, title, cover_url):
    try:
        audio = MP3(mp3_file, ID3=ID3)
        if audio.tags is None:
            audio.add_tags()
        
        # Add the title tag
        audio.tags.add(TIT2(encoding=3, text=title))

        # Download the cover image
        response = requests.get(cover_url)
        if response.status_code != 200:
            print("Failed to download cover image")
            return
        
        cover = BytesIO(response.content)
        mime_type = response.headers['Content-Type']
        
        if mime_type not in ['image/jpeg', 'image/png']:
            print(f"Unsupported image format: {mime_type}")
            return
        
        # Add the cover photo
        audio.tags.add(
            APIC(
                encoding=3,  # UTF-8 encoding
                mime=mime_type,  # MIME type from the HTTP response
                type=3,  # Cover (front)
                desc='Cover',
                data=cover.read()  # Read the binary data
            )
        )
        
        # Save the updated MP3 file
        audio.save(v2_version=3)  # Ensure ID3v2.3 version
        print(f"Cover photo added to {mp3_file}")

    except Exception as e:
        print(f"Error adding cover photo: {e}")

def show_progress_dialog(): # progressbar animation
    progress_dialog = Toplevel(root)
    progress_dialog.title("Downloading...")
    progress_dialog.geometry("400x100")

    label = ttk.Label(progress_dialog, text="Downloading and converting, please wait...", font=("Helvetica", 12))
    label.pack(pady=10)

    progress_bar = ttk.Progressbar(progress_dialog, mode='determinate', bootstyle="success-striped")
    progress_bar.pack(pady=5, fill=X)
    progress_bar["maximum"] = 100

    return progress_dialog, progress_bar

def on_download(): # to store the downloaded file
    url = url_entry.get()
    output_path = filedialog.askdirectory(title="Select Output Folder")
    if not output_path:
        return

    # Ensure the output path exists
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    playsound(sfx("SFX- Ui01.mp3"))

    progress_dialog, progress_bar = show_progress_dialog()

    def download_and_process(): # output
        # Simulate the progress bar movement
        for i in range(101):
            progress_bar["value"] = i
            root.update_idletasks()
            root.after(20)  # delay of 50 milliseconds

        mp3_file, title, cover_url = download_youtube_video(url, output_path)
        progress_dialog.destroy()

        if mp3_file and title and cover_url:
            add_cover_photo(mp3_file, title, cover_url)
            playsound(sfx("SFX- Ui02.mp3"))
            messagebox.showinfo("Success", f"Downloaded and converted {title} to MP3 with cover photo.")
            
        else:
            playsound(sfx("SFX- Ui09.mp3"))
            messagebox.showerror("Error", "Failed to download or convert mp3 :(")

    root.after(100, download_and_process)

def show_about():
    about_window = Toplevel(root)
    about_window.title("About me")
    about_window.geometry("540x500")

    about_label = ttk.Label(about_window, text="About the Developer", font=("Helvetica", 18, "bold"))
    about_label.pack(pady=50)

    developer_info = (
    "Name: Adith\n\n"
    "Email: will be avialable in github\n\n"
    "GitHub: https://github.com/Adith-techie\n\n"
    "LinkedIn: https://www.linkedin.com/in/adith-k-a88b6730a\n\n\n"

    "This application was developed to convert YouTube videos to MP3 format with cover photos.\n"
    )
    info_label = ttk.Label(about_window, text=developer_info, font=("Helvetica", 12), wraplength=500)
    info_label.pack(pady=5, padx=5)

# Setting up the GUI
root = ttk.Window(themename="vapor")
root.title("YouTube to MP3 Converter")
root.geometry("540x600")

frame = ttk.Frame(root, padding="10")
frame.pack(padx=10, pady=10, fill=BOTH, expand=True)

title_label = ttk.Label(frame, text="YouTube to MP3 Converter", font=("Helvetica", 18, "bold"))
title_label.pack(pady=80)

url_label = ttk.Label(frame, text="Enter the YouTube URL:", font=("Helvetica", 12))
url_label.pack(pady=20)

url_entry = ttk.Entry(frame, width=30, font=("Helvetica", 12))
url_entry.pack(pady=5)

download_button = ttk.Button(frame, width="10", text="Download", command=on_download, bootstyle="success-outline")
download_button.pack(pady=60)

about_button = ttk.Button(frame, width="10" , text="About me", command=show_about, bootstyle="info-outline")
about_button.pack(pady=10)

playsound(sfx("SFX- Ui03.mp3"))
root.mainloop()
