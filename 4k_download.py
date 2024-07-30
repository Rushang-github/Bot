import yt_dlp
import os
from moviepy.editor import VideoFileClip, AudioFileClip

def download_video(url):
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',  # Download best video and audio separately
        'noplaylist': True,  # Avoid downloading playlists
        'outtmpl': '%(title)s.%(ext)s',  # Save with video title
        'quiet': True,  # Suppress output for cleaner responses
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            video_title = info_dict.get('title', 'video') + '.mp4'
            audio_title = info_dict.get('title', 'audio') + '.m4a'  # Assuming audio is saved as m4a

        # Merge video and audio using MoviePy
        merge_video_audio(video_title, audio_title, f'merged_{video_title}')

        print(f"Downloaded and merged video: {video_title}")

        # Clean up the downloaded files after merging
        os.remove(video_title)
        os.remove(audio_title)
        os.remove(f'merged_{video_title}')

    except Exception as e:
        print(f"An error occurred: {e}")

def merge_video_audio(video_path, audio_path, output_path):
    # Load the video and audio files
    video = VideoFileClip(video_path)
    audio = AudioFileClip(audio_path)

    # Set the audio of the video
    final_video = video.set_audio(audio)

    # Write the result to a file
    final_video.write_videofile(output_path, codec='libx264')

if __name__ == '__main__':
    video_url = input("Enter the YouTube video URL: ")
    download_video(video_url)
