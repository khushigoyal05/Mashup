import sys
import os
import shutil
from yt_dlp import YoutubeDL
from pydub import AudioSegment

def create_mashup(singer, n, duration, output_file):
    # Create or clear downloads folder
    if os.path.exists('downloads'):
        shutil.rmtree('downloads')
    os.makedirs('downloads')

    # 1. Search and Download
    ydl_opts = {
        'format': 'bestaudio/best/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'max_downloads': n,
        'quiet': False,  # Changed to False so we see progress
    }

    print(f"--- Step 1: Searching for {singer} ---")
    with YoutubeDL(ydl_opts) as ydl:
        try:
            # Using ytsearch leads to better results
            ydl.download([f"ytsearch{n}:{singer} audio"])
        except Exception as e:
            print(f"Download break (Expected or Error): {e}")

    # 2. Process and Merge
    combined = AudioSegment.empty()
    files = [f for f in os.listdir('downloads') if f.endswith('.mp3')]
    
    print(f"--- Step 2: Found {len(files)} files. Starting Trim ---")
    
    if len(files) == 0:
        print("Error: No files found in downloads folder!")
        return

    for i, file in enumerate(files[:n]):
        path = os.path.join('downloads', file)
        print(f"Processing file {i+1}: {file}")
        audio = AudioSegment.from_file(path)
        cut_audio = audio[:duration * 1000]
        combined += cut_audio
    
    # 3. Export
    print(f"--- Step 3: Exporting to {output_file} ---")
    combined.export(output_file, format="mp3")
    print("--- SUCCESS: Mashup Complete ---")

if __name__ == "__main__":
    # Validate parameters [cite: 25, 26]
    if len(sys.argv) != 5:
        print("Usage: python 102303993.py <SingerName> <NumberOfVideos> <AudioDuration> <OutputFileName>")
        sys.exit(1)

    try:
        singer_name = sys.argv[1]
        num_videos = int(sys.argv[2])
        audio_dur = int(sys.argv[3])
        out_name = sys.argv[4]

        # Assignment constraints [cite: 18, 21]
        if num_videos <= 10:
            print("Error: Number of videos must be greater than 10.") [cite: 27]
            sys.exit(1)
        if audio_dur <= 20:
            print("Error: Audio duration must be greater than 20.") [cite: 27]
            sys.exit(1)

        create_mashup(singer_name, num_videos, audio_dur, out_name)

    except Exception as e:
        print(f"Main Error: {e}") [cite: 28]