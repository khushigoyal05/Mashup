import sys
import os
import shutil
from yt_dlp import YoutubeDL
from pydub import AudioSegment

def create_mashup(singer, n, duration, output_file):
    download_dir = 'downloads'
    if os.path.exists(download_dir):
        shutil.rmtree(download_dir)
    os.makedirs(download_dir)

    # yt-dlp options with a browser-like user agent to mitigate 403 errors
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'no_warnings': True,
        'nocheckcertificate': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': f'{download_dir}/%(title)s.%(ext)s',
        'max_downloads': n,
    }

    # Task: Download N videos of X singer [cite: 18, 19]
    with YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([f"ytsearch{n}:{singer} song"])
        except Exception:
            pass 

    # Task: Merge all audios to make a single output file [cite: 22]
    combined = AudioSegment.empty()
    files = sorted([f for f in os.listdir(download_dir) if f.endswith('.mp3')])
    
    if not files:
        # Task: Show appropriate message for errors 
        raise Exception("YouTube blocked the request. This is common on cloud servers.")

    for file in files[:n]:
        path = os.path.join(download_dir, file)
        try:
            # Task: Cut first Y sec audios [cite: 21]
            audio = AudioSegment.from_file(path)
            cut_audio = audio[:duration * 1000] 
            combined += cut_audio
        except Exception:
            continue
    
    combined.export(output_file, format="mp3")

if __name__ == "__main__":
    # Task: Check for correct number of parameters [cite: 25, 26]
    if len(sys.argv) != 5:
        print("Usage: python 102303993.py <SingerName> <NumberOfVideos> <AudioDuration> <OutputFileName>")
        sys.exit(1)

    try:
        singer_name = sys.argv[1]
        num_videos = int(sys.argv[2])
        audio_dur = int(sys.argv[3])
        out_name = sys.argv[4]

        # Constraints: N > 10 and Y > 20 [cite: 18, 21]
        if num_videos <= 10 or audio_dur <= 20:
            print("Error: N must be > 10 and Y must be > 20.")
            sys.exit(1)

        create_mashup(singer_name, num_videos, audio_dur, out_name)

    except Exception as e:
        # Task: Handling of exception [cite: 28]
        print(f"An error occurred: {e}")
        sys.exit(1)