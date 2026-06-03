# YouTube to MP3 Converter

A simple Python desktop application that downloads audio from YouTube videos, converts it to MP3, and embeds the video thumbnail as the cover image.

## Features

- Download audio from YouTube using `yt_dlp`
- Convert downloaded audio to MP3 using `moviepy`
- Add MP3 metadata and cover art using `mutagen`
- Simple GUI built with `tkinter` and `ttkbootstrap`
- Plays UI sound effects during download and completion

## Requirements

- Python 3.8+
- ffmpeg installed and available on your PATH

## Python dependencies

- `yt_dlp`
- `moviepy`
- `mutagen`
- `requests`
- `playsound3`
- `ttkbootstrap`

## Installation

1. Clone or download the project.
2. Create a virtual environment (recommended):

```bash
python -m venv venv
```

3. Activate the environment:

```bash
venv\Scripts\activate
```

4. Install dependencies:

```bash
pip install yt_dlp moviepy mutagen requests playsound3 ttkbootstrap
```

## Usage

1. Run the app:

```bash
python mp3converterpy\mymp3converter.py
```

2. Enter a YouTube video URL.
3. Choose an output folder.
4. Wait for the download and conversion to complete.

## Notes

- The app saves the converted MP3 file into the selected folder.
- It attempts to download the video thumbnail and embed it as the cover image.
- If the subtitle or thumbnail download fails, the app may still save the MP3 file without cover art.

## Project Structure

- `mp3converterpy/mymp3converter.py` - Main application script
- `mp3converterpy/soundfx/` - UI sound effect files
- `downloads/` - Sample or output directory placeholder

## License

This project is provided as-is for learning and personal use.
