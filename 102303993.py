import sys
import os
import shutil
from yt_dlp import YoutubeDL
from pydub import AudioSegment

def create_mashup(singer, n, duration, output_file):
    # Set up a clean downloads directory
    download_dir = os.path.join(os.getcwd(), 'downloads')
    if os.path.exists(download_dir):
        shutil.rmtree(download_dir)
    os.makedirs(download_dir)

    # 1. Download Options
    ydl_opts = {
        'format': 'bestaudio/best',
        # User agent helps avoid being blocked by YouTube on cloud servers
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(download_dir, '%(title)s.%(ext)s'),
        'max_downloads': n,
        'quiet': True,
        'no_warnings': True,
    }

    # 2. Search and Download
    print(f"Searching and downloading {n} videos for {singer}...")
    with YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([f"ytsearch{n}:{singer} audio"])
        except Exception:
            # yt-dlp raises an error when max_downloads is hit; we catch it to continue
            pass

    # 3. Process and Merge
    combined = AudioSegment.empty()
    files = sorted([f for f in os.listdir(download_dir) if f.endswith('.mp3')])
    
    if not files:
        print("Error: No audio files were downloaded.")
        sys.exit(1)

    print(f"Trimming first {duration} seconds and merging...")
    for file in files[:n]:
        path = os.path.join(download_dir, file)
        try:
            audio = AudioSegment.from_file(path)
            # Cut first Y seconds (duration * 1000 for milliseconds)
            cut_audio = audio[:duration * 1000]
            combined += cut_audio
        except Exception as e:
            print(f"Skipping {file} due to error: {e}")
    
    # 4. Export final result
    combined.export(output_file, format="mp3")
    print(f"SUCCESS: Mashup saved as {output_file}")

if __name__ == "__main__":
    # Check for correct number of parameters
    if len(sys.argv) != 5:
        print("Usage: python 102303993.py <SingerName> <NumberOfVideos> <AudioDuration> <OutputFileName>")
        sys.exit(1)

    try:
        singer_name = sys.argv[1]
        num_videos = int(sys.argv[2])
        audio_dur = int(sys.argv[3])
        out_name = sys.argv[4]

        # Validating assignment constraints
        if num_videos <= 10:
            print("Error: Number of videos (N) must be greater than 10.")
            sys.exit(1)
        if audio_dur <= 20:
            print("Error: Audio duration (Y) must be greater than 20.")
            sys.exit(1)

        create_mashup(singer_name, num_videos, audio_dur, out_name)

    except ValueError:
        print("Error: Number of videos and Duration must be integers.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")