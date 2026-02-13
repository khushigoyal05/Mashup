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

    # 1. Improved Download Options to bypass 403 Forbidden
    ydl_opts = {
        'format': 'bestaudio/best',
        # Helps bypass bot detection
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'referer': 'https://www.google.com/',
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

    # 2. Search and Download
    with YoutubeDL(ydl_opts) as ydl:
        try:
            # Adding "songs" to query often yields better results for singers
            ydl.download([f"ytsearch{n}:{singer} songs"])
        except Exception:
            pass 

    # 3. Process and Merge
    combined = AudioSegment.empty()
    files = sorted([f for f in os.listdir(download_dir) if f.endswith('.mp3')])
    
    if not files:
        raise Exception("No audio files were downloaded. YouTube might be blocking the request.")

    # Only process up to N files
    for file in files[:n]:
        path = os.path.join(download_dir, file)
        try:
            audio = AudioSegment.from_file(path)
            # Y seconds cut
            cut_audio = audio[:duration * 1000]
            combined += cut_audio
        except Exception:
            continue
    
    # 4. Export
    combined.export(output_file, format="mp3")

if __name__ == "__main__":
    # Parameters check per assignment [cite: 12, 24]
    if len(sys.argv) != 5:
        sys.exit(1)

    try:
        singer_name = sys.argv[1]
        num_videos = int(sys.argv[2])
        audio_dur = int(sys.argv[3])
        out_name = sys.argv[4]

        # Assignment constraints: N > 10, Y > 20 
        if num_videos <= 10 or audio_dur <= 20:
            sys.exit(1)

        create_mashup(singer_name, num_videos, audio_dur, out_name)
    except Exception:
        sys.exit(1)