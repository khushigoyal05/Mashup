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

    # 1. Bypass 403 Forbidden with better headers
    ydl_opts = {
        'format': 'bestaudio/best',
        'nocheckcertificate': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': f'{download_dir}/%(title)s.%(ext)s',
        'max_downloads': n,
        'quiet': True,
        'no_warnings': True,
    }

    # 2. Search and Download [cite: 18, 19]
    with YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([f"ytsearch{n}:{singer}"])
        except Exception:
            pass 

    # 3. Process and Merge [cite: 20, 21, 22]
    combined = AudioSegment.empty()
    files = sorted([f for f in os.listdir(download_dir) if f.endswith('.mp3')])
    
    if not files:
        raise Exception("YouTube blocked the request. Try a different singer name.")

    for file in files[:n]:
        path = os.path.join(download_dir, file)
        try:
            audio = AudioSegment.from_file(path)
            cut_audio = audio[:duration * 1000] 
            combined += cut_audio
        except Exception:
            continue
    
    combined.export(output_file, format="mp3")

if __name__ == "__main__":
    # Check for correct number of parameters [cite: 25, 26]
    if len(sys.argv) != 5:
        print("Usage: python <program.py> <SingerName> <NumberOfVideos> <AudioDuration> <OutputFileName>") [cite: 24]
        sys.exit(1)

    try:
        singer_name = sys.argv[1]
        num_videos = int(sys.argv[2])
        audio_dur = int(sys.argv[3])
        out_name = sys.argv[4]

        # Validating assignment constraints 
        if num_videos <= 10 or audio_dur <= 20:
            print("N must be > 10 and Y must be > 20") [cite: 27]
            sys.exit(1)

        create_mashup(singer_name, num_videos, audio_dur, out_name)
    except Exception as e:
        print(f"Error: {e}") [cite: 28]
        sys.exit(1)